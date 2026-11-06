# ĐỀ CƯƠNG CHI TIẾT BÁO CÁO TIỂU LUẬN CUỐI KHÓA (OUTLINE — ĐÃ CHỈNH SỬA NGUỒN)

**Học phần:** Trí tuệ Nhân tạo Ứng dụng & Khoa học Dữ liệu  
**Đề tài dự kiến:** Hệ thống Cảnh báo Sớm Sinh viên Có Nguy cơ Nghỉ học sau Học kỳ 1 dựa trên Học máy Có giải thích (Explainable AI)  
**Tài liệu căn cứ:** `huong_dan_tieu_luan_va_rubric_cuoi_khoa.pdf`  
**Chuẩn trích dẫn:** APA 7th Edition  

> **Lưu ý chỉnh sửa:** Toàn bộ các nguồn đã được bổ sung và trích dẫn trực tiếp trong thân bài theo yêu cầu của hướng dẫn: nguồn dữ liệu gốc, tài liệu học thuật, tài liệu thư viện chính thức, và các chuẩn về đạo đức AI/fairness phải được trích dẫn cụ thể (Hướng dẫn tiểu luận, mục 3.8 và Checklist).

---

## 0. QUY CÁCH ĐỊNH DẠNG QUARTO & HỒ SƠ NỘP BÀI (10% — Trụ cột VI)

### 0.1. Cấu hình YAML Frontmatter bắt buộc (cho file `.qmd`)

```yaml
---
title: "Hệ thống cảnh báo sớm sinh viên có nguy cơ nghỉ học dựa trên học máy có giải thích"
subtitle: "Học phần Trí tuệ Nhân tạo Ứng dụng & Khoa học Dữ liệu"
author: "Nhóm XX: [Họ tên và MSSV các thành viên]"
date: "2026-11-11"
lang: vi
format:
  pdf:
    documentclass: article
    papersize: a4
    pdf-engine: xelatex
    toc: true
    toc-depth: 3
    number-sections: true
    colorlinks: true
    fontsize: 11pt
execute:
  echo: false
  warning: false
---
```

### 0.2. Quy định trình bày & Liêm chính học thuật

- **Độ dài:** Tối đa **45 trang** (không tính code/mã nguồn), ẩn code trong thân bài (`echo: false`) theo yêu cầu định dạng Quarto (Hướng dẫn tiểu luận, mục 2).
- **Bảng biểu & Hình ảnh:**
  - Hình vẽ/biểu đồ: Đánh số và đặt chú thích **phía dưới** (VD: *Hình 3.1: Phân phối trạng thái sinh viên và độ tuổi nhập học*).
  - Bảng số liệu: Đánh số và đặt tiêu đề **phía trên** (VD: *Bảng 4.1: So sánh hiệu năng các thuật toán trên kịch bản S1*).
  - Mọi biểu đồ phải đi kèm phân tích rút ra ý nghĩa nghiệp vụ/kinh doanh (Business Insights).
- **Liêm chính học thuật:** Tỷ lệ trùng lặp Turnitin $\le 20\%$. Có mục **Lời cảm ơn / Tuyên bố sử dụng AI** nêu rõ phạm vi sử dụng công cụ AI hỗ trợ (Hướng dẫn tiểu luận, mục 2.5).

---

## 3.1. TRANG BÌA & TRANG THÔNG TIN ĐẦU

1. **Trang bìa chính:** Tên trường, khoa, tên môn học, tiêu đề đề tài (Sentence case), họ tên & MSSV các thành viên, giảng viên hướng dẫn, địa danh và năm học.
2. **Lời cảm ơn & Tuyên bố sử dụng AI (Academic Integrity).**
3. **Mục lục tự động, Danh mục từ viết tắt, Danh mục bảng biểu, Danh mục hình vẽ.**

---

## PHẦN 1: GIỚI THIỆU & XÁC ĐỊNH BÀI TOÁN KINH DOANH / GIÁO DỤC (15% — Trụ cột I)

*(Áp dụng giai đoạn Empathize & Define của Design Thinking — Mục tiêu đạt mức Xuất sắc 9.0–10.0)*

### 1.1. Bối cảnh thực tiễn & Nỗi đau nghiệp vụ (Pain Points)

- **Thực trạng tại các cơ sở giáo dục đại học:** Tỷ lệ sinh viên bỏ học giữa chừng cao; trong bộ dữ liệu UCI *Predict Students' Dropout and Academic Success*, 1.421/3.630 sinh viên đã có kết quả cuối cùng thuộc nhóm Dropout, tương đương **39,1%** (Realinho et al., 2022; UCI Machine Learning Repository, 2022).
- **Bối cảnh quốc tế:** Tỷ lệ sinh viên không hoàn thành chương trình đại học là vấn đề chính sách giáo dục được theo dõi rộng rãi tại các nước OECD, với hệ quả về chi phí cá nhân, chi phí công và hiệu quả sử dụng nguồn lực đào tạo (OECD, 2023).
- **Tổn thất kinh tế & xã hội:**
  - *Đối với nhà trường:* Thất thu học phí các kỳ tiếp theo, lãng phí nguồn lực đào tạo và suất học bổng, giảm chỉ số uy tín/kiểm định chất lượng đào tạo.
  - *Đối với cố vấn học tập (CVHT) & phòng Công tác sinh viên:* Quá tải khi phải theo dõi thủ công hàng nghìn hồ sơ, phát hiện muộn khi sinh viên đã bỏ thi hoặc nghỉ học hẳn ở cuối năm 1.
  - *Đối với sinh viên:* Lãng phí thời gian, chi phí cơ hội và áp lực tài chính/tâm lý.
- **Cơ sở giải pháp:** Các hệ thống *early alert* và *learning analytics* đã được nghiên cứu như công cụ hỗ trợ phát hiện sớm sinh viên gặp khó khăn và điều phối can thiệp của cố vấn học tập (Arnold & Pistilli, 2012; Jayaprakash et al., 2014).

### 1.2. Chân dung người dùng mục tiêu (User Persona) & Bản đồ thấu cảm (Empathy Map)

- **Người dùng trực tiếp (Primary Persona):** Cố vấn học tập (CVHT) / Chuyên viên Phòng Công tác Sinh viên.
- **Người thụ hưởng (Secondary Persona):** Sinh viên năm nhất đang gặp khó khăn học tập hoặc tài chính; Ban Giám hiệu / Phòng Đào tạo.
- **Bản đồ thấu cảm (Empathy Map) của Cố vấn học tập:**
  - *Thấy gì (Says & Sees):* Danh sách điểm thi rời rạc cuối kỳ, sinh viên vắng thi không rõ lý do (`without evaluations`), không biết ưu tiên gọi cho ai trước khi thời gian hỗ trợ có hạn.
  - *Nghĩ & Cảm thấy gì (Thinks & Feels):* Lo lắng bỏ sót sinh viên thực sự cần giúp đỡ (False Negative), mệt mỏi nếu hệ thống cảnh báo tràn lan không có giải thích cụ thể (False Positive).
  - *Mong muốn (Pains & Gains):* Cần một công cụ cảnh báo sớm ngay **sau học kỳ 1 (Kịch bản S1)**, phân tầng rủi ro rõ ràng (**Đỏ / Vàng / Xanh**) và giải thích được *tại sao* sinh viên đó có nguy cơ cao để có kịch bản tư vấn phù hợp.
- **Căn cứ thiết kế:** Việc xây dựng Persona và Empathy Map bám theo giai đoạn Empathize–Define của Design Thinking; nhu cầu "cảnh báo sớm kèm giải thích" phù hợp với mục tiêu của các hệ thống early-alert trong giáo dục đại học (Arnold & Pistilli, 2012).

### 1.3. Phân loại bài toán AI & Mục tiêu SMART

- **Phân loại bài toán AI:** Kết hợp giữa **Insight** (Khai phá thông tin, giải thích yếu tố liên quan đến rủi ro nghỉ học qua XAI) và **Solution** (Hệ thống hỗ trợ ra quyết định tự động chấm điểm và phân tầng ưu tiên can thiệp sau Học kỳ 1).
- **Mục tiêu SMART:**
  - *Specific (Cụ thể):* Dự báo xác suất nghỉ học của sinh viên ngay khi kết thúc học kỳ 1 (S1 — dùng 33 đặc trưng đầu vào và kết quả kỳ 1) và chấm điểm cho 794 sinh viên đang theo học (`Enrolled`).
  - *Measurable (Đo lường được):* Đạt $ROC\text{-}AUC \ge 0.90$, $Recall \ge 90\%$ tại ngưỡng vận hành tối ưu chi phí để hạn chế tối đa việc bỏ sót sinh viên nguy cơ cao.
  - *Achievable (Khả thi):* Xây dựng quy trình chuẩn hóa và mô hình gọn nhẹ, giải thích được bằng SHAP (Lundberg & Lee, 2017).
  - *Relevant (Thực tiễn):* Can thiệp ngay đầu học kỳ 2 — thời điểm "vàng" còn khả năng cứu vãn kết quả học tập, thay vì đợi hết kỳ 2 (S2) khi sự việc đã rồi.
  - *Time-bound (Thời hạn):* Chấm điểm tức thời (< 1 giây/hồ sơ) ngay sau khi công bố điểm học kỳ 1 trên ứng dụng Web App.

### 1.4. Ước tính hiệu quả kinh tế (Estimated ROI) dựa trên Ma trận nhầm lẫn

- **Thiết lập hàm chi phí – lợi ích (Cost-Benefit Matrix):**
  - Gọi $L = 1.0$ là thiệt hại chuẩn hóa khi mất 1 sinh viên nghỉ học (học phí mất đi + chi phí tuyển sinh bù).
  - Gọi $C = 0.05$ là chi phí cố vấn liên hệ, rà soát và tư vấn cho 1 sinh viên bị gắn cờ ($TP + FP$).
  - Gọi $S = 0.30$ là xác suất can thiệp thành công giúp giữ chân sinh viên thực sự có nguy cơ ($TP$).
- **Công thức Lợi ích ròng kỳ vọng (Expected Net Benefit) và ROI:**

$$\text{Net Benefit} = TP \times (S \times L - C) - FP \times C$$

$$\text{Estimated ROI} = \frac{\text{Net Benefit}}{(TP + FP) \times C}$$

- Liên kết trực tiếp với việc tối ưu ngưỡng quyết định ($t_{low} = 0.19$ so với ngưỡng mặc định $0.50$) trong Phần 5.
- **Lưu ý học thuật:** $L, C, S$ là tham số giả định phục vụ mô phỏng bài toán quản trị; cách tiếp cận tối ưu ngưỡng theo chi phí bất đối xứng giữa FN và FP phù hợp với khung *cost-sensitive learning* (Elkan, 2001).

---

## PHẦN 2: CƠ SỞ LÝ THUYẾT & QUY TRÌNH NGHIÊN CỨU (10%)

### 2.1. Tổng quan phương pháp luận CRISP-DM

- Sơ đồ hóa 6 giai đoạn thực hiện dự án theo chuẩn **CRISP-DM** kết hợp **Design Thinking** (Chapman et al., 2000):
  1. *Business Understanding:* Xác định bài toán cảnh báo sớm cuối Học kỳ 1 (S1) & ma trận chi phí can thiệp.
  2. *Data Understanding:* Khảo sát 4.424 hồ sơ sinh viên từ bộ dữ liệu UCI (3.630 hồ sơ có nhãn cuối: Graduate/Dropout; 794 hồ sơ Enrolled) (Realinho et al., 2022).
  3. *Data Preparation:* Kiểm tra rò rỉ thời gian (Temporal Leakage giữa S0, S1, S1F, S2), tạo đặc trưng hành vi học tập kỳ 1, xây dựng Pipeline chống Data Leakage.
  4. *Modeling:* Thiết lập 3 mốc Baseline và huấn luyện 3 thuật toán (Logistic Regression, Random Forest, XGBoost) kết hợp tinh chỉnh siêu tham số bằng Optuna (Akiba et al., 2019).
  5. *Evaluation:* Đánh giá trên tập Test độc lập, tối ưu ngưỡng theo lợi ích ròng, giải thích bằng SHAP và kiểm tra tính công bằng (Fairness).
  6. *Deployment:* Đóng gói `artifacts/` và xây dựng ứng dụng tương tác bằng Streamlit (Streamlit, n.d.).

### 2.2. Khái quát các thuật toán & Công nghệ sử dụng

- **Mô hình tuyến tính có điều chuẩn — Logistic Regression (LR):** Nguyên lý hàm sigmoid, điều chuẩn $L_1/L_2$, ưu điểm về tính minh bạch, xác suất hiệu chỉnh tốt và tốc độ suy luận nhanh (scikit-learn developers, n.d.).
- **Mô hình tổ hợp cây (Tree-based Ensembles):**
  - *Random Forest (RF):* Nguyên lý Bagging và lấy mẫu đặc trưng ngẫu nhiên giảm phương sai (Breiman, 2001).
  - *XGBoost (XGB):* Nguyên lý Gradient Boosted Decision Trees, tối ưu hóa bậc hai và kiểm soát độ phức tạp của cây (Chen & Guestrin, 2016).
- **Lý do lựa chọn nhóm giải thuật:** Dữ liệu dạng bảng (tabular data) hỗn hợp biến số và biến phân loại, kích thước vừa phải (3.630 mẫu có nhãn), đòi hỏi khả năng giải thích cao (XAI) và tốc độ phản hồi thời gian thực trên Web App.
- **Cơ sở lý thuyết về SHAP (SHapley Additive exPlanations):** Giải thích đóng góp biên của từng đặc trưng vào dự báo cá nhân hóa, dựa trên giá trị Shapley trong lý thuyết trò chơi (Lundberg & Lee, 2017).

---

## PHẦN 3: KHÁM PHÁ & TIỀN XỬ LÝ DỮ LIỆU (20% — Trụ cột II)

*(Áp dụng Chương 3 EDA và Chương 4 Thống kê — Minh họa từ thư mục `figures/`)*

### 3.1. Từ điển dữ liệu (Data Dictionary) & Phân tách trạng thái nhãn

- **Nguồn gốc bộ dữ liệu:** Bộ dữ liệu học thuật chuẩn từ UCI Machine Learning Repository — *Predict Students' Dropout and Academic Success* (Realinho et al., 2022; UCI Machine Learning Repository, 2022), gồm **4.424 sinh viên** và **36 thuộc tính gốc**.
- **Chiến lược tách dữ liệu theo tình trạng nhãn:**
  - Tập có nhãn hoàn chỉnh (**3.630 hồ sơ**): Gồm `Graduate` (2.209 sinh viên — 60,9%) và `Dropout` (1.421 sinh viên — 39,1%). Dùng để chia Train/Dev (80%) và Test (20%).
  - Tập đang theo học (**794 hồ sơ `Enrolled`**): Chưa có kết quả cuối cùng, được tách riêng hoàn toàn để chấm điểm và lập danh sách can thiệp thực tế.
- **Bảng Từ điển dữ liệu:** Phân nhóm các biến theo thời điểm phát sinh thông tin:
  1. Nhóm nhân khẩu học & đầu vào lúc nhập học (`S0`: Tuổi, Giới tính, Ngành học, Điểm đầu vào, Điểm bằng cấp trước...).
  2. Nhóm kết quả học tập Học kỳ 1 (`SEM1`: Số môn đăng ký, số lần dự thi, số môn đạt, điểm trung bình kỳ 1, số môn không dự thi...).
  3. Nhóm tài chính & học bổng (`FIN`: Học bổng, Tình trạng đóng học phí `Tuition fees up to date`, Tình trạng nợ `Debtor`).
  4. Nhóm kinh tế vĩ mô (`MACRO`: Tỷ lệ thất nghiệp, lạm phát, tăng trưởng GDP — lưu ý chỉ có 9–10 giá trị rời rạc theo niên khóa).
  5. Nhóm kết quả Học kỳ 2 (`SEM2`: Chỉ dùng cho kịch bản đối sánh S2, tuyệt đối không đưa vào mô hình cảnh báo sớm S1).

### 3.2. Phân tích khám phá dữ liệu (EDA) & Rút trích Business Insights

*(Mỗi biểu đồ bắt buộc đi kèm phân tích ý nghĩa nghiệp vụ; sử dụng ngôn ngữ chuẩn xác: "có liên hệ với tình trạng nghỉ học", không quy kết nhân quả)*

- **Phân phối biến mục tiêu và độ tuổi nhập học** (Minh họa: `figures/eda_target_age.png`):
  - Kiểm tra tỷ lệ mất cân bằng lớp vừa phải (39,1% Dropout), độ lệch phải (skewness) của biến `Age at enrollment`.
  - *Business Insight:* Nhóm sinh viên nhập học ở độ tuổi lớn hơn có tỷ lệ nghỉ học cao hơn đáng kể (vướng bận công việc/gia đình), cần chính sách hỗ trợ linh hoạt.
- **Phân tích tỷ lệ nghỉ học theo các lát cắt phân loại** (Minh họa: `figures/eda_dropout_by_group.png`):
  - So sánh tỷ lệ Dropout theo Ngành học (`Course`), Giới tính (`Gender`), Học bổng (`Scholarship holder`) và Tình trạng học phí.
  - *Business Insight:* Sinh viên không có học bổng và một số ngành đặc thù có tỷ lệ rời bỏ cao vượt trội, gợi ý phân bổ nguồn lực cố vấn theo khoa/ngành.
- **Phân tích đa biến & Tiến độ học tập Học kỳ 1** (Minh họa: `figures/eda_multivariate.png`):
  - Mối quan hệ giữa số môn đăng ký, số môn đạt và điểm trung bình kỳ 1.
  - *Business Insight:* Sinh viên có tỷ lệ môn đạt kỳ 1 thấp hoặc đăng ký nhưng bỏ thi (`s1_ghost`) là tín hiệu cảnh báo sớm mạnh nhất.
- **Ma trận tương quan giữa các đặc trưng định lượng** (Minh họa: `figures/eda_correlation.png`):
  - Phát hiện hiện tượng đa cộng tuyến giữa các biến kết quả học tập kỳ 1 và kỳ 2, củng cố cơ sở cho việc sử dụng điều chuẩn và chuẩn hóa.
- **Công cụ trực quan hóa:** Các biểu đồ EDA được xây dựng bằng `pandas`, `matplotlib` và `seaborn` (pandas development team, n.d.; Hunter, 2007; Waskom, 2021).

### 3.3. Quy trình chuẩn bị dữ liệu (Data Preprocessing & Feature Engineering)

- **Kiểm tra dữ liệu khuyết thiếu, trùng lặp và ngoại lai (Outliers):**
  - Kiểm tra dòng trùng: 0 dòng trùng lặp.
  - Kiểm tra giá trị thiếu: 0 giá trị thiếu trong tập gốc; tuy nhiên vẫn tích hợp `SimpleImputer(strategy="median")` cho biến số và `most_frequent` cho biến phân loại trong Pipeline để phòng vệ khi vận hành thực tế (scikit-learn developers, n.d.).
  - Xử lý ngoại lai (IQR analysis): Không xóa tự động các giá trị ngoại lai hợp lệ về mặt nghiệp vụ (ví dụ: sinh viên lớn tuổi đi học lại hoặc sinh viên được công nhận nhiều tín chỉ); thay vào đó sử dụng **`RobustScaler`** để giảm độ nhạy với ngoại lai (scikit-learn developers, n.d.).
- **Kỹ thuật tạo biến mới (Feature Engineering) từ nghiệp vụ giáo dục** (Triển khai trong `dropout_utils.py`, hàm `add_features`):
  1. `s1_approval_rate`: Tỷ lệ số môn đạt / số môn đăng ký kỳ 1 (chuẩn hóa tiến độ học tập giữa các ngành có số môn khác nhau).
  2. `s1_eval_pass_rate`: Tỷ lệ số môn đạt / số lần tham gia đánh giá kỳ 1 (phản ánh hiệu quả thi cử).
  3. `s1_no_eval_rate`: Tỷ lệ môn không tham gia đánh giá / số môn đăng ký kỳ 1.
  4. `s1_ghost`: Biến cờ nhị phân đánh dấu sinh viên có đăng ký môn học nhưng bỏ toàn bộ kỳ thi đánh giá ở kỳ 1.
  5. `grade_gap`: Độ chênh lệch giữa điểm trúng tuyển đầu vào (`Admission grade`) và điểm bằng cấp trước (`Previous qualification grade`).
- **Mã hóa, Chuẩn hóa & Phân chia dữ liệu chống rò rỉ (Anti-Data Leakage):**
  - Chia tập có nhãn (3.630 mẫu) theo tỷ lệ **80% Dev (Train/CV) — 20% Test** bằng `StratifiedShuffleSplit` giữ nguyên tỷ lệ Dropout (scikit-learn developers, n.d.).
  - Đóng gói toàn bộ biến đổi (`ColumnTransformer`: `RobustScaler` cho biến số + `OneHotEncoder(handle_unknown="ignore")` cho biến định danh) vào trong `scikit-learn Pipeline`, chỉ `fit` trên tập Train của từng fold để tránh data leakage (scikit-learn developers, n.d.).

---

## PHẦN 4: THIẾT KẾ, HUẤN LUYỆN & TỐI ƯU MÔ HÌNH (20% — Trụ cột III)

*(Áp dụng Chương 5–10, Chương 12 — Trọng số Rubric 25%)*

### 4.1. Lựa chọn kịch bản thời điểm dự báo (Scenario Analysis: S0, S1, S1F, S2)

- So sánh 4 kịch bản thông tin theo dòng thời gian (Minh họa: `figures/scenario_comparison.png`):
  - **S0 (Lúc nhập học):** Dự báo sớm nhất nhưng thông tin học tập chưa có, hiệu năng thấp.
  - **S1 (Hết Học kỳ 1 — 33 đặc trưng):** Cân bằng tối ưu giữa độ chính xác ($ROC\text{-}AUC \approx 0.92$) và tính kịp thời để cố vấn can thiệp đầu kỳ 2, đồng thời tránh các biến tài chính dễ bị nhiễu hậu nghiệm (`Tuition fees up to date`, `Debtor`). **$\rightarrow$ Chọn S1 làm kịch bản triển khai chính.**
  - **S1F (Hết kỳ 1 + Tài chính)** và **S2 (Hết kỳ 2 + Tài chính):** Điểm cao hơn nhưng S2 quá muộn và các biến nợ học phí có nguy cơ là *hệ quả* của quyết định bỏ học (reverse causality / temporal leakage).
- **Căn cứ phương pháp luận:** Việc phân tách đặc trưng theo thời điểm thu thập để tránh leakage là nguyên tắc cốt lõi trong dự báo sớm học vụ (Kabakchieva, 2013; Miguéis et al., 2018).

### 4.2. Thiết lập các mốc mô hình cơ sở (Baseline Models)

- Thiết lập 3 mốc tham chiếu trên tập Dev (5-fold Stratified CV) ở kịch bản S1:
  1. **Dummy Classifier (Stratified/Prior):** $ROC\text{-}AUC_{CV} = 0.500$ (mốc ngẫu nhiên) (scikit-learn developers, n.d.).
  2. **Single-Feature Heuristic Rule (Luật 1 biến dựa trên `s1_approval_rate`):** $ROC\text{-}AUC_{CV} = 0.880$ (chứng minh giá trị của biến Feature Engineering mới tạo).
  3. **Logistic Regression mặc định (Default LR):** $ROC\text{-}AUC_{CV} = 0.919$.

### 4.3. Huấn luyện các mô hình nâng cao & Tinh chỉnh siêu tham số (Hyperparameter Tuning)

- Triển khai và đối sánh công bằng 3 thuật toán trên cùng 33 biến của kịch bản S1 qua **5-Fold Stratified Cross-Validation** (scikit-learn developers, n.d.):
  1. **Logistic Regression (LR)**
  2. **Random Forest (RF)** (Breiman, 2001)
  3. **XGBoost (XGB)** (Chen & Guestrin, 2016)
- **Tối ưu siêu tham số bằng Optuna** (Akiba et al., 2019) (Minh họa: `figures/optuna_history.png`):
  - Kết quả $ROC\text{-}AUC_{CV}$ sau tinh chỉnh: **LR = 0.9190**, **RF = 0.9206**, **XGB = 0.9244**.

### 4.4. Phân tích Quá khớp (Overfitting) & Quy tắc chọn mô hình triển khai cuối cùng

- **Phân tích chênh lệch Train – Validation & Learning Curves** (Minh họa: `figures/learning_curves.png`):
  - **Random Forest:** $AUC_{Train} = 0.996$ vs. $AUC_{CV} = 0.921$ ($\text{Gap} = 0.075$) $\rightarrow$ Có dấu hiệu Overfitting rõ nhất.
  - **XGBoost:** $AUC_{Train} = 0.965$ vs. $AUC_{CV} = 0.924$ ($\text{Gap} = 0.041$).
  - **Logistic Regression:** $AUC_{Train} = 0.938$ vs. $AUC_{CV} = 0.919$ ($\text{Gap} = 0.019$) $\rightarrow$ Hội tụ ổn định nhất, khoảng cách Train–Val rất nhỏ.
- **Căn cứ phân tích:** Learning Curves là công cụ chuẩn để chẩn đoán overfitting/underfitting thông qua khoảng cách giữa hiệu năng train và validation (scikit-learn developers, n.d.).
- **Quy tắc đa tiêu chí chọn mô hình cuối (`FINAL Model`):**
  - Áp dụng ngưỡng dung sai hiệu năng `AUC_TOL`: Giữ lại các mô hình có $ROC\text{-}AUC_{CV}$ nằm trong khoảng dung sai rất nhỏ so với mô hình cao nhất, sau đó xét đến mức độ chống quá khớp, độ trễ suy luận (latency), dung lượng lưu trữ (`model.joblib`) và tính minh bạch khi giải thích cho cố vấn học tập.
  - **Quyết định:** Lựa chọn **Logistic Regression (Tuned)** làm mô hình triển khai chính thức (`FINAL`).

---

## PHẦN 5: ĐÁNH GIÁ CHUYÊN SÂU, GIẢI THÍCH MÔ HÌNH & ĐẠO ĐỨC AI (20% — Trụ cột IV)

*(Trọng số Rubric 15% — Minh họa từ `figures/`)*

### 5.1. Báo cáo & Phân tích các chỉ số kỹ thuật trên tập Test độc lập

- **Kết quả đánh giá trên tập Test (726 sinh viên — giữ riêng hoàn toàn):**
  - Các chỉ số độc lập ngưỡng: **$ROC\text{-}AUC = 0.931$**, **$PR\text{-}AUC = 0.916$**.
  - **Căn cứ lựa chọn PR-AUC:** Trong bài toán phân loại nhị phân với tỷ lệ lớp mất cân bằng, PR-AUC phản ánh chính xác hơn ROC-AUC về chất lượng phân biệt trên lớp thiểu số (Saito & Rehmsmeier, 2015; Davis & Goadrich, 2006).
- **Lý giải tại sao ưu tiên Recall và PR-AUC / Net Benefit hơn Accuracy:** Trong bài toán cảnh báo sớm học vụ, chi phí của việc **bỏ sót một sinh viên có nguy cơ bỏ học (False Negative - FN)** lớn hơn rất nhiều so với chi phí cố vấn gửi email/gặp mặt nhầm một sinh viên an toàn (False Positive - FP); đây là bài toán chi phí bất đối xứng điển hình (Elkan, 2001).
- **Phân tích Ma trận nhầm lẫn (Confusion Matrix) & Tối ưu hóa ngưỡng quyết định** (Minh họa: `figures/roc_pr_netbenefit.png` và `figures/confusion_matrices.png`):
  - *Ngưỡng mặc định ($t_{high} = 0.50$):* $Recall = 78.9\%$, $Precision = 82.4\%$, gắn cờ $272/726$ sinh viên (bỏ sót tới ~21,1% sinh viên thực sự nghỉ học).
  - *Ngưỡng tối ưu lợi ích ròng ($t_{low} = 0.19$, tìm trên dự báo Out-of-Fold của tập Dev với $L=1, C=0.05, S=0.30$):* **$Recall = 94.0\%$**, **$Precision = 66.4\%$**, **$Accuracy = 79.1\%$**, gắn cờ $402/726$ sinh viên.
  - **Thiết kế cơ chế phân tầng 3 mức (Traffic-Light Triage) cho ứng dụng thực tế:**
    - **Mức Xanh ($p < 0.19$):** Theo dõi bình thường.
    - **Mức Vàng ($0.19 \le p < 0.50$):** Cố vấn xem lại hồ sơ, nhắc lịch thi và gửi tài nguyên học tập.
    - **Mức Đỏ ($p \ge 0.50$):** Ưu tiên liên hệ trực tiếp sớm, rà soát lộ trình học lại và hỗ trợ tài chính.

### 5.2. Minh bạch hóa & Giải thích mô hình (Explainable AI — XAI)

- **Giải thích toàn cục (Global Explainability — SHAP Summary Plot)** (Minh họa: `figures/shap_summary.png`):
  - Phân tích các yếu tố đóng góp lớn nhất vào điểm rủi ro: Số môn đạt kỳ 1 (`Curricular units 1st sem (approved)`), tỷ lệ môn đạt (`s1_approval_rate`), điểm trung bình kỳ 1, tuổi nhập học và ngành học.
  - **Căn cứ phương pháp:** SHAP phân bổ đóng góp của từng đặc trưng vào dự báo dựa trên giá trị Shapley (Lundberg & Lee, 2017; SHAP developers, n.d.).
- **Giải thích cục bộ cho từng sinh viên (Local Explainability trên Web App):**
  - Minh họa biểu đồ đóng góp SHAP ngang cho từng cá nhân (Xanh: yếu tố kéo giảm rủi ro; Đỏ: yếu tố đẩy tăng rủi ro).
  - *Lưu ý chuẩn mực học thuật:* Nhấn mạnh SHAP mô tả **cách mô hình sử dụng đặc trưng để dự báo**, không phải bằng chứng nhân quả ngoài đời thực (Lundberg & Lee, 2017).

### 5.3. Đạo đức AI, Thiên lệch thuật toán & Rủi ro vận hành (AI Ethics, Fairness & Risks)

- **Kiểm toán tính công bằng (Algorithmic Fairness Audit) trên các nhóm nhân khẩu học:**
  - Phân tích chênh lệch tỷ lệ gắn cờ, Recall và **False Positive Rate (FPR)** theo Giới tính và Học bổng:
    - *Theo giới tính:* Recall tương đồng (Nam $95.5\%$ vs. Nữ $92.3\%$), nhưng FPR của Nam cao hơn Nữ ($46.3\%$ so với $23.7\%$).
    - *Theo học bổng:* FPR nhóm không có học bổng là $39.1\%$ so với $13.5\%$ ở nhóm có học bổng; Recall lần lượt là $94.6\%$ và $88.5\%$.
  - Thảo luận nguyên nhân gốc rễ (Base rate thực tế khác nhau giữa các nhóm trong dữ liệu lịch sử) và giới hạn cỡ mẫu ở các phân nhóm nhỏ.
  - **Căn cứ khung phân tích:** Các chỉ số fairness (demographic parity, equalized odds, FPR parity) và nguồn gốc thiên lệch được hệ thống hóa trong Mehrabi et al. (2021) và Barocas, Hardt & Narayanan (2023).
- **Bảo mật quyền riêng tư & Nguy cơ dán nhãn tâm lý (Stigmatization Risk):**
  - Dữ liệu điểm số và tài chính của sinh viên phải được phân quyền chỉ dành cho Cố vấn học tập, không công khai danh sách rủi ro trước lớp để tránh hiệu ứng tâm lý tự kỷ ám thị (Self-fulfilling prophecy).
  - **Căn cứ chính sách:** Nguyên tắc bảo vệ dữ liệu cá nhân và quyền con người trong AI được khuyến nghị trong UNESCO Recommendation on the Ethics of Artificial Intelligence (UNESCO, 2021).
- **Cơ chế Con người trong vòng lặp (Human-in-the-Loop):**
  - Mô hình AI chỉ đóng vai trò **công cụ sàng lọc và gợi ý ưu tiên**, tuyệt đối không tự động ra quyết định kỷ luật, buộc thôi học hay cắt học bổng của sinh viên.
  - **Căn cứ:** Yêu cầu Human-in-the-loop là khuyến nghị chuẩn trong đạo đức AI ứng dụng (UNESCO, 2021; Barocas et al., 2023).

---

## PHẦN 6: SẢN PHẨM MẪU, KHẢ NĂNG ỨNG DỤNG & HƯỚNG PHÁT TRIỂN (15% — Trụ cột V)

### 6.1. Thiết kế giao diện ứng dụng mẫu (Prototype Application)

- **Kiến trúc hệ thống:** Xây dựng bằng **Streamlit** (Streamlit, n.d.), nạp mô hình từ `artifacts/model.joblib` (joblib developers, n.d.), cấu hình ngưỡng và từ điển từ `artifacts/meta.json` và nền tham chiếu SHAP từ `artifacts/background.csv`.
- **Minh họa 3 luồng kịch bản sử dụng chính trên giao diện:**
  1. **Dự báo & Giải thích 1 hồ sơ sinh viên:** Nhập thông tin cá nhân và kết quả học kỳ 1 $\rightarrow$ Hiển thị tức thời Xác suất nghỉ học (%), nhãn phân tầng **Đỏ / Vàng / Xanh**, danh sách **Gợi ý hành động cho cố vấn** và **Biểu đồ giải thích SHAP 5 yếu tố hàng đầu**.
  2. **Mô phỏng kịch bản giả định ("What-If" Simulation):** Thanh trượt cho phép cố vấn thử giả định *"Nếu sinh viên đạt thêm $k$ môn ở kỳ 1"* $\rightarrow$ Quan sát mức giảm rủi ro theo mô hình kèm cảnh báo phân biệt giữa mô phỏng mô hình và can thiệp thực tế.
  3. **Chấm điểm hàng loạt theo lô (Batch Scoring CSV):** Cho phép tải lên danh sách sinh viên (ví dụ: 794 sinh viên đang học `Enrolled`), tự động chuẩn hóa tên cột, xếp hạng mức độ rủi ro từ cao xuống thấp và xuất file `outputs/Danh_Sach_Can_Thiep.csv`.

### 6.2. Kế hoạch triển khai thực tế & Đo lường tác động (Deployment & Monitoring)

- **Quy trình tích hợp vào vận hành nhà trường:**
  - *Cuối học kỳ 1 (Tuần 1–2 sau khi có điểm):* Phòng Đào tạo xuất dữ liệu điểm kỳ 1 $\rightarrow$ Chạy Batch Scoring trên ứng dụng $\rightarrow$ Phân bổ danh sách nhóm **Đỏ** và **Vàng** về từng Cố vấn học tập.
  - *Đầu học kỳ 2:* Cố vấn học tập liên hệ tư vấn theo gợi ý và ghi nhận phản hồi.
- **Giám sát suy giảm hiệu năng mô hình (Data Drift & Model Drift):**
  - Theo dõi sự thay đổi phân phối điểm đầu vào và tỷ lệ qua môn giữa các khóa tuyển sinh mới (Population Stability Index — PSI).
  - Theo dõi hiện tượng *Feedback Loop Drift*: Khi cố vấn can thiệp thành công giúp sinh viên nhóm Đỏ không bỏ học, nhãn thực tế thay đổi; cần ghi nhận biến `Intervention_Flag` khi huấn luyện lại (retrain) mô hình hằng năm.
  - **Căn cứ lý thuyết:** Hiện tượng concept drift và các chiến lược thích ứng được hệ thống hóa trong Gama et al. (2014).

### 6.3. Hạn chế hiện tại & Hướng nghiên cứu mở rộng

- **Hạn chế:**
  - Bộ dữ liệu thuộc bối cảnh giáo dục đại học tại Bồ Đào Nha (UCI), cần hiệu chỉnh lại ngưỡng và trọng số khi áp dụng cho đại học tại Việt Nam (Realinho et al., 2022).
  - Chưa có dữ liệu hành vi theo tuần trên hệ thống LMS (tần suất đăng nhập, nộp bài tập, điểm chuyên cần giữa kỳ) để cảnh báo sớm hơn nữa (ngay tuần thứ 6–8 của học kỳ 1).
  - Tham số chi phí – lợi ích ($L, C, S$) hiện đang là giả định mô phỏng.
- **Hướng phát triển:**
  - Tích hợp dữ liệu chuỗi thời gian từ LMS và hệ thống điểm danh để xây dựng mô hình cảnh báo động theo từng tháng.
  - Thử nghiệm thực địa có đối chứng (A/B Testing / Randomized Controlled Trial) để đo lường chính xác tỷ lệ giữ chân thành công $S$.

---

## 3.8. TÀI LIỆU THAM KHẢO & PHỤ LỤC

### 1. Tài liệu tham khảo (Trích IEEE)

**Dữ liệu & bối cảnh giáo dục:**

- Realinho, V., Machado, J., Baptista, L., & Martins, M. V. (2022). *Predicting student dropout and academic success* [Data set]. UCI Machine Learning Repository. https://doi.org/10.24432/C5MC89
- OECD. (2023). *Education at a Glance 2023: OECD Indicators*. OECD Publishing. https://doi.org/10.1787/e13bef63-en
- Arnold, K. E., & Pistilli, M. D. (2012). Course signals at Purdue: Using learning analytics to increase student success. *Proceedings of the 2nd International Conference on Learning Analytics and Knowledge*, 267–270.
- Jayaprakash, S. M., Moody, E. W., Lauría, E. J. M., Regan, J. R., & Baron, J. D. (2014). Early alert of academically at-risk students: An open source analytics initiative. *Journal of Learning Analytics, 1*(1), 6–47.

**Phương pháp luận:**

- Chapman, P., Clinton, J., Kerber, R., Khabaza, T., Reinartz, T., Shearer, C., & Wirth, R. (2000). *CRISP-DM 1.0: Step-by-step data mining guide*. SPSS Inc.
- Elkan, C. (2001). The foundations of cost-sensitive learning. *Proceedings of the 17th International Joint Conference on Artificial Intelligence (IJCAI)*, 973–978.

**Mô hình máy học:**

- Breiman, L. (2001). Random forests. *Machine Learning, 45*(1), 5–32. https://doi.org/10.1023/A:1010933404324
- Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting system. *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*, 785–794. https://doi.org/10.1145/2939672.2939785
- scikit-learn developers. (n.d.). *scikit-learn user guide*. https://scikit-learn.org/stable/user_guide.html

**Tối ưu siêu tham số:**

- Akiba, T., Sano, S., Yanase, T., Ohta, T., & Koyama, M. (2019). Optuna: A next-generation hyperparameter optimization framework. *Proceedings of the 25th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining*, 2623–2631. https://doi.org/10.1145/3292500.3330701

**Đánh giá mô hình:**

- Saito, T., & Rehmsmeier, M. (2015). The precision-recall plot is more informative than the ROC plot when evaluating binary classifiers on imbalanced datasets. *PLOS ONE, 10*(3), e0118432. https://doi.org/10.1371/journal.pone.0118432
- Davis, J., & Goadrich, M. (2006). The relationship between precision-recall and ROC curves. *Proceedings of the 23rd International Conference on Machine Learning (ICML)*, 233–240.

**Explainable AI (XAI):**

- Lundberg, S. M., & Lee, S.-I. (2017). A unified approach to interpreting model predictions. *Advances in Neural Information Processing Systems, 30* (NeurIPS 2017).
- SHAP developers. (n.d.). *SHAP documentation*. https://shap.readthedocs.io/

**Đạo đức AI & Fairness:**

- Mehrabi, N., Morstatter, F., Saxena, N., Lerman, K., & Galstyan, A. (2021). A survey on bias and fairness in machine learning. *ACM Computing Surveys, 54*(6), 1–35. https://doi.org/10.1145/3457607
- Barocas, S., Hardt, M., & Narayanan, A. (2023). *Fairness and machine learning: Limitations and opportunities*. MIT Press.
- UNESCO. (2021). *Recommendation on the ethics of artificial intelligence*. UNESCO.

**Vận hành & Monitoring:**

- Gama, J., Žliobaitė, I., Bifet, A., Pechenizkiy, M., & Bouchachia, A. (2014). A survey on concept drift adaptation. *ACM Computing Surveys, 46*(4), 1–37. https://doi.org/10.1145/2523813
- Streamlit. (n.d.). *Streamlit documentation*. https://docs.streamlit.io/
- joblib developers. (n.d.). *joblib documentation*. https://joblib.readthedocs.io/

**Thư viện trực quan hóa:**

- pandas development team. (n.d.). *pandas documentation*. https://pandas.pydata.org/docs/
- Hunter, J. D. (2007). Matplotlib: A 2D graphics environment. *Computing in Science & Engineering, 9*(3), 90–95.
- Waskom, M. L. (2021). seaborn: Statistical data visualization. *Journal of Open Source Software, 6*(60), 3021.

### 2. Phụ lục

- **Phụ lục A:** Bảng giải thích chi tiết 36 thuộc tính gốc của bộ dữ liệu UCI và các biến kỹ thuật tạo mới (nguồn: Realinho et al., 2022).
- **Phụ lục B:** Bảng kết quả tìm kiếm siêu tham số Optuna và bảng đối sánh tài nguyên (thời gian huấn luyện, độ trễ dự báo, kích thước mô hình).
- **Phụ lục C:** Ảnh chụp màn hình giao diện ứng dụng Streamlit (`app.py`) và đường dẫn Video Demo / Web App.

---

## DANH MỤC KIỂM TRA TRƯỚC KHI NỘP BÀI (CHECKLIST BẮT BUỘC)

- [ ] File nguồn Quarto `.qmd` có đúng YAML Frontmatter và biên dịch thành công sang `.pdf` (`quarto render <file>.qmd --to pdf`).
- [ ] Độ dài báo cáo $\le 45$ trang (không tính code), đã bật `echo: false` để ẩn code trong thân bài.
- [ ] Có đầy đủ Trang bìa, Bảng phân công nhiệm vụ & tỷ lệ đóng góp (%), Lời tuyên bố sử dụng AI và Mục lục tự động.
- [ ] Toàn bộ 10 biểu đồ trong `figures/` và các bảng số liệu đều có tiêu đề, đánh số thứ tự đúng quy định và có đoạn phân tích Business Insights đi kèm.
- [ ] **[MỚI]** Mọi con số, khẳng định phương pháp và kết quả đều có trích dẫn nguồn trong thân bài (không chỉ ở danh mục cuối).
- [ ] **[MỚI]** Đã trích dẫn nguồn dữ liệu gốc UCI (DOI) ngay tại phần mô tả dữ liệu (Phần 3.1).
- [ ] **[MỚI]** Đã trích dẫn tài liệu chính thức của các thư viện sử dụng: scikit-learn, SHAP, Optuna, Streamlit, joblib, pandas, matplotlib, seaborn.
- [ ] **[MỚI]** Đã trích dẫn nguồn học thuật cho từng nhóm phương pháp: CRISP-DM, Random Forest, XGBoost, PR-AUC, fairness, concept drift.
- [ ] Notebook `SIC_UCI_DropStudent_out.ipynb` đã chạy `Restart & Run All` sạch sẽ không lỗi, khớp hoàn toàn số liệu với báo cáo.
- [ ] Đính kèm link chạy thử Web App (`app.py`) hoặc video demo 2–3 phút trong thư mục `demo/`.
- [ ] Đóng gói file nén theo đúng cú pháp: `[Nhom_XX]_[MaDeTai]_[TenDeTai].zip` gồm: `.qmd`, `.pdf`, `code/`, `data/`, `demo/` và nộp trước **23:59 ngày 11/11/2026**.
