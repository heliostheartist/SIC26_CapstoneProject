"""
dropout_utils.py
Module dùng chung cho notebook tiểu luận và app Streamlit.
Giữ ở cùng thư mục với notebook và app.py.

Nội dung:
  - load_data(): đọc bộ UCI "Predict students' dropout and academic success"
  - add_features(): tạo biến mới từ nghiệp vụ (chỉ dùng thông tin trong CÙNG MỘT dòng,
    nên không gây rò rỉ dữ liệu giữa train/test)
  - SCENARIOS / scenario_columns(): các kịch bản theo thời điểm dự báo
  - build_pipeline(): tiền xử lý + mô hình (fit bên trong từng fold nên không leak)
  - net_benefit_table(): phân tích chi phí - lợi ích theo ngưỡng
"""
from __future__ import annotations

import os
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, confusion_matrix, f1_score,
                             precision_score, recall_score)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, RobustScaler

SEED = 42
TARGET = "Target"

# 1. Nhóm biến
CAT_COLS = [
    "Marital Status", "Application mode", "Course", "Daytime/evening attendance",
    "Previous qualification", "Nacionality", "Mother's qualification",
    "Father's qualification", "Mother's occupation", "Father's occupation",
]
SEM1 = [
    "Curricular units 1st sem (credited)", "Curricular units 1st sem (enrolled)",
    "Curricular units 1st sem (evaluations)", "Curricular units 1st sem (approved)",
    "Curricular units 1st sem (grade)", "Curricular units 1st sem (without evaluations)",
]
SEM2 = [c.replace("1st sem", "2nd sem") for c in SEM1]
FIN_CORE = ["Debtor", "Tuition fees up to date"]     # thời điểm đo không rõ -> tách riêng
MACRO = ["Unemployment rate", "Inflation rate", "GDP"]

# Tên ngành theo mô tả của bộ dữ liệu UCI (nên đối chiếu lại với tài liệu gốc khi trích dẫn)
COURSE_NAMES = {
    33: "Biofuel Production Technologies", 171: "Animation & Multimedia Design",
    8014: "Social Service (evening)", 9003: "Agronomy", 9070: "Communication Design",
    9085: "Veterinary Nursing", 9119: "Informatics Engineering", 9130: "Equinculture",
    9147: "Management", 9238: "Social Service", 9254: "Tourism", 9500: "Nursing",
    9556: "Oral Hygiene", 9670: "Advertising & Marketing Mgmt",
    9773: "Journalism & Communication", 9853: "Basic Education",
    9991: "Management (evening)",
}


# 2. Đọc dữ liệu
def _clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    cleaned = [str(c).strip().strip('"').replace("\t", "").strip() for c in df.columns]
    # UCI files may spell this header "Marital status"; use one canonical name.
    aliases = {"marital status": "Marital Status"}
    df.columns = [aliases.get(c.casefold(), c) for c in cleaned]
    return df


def load_data(path: str | None = None) -> pd.DataFrame:
    """Thứ tự thử: path chỉ định -> file local (data.csv, data_clean.csv) -> ucimlrepo (id=697)."""
    cands = [path] if path else []
    cands += ["data/raw/data.csv", "data/data.csv", "data.csv", "data/data_clean.csv", "data_clean.csv"]
    for p in cands:
        if p and os.path.exists(p):
            df = pd.read_csv(p, sep=";")
            if df.shape[1] < 5:                     # file dùng dấu phẩy
                df = pd.read_csv(p)
            df = _clean_columns(df)
            for c in df.columns:
                if c != TARGET:
                    df[c] = pd.to_numeric(df[c], errors="coerce")
            print(f"Đọc dữ liệu từ: {p}  ->  {df.shape}")
            return df
    try:
        from ucimlrepo import fetch_ucirepo
        d = fetch_ucirepo(id=697)
        df = pd.concat([d.data.features, d.data.targets], axis=1)
        df = _clean_columns(df)
        print(f"Đọc dữ liệu từ UCI (ucimlrepo id=697)  ->  {df.shape}")
        return df
    except Exception as e:                           #
        raise FileNotFoundError(
            "Không tìm thấy dữ liệu. Hãy đặt data.csv (bản gốc UCI, dấu ';') vào thư mục data/ "
            "hoặc chạy: pip install ucimlrepo"
        ) from e


# 3. Feature engineering (chỉ dùng thông tin trong cùng một dòng)
def _safe_div(a, b):
    return np.where(b > 0, a / np.where(b > 0, b, 1), 0.0)


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    d = df.copy()
    # (1) Đà học tập: điểm đầu vào so với điểm THPT/bằng trước đó
    if {"Admission grade", "Previous qualification (grade)"} <= set(d.columns):
        d["grade_gap"] = d["Admission grade"] - d["Previous qualification (grade)"]

    for k, tag in (("1st", "s1"), ("2nd", "s2")):
        enr = f"Curricular units {k} sem (enrolled)"
        ev = f"Curricular units {k} sem (evaluations)"
        ap = f"Curricular units {k} sem (approved)"
        noev = f"Curricular units {k} sem (without evaluations)"
        if {enr, ev, ap, noev} <= set(d.columns):
            # (2) Tỷ lệ môn đạt trên môn đăng ký: đo tiến độ học thật sự
            d[f"{tag}_approval_rate"] = _safe_div(d[ap], d[enr])
            # (3) Tỷ lệ đạt trên số lần thi: đo hiệu quả thi cử
            d[f"{tag}_eval_pass_rate"] = _safe_div(d[ap], d[ev])
            # (4) Tỷ lệ môn không dự thi: tín hiệu "rời bỏ" sớm
            d[f"{tag}_no_eval_rate"] = _safe_div(d[noev], d[enr])
            # (5) Đăng ký môn nhưng không có lần đánh giá nào ("sinh viên ma")
            d[f"{tag}_ghost"] = ((d[enr] > 0) & (d[ev] == 0)).astype(int)

    # (6) Xu hướng giữa hai kỳ (chỉ có ở kịch bản đầy đủ)
    if "s1_approval_rate" in d and "s2_approval_rate" in d:
        d["d_approval_rate"] = d["s2_approval_rate"] - d["s1_approval_rate"]
        d["d_approved"] = (d["Curricular units 2nd sem (approved)"]
                           - d["Curricular units 1st sem (approved)"])
        d["d_grade"] = (d["Curricular units 2nd sem (grade)"]
                        - d["Curricular units 1st sem (grade)"])

    # (7) Áp lực tài chính: nợ/chưa đóng học phí và không có học bổng
    if {"Debtor", "Tuition fees up to date"} <= set(d.columns):
        d["fin_risk"] = d["Debtor"] + (1 - d["Tuition fees up to date"])
        if "Scholarship holder" in d:
            d["fin_no_aid"] = ((d["fin_risk"] > 0) & (d["Scholarship holder"] == 0)).astype(int)
    return d


FE_S1 = ["s1_approval_rate", "s1_eval_pass_rate", "s1_no_eval_rate", "s1_ghost"]
FE_S2 = ["s2_approval_rate", "s2_eval_pass_rate", "s2_no_eval_rate", "s2_ghost",
         "d_approval_rate", "d_approved", "d_grade"]
FE_FIN = ["fin_risk", "fin_no_aid"]

SCENARIO_LABELS = {
    "S0": "S0 - Lúc nhập học (chưa có điểm)",
    "S1": "S1 - Hết học kỳ 1 (không gồm tài chính)",
    "S1F": "S1F - Hết học kỳ 1 + Nợ/học phí",
    "S2": "S2 - Hết học kỳ 2 + Nợ/học phí (đối chứng, cảnh báo muộn)",
}


def scenario_columns(name: str, all_cols) -> list[str]:
    """Danh sách cột đầu vào theo kịch bản (chỉ lấy cột thật sự có trong dữ liệu)."""
    all_cols = list(all_cols)
    base = [c for c in all_cols
            if c not in SEM1 + SEM2 + FIN_CORE + [TARGET, "label"]
            and not c.startswith(("s1_", "s2_", "d_", "fin_"))]
    cols = {
        "S0": base,
        "S1": base + SEM1 + FE_S1,
        "S1F": base + SEM1 + FE_S1 + FIN_CORE + FE_FIN,
        "S2": base + SEM1 + FE_S1 + FIN_CORE + FE_FIN + SEM2 + FE_S2,
    }[name]
    return [c for c in dict.fromkeys(cols) if c in all_cols]


# 4. Tiền xử lý + mô hình
def build_preprocessor(cols: list[str]) -> ColumnTransformer:
    cat = [c for c in CAT_COLS if c in cols]
    num = [c for c in cols if c not in cat]
    return ColumnTransformer([
        ("num", Pipeline([("imp", SimpleImputer(strategy="median")),
                          ("sc", RobustScaler())]), num),
        ("cat", Pipeline([("imp", SimpleImputer(strategy="most_frequent")),
                          ("oh", OneHotEncoder(handle_unknown="ignore", min_frequency=10,
                                               sparse_output=False))]), cat),
    ])


def make_estimator(name: str, params: dict | None = None):
    params = dict(params or {})
    if name == "Dummy":
        return DummyClassifier(strategy="prior")
    if name == "LR":
        base = dict(max_iter=4000)
        return LogisticRegression(**{**base, **params})
    if name == "RF":
        base = dict(n_estimators=300, min_samples_leaf=2, random_state=SEED, n_jobs=-1)
        return RandomForestClassifier(**{**base, **params})
    if name == "XGB":
        from xgboost import XGBClassifier
        base = dict(n_estimators=300, learning_rate=0.05, max_depth=4, subsample=0.9,
                    colsample_bytree=0.9, eval_metric="logloss", random_state=SEED, n_jobs=-1)
        return XGBClassifier(**{**base, **params})
    raise ValueError(name)


def build_pipeline(name: str, cols: list[str], params: dict | None = None) -> Pipeline:
    return Pipeline([("pre", build_preprocessor(cols)), ("clf", make_estimator(name, params))])


# 5. Chỉ số và phân tích chi phí - lợi ích
def metrics_at(y, p, t=0.5) -> dict:
    y = np.asarray(y)
    pred = (np.asarray(p) >= t).astype(int)
    tn, fp, fn, tp = confusion_matrix(y, pred, labels=[0, 1]).ravel()
    return dict(threshold=t, accuracy=accuracy_score(y, pred),
                precision=precision_score(y, pred, zero_division=0),
                recall=recall_score(y, pred, zero_division=0),
                f1=f1_score(y, pred, zero_division=0),
                TN=tn, FP=fp, FN=fn, TP=tp, flagged=int(pred.sum()))


def net_benefit_table(y, p, thresholds, L=1.0, c=0.05, s=0.30) -> pd.DataFrame:
    """
    Lợi ích ròng so với 'không can thiệp'.
      L: thiệt hại khi mất 1 sinh viên (đơn vị: tiền học phí 1 năm)
      c: chi phí 1 lần can thiệp (cùng đơn vị)
      s: xác suất can thiệp giữ được sinh viên thật sự có nguy cơ
    Lợi ích = s * L * TP ;  Chi phí = c * (TP + FP)
    """
    y = np.asarray(y)
    rows = []
    for t in thresholds:
        pred = (np.asarray(p) >= t).astype(int)
        tp = int(((pred == 1) & (y == 1)).sum())
        fp = int(((pred == 1) & (y == 0)).sum())
        benefit, cost = s * L * tp, c * (tp + fp)
        rows.append(dict(threshold=t, TP=tp, FP=fp, benefit=benefit, cost=cost,
                         net=benefit - cost, net_per_student=(benefit - cost) / len(y),
                         roi=(benefit - cost) / cost if cost > 0 else np.nan))
    return pd.DataFrame(rows)


# 6. SHAP (gộp one-hot về biến gốc để đọc theo ngôn ngữ nghiệp vụ)
def _raw_of(name: str) -> str:
    for c in sorted(CAT_COLS, key=len, reverse=True):
        if name.startswith(c + "_"):
            return c
    return name


def shap_values(pipe, X_raw: pd.DataFrame, X_bg_raw: pd.DataFrame | None = None,
                max_bg: int = 200) -> dict:
    """Trả về dict: values_t/names_t (sau one-hot), values_raw/names_raw (đã gộp), base."""
    import shap
    pre, clf = pipe.named_steps["pre"], pipe.named_steps["clf"]
    Xt = pre.transform(X_raw)
    names_t = [n.split("__", 1)[1] for n in pre.get_feature_names_out()]
    bg = Xt if X_bg_raw is None else pre.transform(X_bg_raw)
    if len(bg) > max_bg:
        bg = bg[np.random.default_rng(SEED).choice(len(bg), max_bg, replace=False)]
    try:
        if isinstance(clf, LogisticRegression):
            ex = shap.LinearExplainer(clf, bg)
        else:
            ex = shap.TreeExplainer(clf)
        sv, base = ex.shap_values(Xt), ex.expected_value
    except Exception:                                   # mô hình không có explainer chuyên biệt
        f = lambda z: clf.predict_proba(z)[:, 1]        
        res = shap.Explainer(f, shap.maskers.Independent(bg, max_samples=100))(Xt)
        sv, base = res.values, float(np.mean(res.base_values))
    if isinstance(sv, list):
        sv = sv[-1]
    sv = np.asarray(sv)
    if sv.ndim == 3:
        sv = sv[:, :, -1]
    base = float(np.ravel(base)[-1])
    raw_names = list(dict.fromkeys(_raw_of(n) for n in names_t))
    sv_raw = np.column_stack([sv[:, [i for i, n in enumerate(names_t) if _raw_of(n) == r]].sum(1)
                              for r in raw_names])
    return dict(values_t=sv, names_t=names_t, data_t=Xt, values_raw=sv_raw,
                names_raw=raw_names, data_raw=X_raw[raw_names].to_numpy(dtype=float), base=base)


def top_reasons(sv: dict, k: int = 3) -> list[str]:
    out = []
    for row in sv["values_raw"]:
        idx = np.argsort(-np.abs(row))[:k]
        out.append("; ".join(f"{sv['names_raw'][i]} ({'tăng' if row[i] > 0 else 'giảm'} rủi ro)"
                             for i in idx))
    return out