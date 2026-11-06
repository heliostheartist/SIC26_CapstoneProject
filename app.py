"""Ứng dụng hỗ trợ quản lý và tư vấn sinh viên có nguy cơ nghỉ học.

Chạy: streamlit run app.py
Cần có dropout_utils.py và artifacts/ được tạo từ notebook.
"""
import io
import json

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

import dropout_utils as U

st.set_page_config(
    page_title="Hỗ trợ cố vấn sinh viên",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_resource
def load_artifacts():
    model = joblib.load("models/artifacts/model.joblib")
    with open("models/artifacts/meta.json", encoding="utf-8") as f:
        meta = json.load(f)
    background = pd.read_csv("models/artifacts/background.csv")
    return model, meta, background


try:
    model, meta, background = load_artifacts()
except Exception as exc:  # noqa: BLE001
    st.error("Chưa có mô hình. Hãy chạy notebook để tạo thư mục artifacts/. Chi tiết: " + str(exc))
    st.stop()

COLS = meta["columns"]
RAW = meta["raw_inputs"]
DEFAULTS = meta["defaults"]
T_LOW, T_HIGH = float(meta["t_low"]), float(meta["t_high"])
COURSE = {int(k): v for k, v in meta["course_names"].items()}

TIER_STYLE = {
    "Đỏ": {"color": "#B42318", "label": "Ưu tiên liên hệ sớm"},
    "Vàng": {"color": "#A15C00", "label": "Cố vấn cần xem lại hồ sơ"},
    "Xanh": {"color": "#18794E", "label": "Theo dõi định kỳ"},
}
ACTIONS = {
    "Đỏ": [
        "Cố vấn chủ động liên hệ để tìm hiểu khó khăn hiện tại.",
        "Rà soát môn chưa đạt và cùng sinh viên lập kế hoạch học tập.",
        "Trao đổi về hỗ trợ tài chính hoặc dịch vụ hỗ trợ phù hợp nếu cần.",
    ],
    "Vàng": [
        "Cố vấn xem lại hồ sơ trước khi quyết định có liên hệ.",
        "Nhắc lịch học/thi và chia sẻ tài nguyên hỗ trợ học tập.",
    ],
    "Xanh": ["Tiếp tục theo dõi định kỳ và đánh giá lại ở kỳ tiếp theo."],
}
FEATURE_LABELS = {
    "Course": "Ngành học",
    "Age at enrollment": "Tuổi khi nhập học",
    "Gender": "Giới tính",
    "Scholarship holder": "Tình trạng học bổng",
    "Admission grade": "Điểm đầu vào",
    "Previous qualification (grade)": "Điểm bằng cấp trước",
    "Curricular units 1st sem (enrolled)": "Số môn đăng ký kỳ 1",
    "Curricular units 1st sem (evaluations)": "Số lần đánh giá kỳ 1",
    "Curricular units 1st sem (approved)": "Số môn đạt kỳ 1",
    "Curricular units 1st sem (grade)": "Điểm trung bình kỳ 1",
    "Curricular units 1st sem (credited)": "Số môn được công nhận tín chỉ",
    "Curricular units 1st sem (without evaluations)": "Số môn không có đánh giá",
    "s1_approval_rate": "Tỷ lệ môn đạt kỳ 1",
    "s1_eval_pass_rate": "Tỷ lệ đạt qua đánh giá kỳ 1",
    "s1_no_eval_rate": "Tỷ lệ môn không có đánh giá",
    "s1_ghost": "Đăng ký nhưng không dự đánh giá",
    "grade_gap": "Chênh lệch điểm đầu vào và bằng cấp trước",
}


def tier_of(probability: float) -> str:
    return "Đỏ" if probability >= T_HIGH else ("Vàng" if probability >= T_LOW else "Xanh")


def predict(df_raw: pd.DataFrame) -> np.ndarray:
    return model.predict_proba(U.add_features(df_raw)[COLS])[:, 1]


def explain(df_raw: pd.DataFrame, k: int = 5) -> pd.DataFrame:
    shap_result = U.shap_values(model, U.add_features(df_raw)[COLS], background[COLS])
    values = shap_result["values_raw"][0]
    relevant = [i for i, name in enumerate(shap_result["names_raw"]) if name in FEATURE_LABELS]
    relevant.sort(key=lambda i: abs(values[i]), reverse=True)
    relevant = relevant[:k]
    return pd.DataFrame({
        "Yếu tố": [FEATURE_LABELS[shap_result["names_raw"][i]] for i in relevant],
        "Đóng góp": [float(values[i]) for i in relevant],
    })


def show_explanation(explanation: pd.DataFrame):
    chart = explanation.sort_values("Đóng góp")
    colors = ["#3478A8" if value < 0 else "#C2413A" for value in chart["Đóng góp"]]
    fig, ax = plt.subplots(figsize=(7.5, max(2.5, 0.48 * len(chart))))
    ax.barh(chart["Yếu tố"], chart["Đóng góp"], color=colors, height=0.66)
    ax.axvline(0, color="#374151", linewidth=1)
    ax.set_xlabel("Đóng góp tương đối vào dự đoán của mô hình")
    ax.grid(axis="x", alpha=0.2)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
    st.caption("Đỏ: đẩy dự đoán lên · Xanh: kéo dự đoán xuống. SHAP giải thích mô hình, không chứng minh nguyên nhân.")


def match_expected_column_names(df: pd.DataFrame) -> pd.DataFrame:
    expected = {str(name).strip().casefold(): name for name in RAW}
    rename = {
        col: expected[str(col).strip().casefold()]
        for col in df.columns
        if str(col).strip().casefold() in expected
        and col != expected[str(col).strip().casefold()]
    }
    return df.rename(columns=rename)


def read_csv_upload(uploaded_file) -> pd.DataFrame:
    raw_bytes = uploaded_file.getvalue()
    try:
        frame = pd.read_csv(io.BytesIO(raw_bytes), sep=";")
        if frame.shape[1] < 5:
            frame = pd.read_csv(io.BytesIO(raw_bytes))
    except UnicodeDecodeError:
        frame = pd.read_csv(io.BytesIO(raw_bytes), sep=";", encoding="latin-1")
        if frame.shape[1] < 5:
            frame = pd.read_csv(io.BytesIO(raw_bytes), encoding="latin-1")
    return match_expected_column_names(U._clean_columns(frame))


def prepare_for_scoring(source: pd.DataFrame):
    frame = source.copy().reset_index(drop=True)
    missing = [name for name in RAW if name not in frame.columns]
    for name in missing:
        frame[name] = DEFAULTS[name]
    for name in RAW:
        frame[name] = pd.to_numeric(frame[name], errors="coerce")
        frame[name] = frame[name].fillna(DEFAULTS[name])
    return frame, missing


def score_frame(frame: pd.DataFrame) -> pd.DataFrame:
    probabilities = predict(frame[RAW])
    results = pd.DataFrame({
        "Dòng dữ liệu": np.arange(1, len(frame) + 1),
        "Xác suất nghỉ học": probabilities,
        "Mức ưu tiên": [tier_of(p) for p in probabilities],
    })
    results = results.sort_values("Xác suất nghỉ học", ascending=False).reset_index(drop=True)
    results.insert(0, "Thứ hạng", np.arange(1, len(results) + 1))
    return results


def risk_badge(tier: str):
    style = TIER_STYLE[tier]
    st.markdown(
        f"<div style='display:inline-block;padding:8px 12px;border-radius:999px;"
        f"background:{style['color']};color:white;font-weight:700'>{tier} · {style['label']}</div>",
        unsafe_allow_html=True,
    )


st.markdown("""
<style>
    .block-container {padding-top: 1.7rem; padding-bottom: 3rem; max-width: 1450px;}
    [data-testid="stMetric"] {background:var(--secondary-background-color);
        color:var(--text-color); border:1px solid rgba(128,128,128,.28);
        padding:14px 16px; border-radius:12px;}
    [data-testid="stMetric"] label, [data-testid="stMetric"] [data-testid="stMetricValue"]
        {color:var(--text-color) !important;}
    /* Force readable text in BaseWeb inputs in both light and dark themes. */
    div[data-testid="stNumberInput"] input,
    div[data-testid="stTextInput"] input,
    div[data-testid="stSelectbox"] input {
        color:var(--text-color) !important;
        -webkit-text-fill-color:var(--text-color) !important;
        background-color:var(--background-color) !important;
        caret-color:var(--text-color) !important;
        border-color:rgba(128,128,128,.45) !important;
    }
    div[data-testid="stNumberInput"] button {
        color:var(--text-color) !important;
        background-color:var(--secondary-background-color) !important;
        border-color:rgba(128,128,128,.4) !important;
    }
    .hero {padding:22px 24px; border-radius:16px; background:linear-gradient(110deg,#123B5D,#176B70);
        color:white; margin-bottom:18px;}
    .hero h1 {margin:0 0 6px 0; font-size:1.8rem;}
    .hero p {margin:0; opacity:.9;}
    .note {padding:12px 14px; background:#F3F7FA; border-left:4px solid #3478A8; border-radius:6px;}
</style>
""", unsafe_allow_html=True)

st.markdown(
    "<div class='hero'><h1>🎓 Bảng điều hành hỗ trợ sinh viên</h1>"
    "<p>Ưu tiên hồ sơ cần cố vấn xem xét sau học kỳ 1 · Công cụ hỗ trợ quyết định của con người</p></div>",
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("### Trung tâm hỗ trợ học tập")
    st.caption(f"Kịch bản: {meta['scenario_label']}")
    st.markdown("**Mức ưu tiên**")
    st.markdown(f"🔴 Đỏ: ≥ {T_HIGH:.2f} · Liên hệ sớm")
    st.markdown(f"🟡 Vàng: {T_LOW:.2f}–<{T_HIGH:.2f} · Cố vấn xem lại")
    st.markdown(f"🟢 Xanh: < {T_LOW:.2f} · Theo dõi định kỳ")
    st.divider()
    st.caption("Dự báo là tín hiệu ưu tiên, không phải kết luận về cá nhân. Cố vấn xác minh hoàn cảnh trước khi hỗ trợ.")

tab_dashboard, tab_student, tab_model = st.tabs([
    "📋 Danh sách cần ưu tiên",
    "👤 Đánh giá một hồ sơ",
    "ℹ️ Mô hình & cách dùng",
])


with tab_dashboard:
    st.subheader("Danh sách sinh viên")
    st.caption("Tải CSV để xếp hạng hồ sơ theo xác suất nghỉ học. Cột Target nếu có sẽ không được dùng làm đầu vào.")
    uploaded_file = st.file_uploader("Chọn file CSV", type=["csv"], key="dashboard_csv")

    if uploaded_file is None:
        st.markdown(
            "<div class='note'><b>Bắt đầu:</b> tải danh sách CSV theo các cột của bộ dữ liệu UCI. "
            "Bạn có thể xem tổng quan mức ưu tiên, lọc danh sách, tải kết quả và mở giải thích cho từng hồ sơ.</div>",
            unsafe_allow_html=True,
        )
        st.info("Chưa có dữ liệu để chấm điểm. Dùng tab ‘Đánh giá một hồ sơ’ để thử nhập một trường hợp.")
    else:
        try:
            source = read_csv_upload(uploaded_file)
            scoring_frame, missing = prepare_for_scoring(source)
            if scoring_frame.empty:
                st.warning("File CSV không có hồ sơ dữ liệu.")
            else:
                if missing:
                    st.warning(
                        f"File thiếu {len(missing)} cột đầu vào; app dùng giá trị trung vị của dữ liệu huấn luyện cho các cột này. "
                        "Kết quả có thể kém tin cậy hơn: " + ", ".join(missing)
                    )
                scored = score_frame(scoring_frame)
                counts = scored["Mức ưu tiên"].value_counts()
                total = len(scored)
                red_n, yellow_n, green_n = (int(counts.get(t, 0)) for t in ("Đỏ", "Vàng", "Xanh"))

                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Tổng hồ sơ", f"{total:,}")
                m2.metric("🔴 Ưu tiên liên hệ", f"{red_n:,}", f"{red_n / total:.1%}")
                m3.metric("🟡 Cố vấn xem lại", f"{yellow_n:,}", f"{yellow_n / total:.1%}")
                m4.metric("🟢 Theo dõi định kỳ", f"{green_n:,}", f"{green_n / total:.1%}")

                left, right = st.columns([1, 1.6])
                with left:
                    st.markdown("**Phân bố mức ưu tiên**")
                    chart_data = pd.DataFrame({
                        "Số hồ sơ": [green_n, yellow_n, red_n],
                    }, index=["Xanh", "Vàng", "Đỏ"])
                    st.bar_chart(chart_data, color="#3478A8", height=230)
                with right:
                    st.markdown("**Danh sách xếp theo xác suất**")
                    selected_tiers = st.multiselect(
                        "Lọc mức ưu tiên", ["Đỏ", "Vàng", "Xanh"], default=["Đỏ", "Vàng"],
                    )
                    visible = scored[scored["Mức ưu tiên"].isin(selected_tiers)]
                    table = visible.copy()
                    table["Xác suất nghỉ học"] = table["Xác suất nghỉ học"].map(lambda p: f"{p:.1%}")
                    st.dataframe(table.head(300), use_container_width=True, hide_index=True)
                    if len(visible) > 300:
                        st.caption("Đang hiển thị 300 hồ sơ đầu; tệp tải xuống có đầy đủ kết quả.")

                # Chỉ giữ cột nhận diện nếu có, để đơn vị đối chiếu hồ sơ trong tệp kết quả.
                id_candidates = [c for c in source.columns if str(c).strip().casefold() in {
                    "student_id", "student id", "id", "mã sinh viên", "ma_sinh_vien", "masv"
                }]
                export = source[id_candidates].copy() if id_candidates else pd.DataFrame({"Dòng dữ liệu": np.arange(1, total + 1)})
                export = export.reset_index(drop=True)
                export["Thứ hạng"] = scored.set_index("Dòng dữ liệu").loc[np.arange(1, total + 1), "Thứ hạng"].to_numpy()
                export["Xác suất nghỉ học"] = predict(scoring_frame[RAW]).round(3)
                export["Mức ưu tiên"] = [tier_of(p) for p in export["Xác suất nghỉ học"]]
                export["Gợi ý"] = [ACTIONS[t][0] for t in export["Mức ưu tiên"]]
                st.download_button(
                    "⬇ Tải danh sách kết quả CSV", export.to_csv(index=False).encode("utf-8-sig"),
                    "danh_sach_uu_tien_tu_van.csv", "text/csv", use_container_width=True,
                )

                st.divider()
                st.markdown("### Xem chi tiết một hồ sơ")
                choice = st.selectbox(
                    "Chọn hồ sơ theo thứ hạng để xem yếu tố liên quan và gợi ý",
                    options=list(range(len(scored))),
                    format_func=lambda i: (
                        f"#{int(scored.iloc[i]['Thứ hạng'])} · Dòng {int(scored.iloc[i]['Dòng dữ liệu'])} · "
                        f"{scored.iloc[i]['Mức ưu tiên']} · {scored.iloc[i]['Xác suất nghỉ học']:.1%}"
                    ),
                )
                selected = scored.iloc[choice]
                source_position = int(selected["Dòng dữ liệu"]) - 1
                selected_row = scoring_frame.iloc[[source_position]][RAW]
                detail_left, detail_right = st.columns([1, 1.5])
                with detail_left:
                    st.metric("Xác suất nghỉ học", f"{selected['Xác suất nghỉ học']:.1%}")
                    risk_badge(selected["Mức ưu tiên"])
                    st.markdown("**Gợi ý cho cố vấn**")
                    for action in ACTIONS[selected["Mức ưu tiên"]]:
                        st.markdown(f"- {action}")
                with detail_right:
                    st.markdown("**Yếu tố liên quan theo SHAP**")
                    try:
                        detail_explanation = explain(selected_row)
                        if detail_explanation.empty:
                            st.info("Chưa có yếu tố phù hợp để hiển thị giải thích.")
                        else:
                            show_explanation(detail_explanation)
                    except Exception as exc:  # noqa: BLE001
                        st.info(f"Chưa tạo được giải thích cho hồ sơ này: {exc}")
        except Exception as exc:  # noqa: BLE001
            st.error(f"Không đọc hoặc chấm được file này. Hãy kiểm tra định dạng CSV và tên cột. Chi tiết: {exc}")


with tab_student:
    st.subheader("Đánh giá một hồ sơ")
    st.caption("Nhập dữ liệu đến hết học kỳ 1. Các trường không hiển thị dùng giá trị trung vị từ dữ liệu huấn luyện.")
    values = dict(DEFAULTS)
    personal, semester, outcome = st.columns([1, 1, 0.85])

    with personal:
        st.markdown("#### Thông tin đầu vào")
        courses = meta["choices"].get("Course", [int(DEFAULTS["Course"])])
        values["Course"] = st.selectbox(
            "Ngành học", courses,
            index=courses.index(int(DEFAULTS["Course"])) if int(DEFAULTS["Course"]) in courses else 0,
            format_func=lambda course: COURSE.get(int(course), str(course)),
            key="single_course",
        )
        values["Age at enrollment"] = st.number_input("Tuổi khi nhập học", 15, 80,
                                                       int(DEFAULTS["Age at enrollment"]), key="single_age")
        values["Gender"] = st.selectbox("Giới tính", [0, 1], index=int(DEFAULTS["Gender"]),
                                        format_func=lambda gender: "Nữ" if gender == 0 else "Nam",
                                        key="single_gender")
        values["Scholarship holder"] = int(st.checkbox("Có học bổng", value=bool(DEFAULTS["Scholarship holder"]),
                                                        key="single_scholarship"))
        values["Admission grade"] = st.number_input("Điểm đầu vào (0–200)", 0.0, 200.0,
                                                     float(DEFAULTS["Admission grade"]), key="single_admission")
        values["Previous qualification (grade)"] = st.number_input(
            "Điểm bằng cấp trước (0–200)", 0.0, 200.0,
            float(DEFAULTS["Previous qualification (grade)"]), key="single_previous_grade",
        )

    with semester:
        st.markdown("#### Kết quả học kỳ 1")
        enrolled = st.number_input("Số môn đăng ký", 0, 40,
                                   int(DEFAULTS["Curricular units 1st sem (enrolled)"]), key="single_enrolled")
        evaluations = st.number_input("Số lần đánh giá/thi", 0, 60,
                                      int(DEFAULTS["Curricular units 1st sem (evaluations)"]), key="single_evaluations")
        approved = st.number_input("Số môn đạt", 0, 40,
                                   min(int(DEFAULTS["Curricular units 1st sem (approved)"]), 40), key="single_approved")
        grade = st.number_input("Điểm trung bình kỳ 1 (0–20)", 0.0, 20.0,
                                float(DEFAULTS["Curricular units 1st sem (grade)"]), key="single_grade")
        credited = st.number_input("Môn được công nhận tín chỉ", 0, 40,
                                   int(DEFAULTS["Curricular units 1st sem (credited)"]), key="single_credited")
        no_eval = st.number_input("Môn không có đánh giá", 0, 40,
                                  int(DEFAULTS["Curricular units 1st sem (without evaluations)"]), key="single_no_eval")
        values.update({
            "Curricular units 1st sem (enrolled)": enrolled,
            "Curricular units 1st sem (evaluations)": evaluations,
            "Curricular units 1st sem (approved)": approved,
            "Curricular units 1st sem (grade)": grade,
            "Curricular units 1st sem (credited)": credited,
            "Curricular units 1st sem (without evaluations)": no_eval,
        })

    row = pd.DataFrame([values])[RAW]
    probability = float(predict(row)[0])
    tier = tier_of(probability)
    with outcome:
        st.markdown("#### Kết quả dự báo")
        st.metric("Xác suất nghỉ học", f"{probability:.1%}")
        risk_badge(tier)
        st.caption(f"Xanh < {T_LOW:.2f} · Vàng {T_LOW:.2f}–<{T_HIGH:.2f} · Đỏ ≥ {T_HIGH:.2f}")
        st.markdown("**Gợi ý cho cố vấn**")
        for action in ACTIONS[tier]:
            st.markdown(f"- {action}")
    if approved > enrolled:
        st.warning("Số môn đạt lớn hơn số môn đăng ký. Hãy kiểm tra lại hồ sơ.")

    left, right = st.columns([1.1, 1])
    with left:
        st.markdown("### Yếu tố liên quan")
        try:
            single_explanation = explain(row)
            if single_explanation.empty:
                st.info("Chưa có yếu tố phù hợp để hiển thị giải thích.")
            else:
                show_explanation(single_explanation)
        except Exception as exc:  # noqa: BLE001
            st.info(f"Chưa tạo được giải thích cho hồ sơ này: {exc}")
    with right:
        st.markdown("### Mô phỏng What-if")
        st.caption("Thử thay đổi số môn đạt kỳ 1 để xem mô hình dự đoán thế nào. Đây không phải bằng chứng nhân quả.")
        extra_passed = st.slider("Giả định đạt thêm bao nhiêu môn?", 0, max(0, enrolled - approved), 0,
                                 key="single_what_if")
        what_if = dict(values)
        what_if["Curricular units 1st sem (approved)"] = approved + extra_passed
        what_if_probability = float(predict(pd.DataFrame([what_if])[RAW])[0])
        a, b = st.columns(2)
        a.metric("Hiện tại", f"{probability:.1%}")
        b.metric("Theo giả định", f"{what_if_probability:.1%}",
                 f"{(what_if_probability - probability) * 100:+.1f} điểm %", delta_color="inverse")
        st.write(f"Mức mới: **{tier_of(what_if_probability)}**")


with tab_model:
    st.subheader("Thông tin mô hình và hướng dẫn sử dụng")
    info_a, info_b, info_c = st.columns(3)
    info_a.metric("Kịch bản", meta["scenario_label"])
    info_b.metric("Mô hình", meta["model"])
    info_c.metric("ROC-AUC trên test", f"{meta['test_auc']:.3f}")
    st.markdown("**Ngưỡng ưu tiên**")
    st.markdown(
        f"- **Đỏ:** xác suất ≥ {T_HIGH:.2f}; ưu tiên cố vấn chủ động liên hệ.\n"
        f"- **Vàng:** {T_LOW:.2f} ≤ xác suất < {T_HIGH:.2f}; cố vấn xem xét hồ sơ.\n"
        f"- **Xanh:** xác suất < {T_LOW:.2f}; theo dõi định kỳ."
    )
    cost = meta.get("cost", {})
    if cost:
        st.caption(
            f"Ngưỡng được chọn theo các giả định chi phí L={cost.get('L')}, c={cost.get('c')}, "
            f"s={cost.get('s')}; cần thay bằng số liệu có nguồn trước khi triển khai thực tế."
        )
    st.markdown("**Quy trình đề xuất cho đơn vị đào tạo**")
    st.markdown(
        "1. Cập nhật dữ liệu học tập sau khi kết thúc học kỳ 1.\n"
        "2. Tải danh sách CSV để xếp thứ tự hồ sơ cần xem xét.\n"
        "3. Cố vấn kiểm tra hồ sơ và trao đổi trực tiếp với sinh viên trước khi đề xuất hỗ trợ.\n"
        "4. Ghi nhận hình thức hỗ trợ và theo dõi kết quả ở kỳ tiếp theo."
    )
    st.markdown("**Giới hạn cần biết**")
    st.markdown(
        "- Mô hình được huấn luyện trên dữ liệu một cơ sở đào tạo ở Bồ Đào Nha; cần kiểm định lại trước khi dùng ở trường khác.\n"
        "- Xác suất là ước lượng của mô hình, không phải kết luận về năng lực hay hoàn cảnh của sinh viên.\n"
        "- What-if mô phỏng thay đổi đầu vào, không chứng minh can thiệp ngoài đời sẽ tạo tác động tương tự.\n"
        "- Chênh lệch hiệu năng giữa các nhóm cần được theo dõi; nhóm có ít hồ sơ cho kết quả kém ổn định.\n"
        "- Không dùng kết quả để từ chối quyền lợi; quyết định hỗ trợ thuộc về con người."
    )
    st.info("Theo dõi định kỳ tỷ lệ thiếu dữ liệu, phân bố đặc trưng và kết quả thực tế để phát hiện dữ liệu/mô hình suy giảm theo thời gian.")
