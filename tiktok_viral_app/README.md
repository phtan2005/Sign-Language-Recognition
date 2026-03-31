# 🎵 TikTok Viral Detector — Streamlit App

Ứng dụng phát hiện video TikTok có Viral hay không dựa trên
Weighted Engagement Rate, sử dụng model Random Forest đã train trên 10M videos.

---

## 📁 Cấu trúc thư mục

```
tiktok_viral_app/
├── app.py               ← File chính Streamlit
├── model_config.json    ← Threshold P80 + metrics từ Colab
├── requirements.txt     ← Thư viện cần cài
└── README.md
```

---

## ⚙️ Cách chạy trên VS Code (lần đầu)

### Bước 1 — Mở thư mục trong VS Code
```
File → Open Folder → chọn thư mục tiktok_viral_app
```

### Bước 2 — Mở Terminal trong VS Code
```
Terminal → New Terminal  (hoặc Ctrl + `)
```

### Bước 3 — Tạo môi trường ảo (khuyến nghị)
```bash
python -m venv venv
```

Kích hoạt môi trường ảo:
- Windows:   `venv\Scripts\activate`
- Mac/Linux: `source venv/bin/activate`

### Bước 4 — Cài thư viện
```bash
pip install -r requirements.txt
```

### Bước 5 — Cập nhật model_config.json
Mở file `model_config.json` và cập nhật 2 trường:

```json
{
  "p80_threshold": 6.0,   ← Thay bằng giá trị p80_threshold thực tế từ Colab
  "metrics": {
    "auc_roc": 0.9123,    ← Thay bằng kết quả thực tế từ Cell 5.5 trong Colab
    "accuracy": 0.8876,
    "f1_score": 0.8901
  }
}
```

> Giá trị p80_threshold được in ra ở **Cell 4.2** trong Colab notebook
> (dòng: `📍 Ngưỡng P80 (Viral threshold): X.XXXX%`)

### Bước 6 — Chạy app
```bash
streamlit run app.py
```

Trình duyệt sẽ tự mở tại: **http://localhost:8501**

---

## 🔁 Lần sau muốn chạy lại

```bash
# Mở VS Code Terminal, kích hoạt venv rồi chạy:
venv\Scripts\activate      # Windows
streamlit run app.py
```

---

## 🧮 Công thức tính Viral

```
Weighted Engagement = (Likes × 1) + (Comments × 1.5) + (Shares × 2)
Engagement Rate (%) = Weighted Engagement / Views × 100

Viral (1)      → ER ≥ P80 threshold  (Top 20%)
Non-Viral (0)  → ER < P80 threshold  (80% còn lại)
```

---

## 📊 Dataset

- **Nguồn:** [The-data-company/TikTok-10M](https://huggingface.co/datasets/The-data-company/TikTok-10M)
- **Kích thước:** ~1.87 GB · ~10 triệu rows · Parquet format
- **Model:** Random Forest Classifier (Spark MLlib) · 100 trees · depth=10
