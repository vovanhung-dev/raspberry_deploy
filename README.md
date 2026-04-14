# Raspberry Deploy - Nhận Diện Ký Hiệu Tay

## Danh Mục

`Machine Learning` `IoT`

## Giới Thiệu

Ứng dụng web nhận diện ký hiệu tay (hand sign detection) chạy trên Raspberry Pi 5, sử dụng TensorFlow và OpenCV với giao diện Flask.

## Chức Năng

- Nhận diện ký hiệu tay qua camera
- Giao diện web Flask
- Model TensorFlow / TensorFlow Lite
- Tối ưu cho Raspberry Pi 5
- Script cài đặt và chạy tự động

## Công Nghệ Sử Dụng

- **AI/ML:** TensorFlow, TensorFlow Lite
- **Computer Vision:** OpenCV
- **Web Framework:** Flask
- **Ngôn ngữ:** Python
- **Hardware:** Raspberry Pi 5

## Yêu Cầu Hệ Thống

- Raspberry Pi 5 (hoặc máy tính có camera)
- Python >= 3.8

## Cài Đặt

```bash
# Trên Raspberry Pi
chmod +x install.sh
./install.sh

# Hoặc thủ công
pip install -r requirements.txt
```

## Chạy Ứng Dụng

```bash
chmod +x run.sh
./run.sh

# Hoặc
python app.py
```
