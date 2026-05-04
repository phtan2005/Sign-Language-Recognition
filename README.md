# 🤟 Real-time Sign Language Recognition & Quiz Game (YOLOv11)

Ứng dụng nhận diện ngôn ngữ ký hiệu (Sign Language) theo thời gian thực sử dụng mô hình YOLOv11. Không chỉ dừng lại ở việc nhận diện ký tự đơn lẻ, hệ thống còn tích hợp Word Builder (ghép từ) và Quiz Mode (trò chơi trắc nghiệm), giúp việc học trở nên trực quan, sinh động và mang tính tương tác cao.

---

## ✨ Tính năng nổi bật

### ⚡ Real-time Inference
- Nhận diện ký hiệu tay theo thời gian thực
- Sử dụng YOLOv11 + PyTorch (CUDA / FP16)
- Tốc độ xử lý cao

### 🛡️ Temporal Smoothing
- Giảm nhiễu (flickering)
- Sử dụng deque + voting
- Giữ kết quả ổn định

### 📝 Word Builder
- Ghép chữ thành từ
- Lưu lịch sử vào word_history.json
- Quản lý session, chỉnh sửa từ

### 🎮 Quiz Mode
- 3 mức độ: Easy / Normal / Hard
- Tính điểm, combo streak
- Rank: S / A / B / C / D

### 🖥️ HUD trực quan
- Hiển thị FPS, progress bar
- Overlay bằng OpenCV

---

## 🛠️ Cài đặt

```bash
pip install ultralytics opencv-python torch torchvision
```

---

## 🚀 Chạy chương trình

```bash
git clone https://github.com/phtan2005/sign-language-yolov11.git
cd sign-language-yolov11
python realtime_detect.py
```

---

## ⌨️ Phím điều khiển

### Word Builder Mode
- M: Đổi chế độ
- SPACE: Hoàn thành từ
- S: Lưu từ
- BACKSPACE: Xóa ký tự
- C: Xóa toàn bộ
- G: Vào Quiz
- Q: Thoát

### Quiz Mode
- 1/2/3: Chọn độ khó
- SPACE: Skip
- R: Chơi lại
- G: Thoát Quiz

---

## ⚙️ Cấu hình

```python
MODEL_PATH = "best.pt"
CONF_THRESH = 0.55
SMOOTH_WINDOW = 5
QUIZ_QUESTIONS = 10
```

---

## 👨‍💻 Tác giả

Phạm Huỳnh Tấn  
Sinh viên AI - Đại học Văn Lang  
GitHub: https://github.com/phtan2005
