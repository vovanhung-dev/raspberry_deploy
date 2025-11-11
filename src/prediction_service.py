"""
Service để nhận diện hand sign từ hình ảnh
"""
import os
import json
import numpy as np
import cv2
from tensorflow import keras


class PredictionService:
    def __init__(self, model_path='models/sign_model.h5', info_path='models/training_info.json'):
        """
        Khởi tạo service với model và class names
        """
        # Load model
        self.model = keras.models.load_model(model_path)
        print(f"Model loaded from {model_path}")

        # Load class names
        if os.path.exists(info_path):
            with open(info_path, 'r') as f:
                info = json.load(f)
                self.class_names = info['class_names']
        else:
            # Fallback: Tạo default class names
            self.class_names = [chr(i) for i in range(65, 91)]  # A-Z
            self.class_names.extend(['del', 'nothing', 'space'])

        print(f"Loaded {len(self.class_names)} classes")

        # Kích thước ảnh đầu vào model
        self.img_size = 64

    def preprocess_image(self, image_path):
        """
        Tiền xử lý ảnh trước khi predict

        Args:
            image_path: Đường dẫn đến file ảnh

        Returns:
            numpy array đã được chuẩn hóa
        """
        # Đọc ảnh
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Không thể đọc ảnh: {image_path}")

        # Convert BGR to RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Resize về kích thước model
        img = cv2.resize(img, (self.img_size, self.img_size))

        # Chuẩn hóa pixel values về [0, 1]
        img = img.astype('float32') / 255.0

        # Thêm batch dimension
        img = np.expand_dims(img, axis=0)

        return img

    def predict(self, image_path):
        """
        Nhận diện hand sign từ ảnh

        Args:
            image_path: Đường dẫn đến file ảnh

        Returns:
            dict chứa kết quả prediction
        """
        try:
            # Tiền xử lý ảnh
            processed_img = self.preprocess_image(image_path)

            # Predict
            predictions = self.model.predict(processed_img, verbose=0)

            # Lấy class có confidence cao nhất
            predicted_class_idx = np.argmax(predictions[0])
            confidence = float(predictions[0][predicted_class_idx])
            predicted_class = self.class_names[predicted_class_idx]

            # Lấy top 5 predictions
            top5_indices = np.argsort(predictions[0])[-5:][::-1]
            top5_predictions = []
            for idx in top5_indices:
                top5_predictions.append({
                    'class': self.class_names[idx],
                    'confidence': float(predictions[0][idx])
                })

            return {
                'success': True,
                'predicted_class': predicted_class,
                'confidence': confidence,
                'top5_predictions': top5_predictions
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def predict_from_frame(self, frame):
        """
        Nhận diện hand sign từ frame numpy array (từ webcam)

        Args:
            frame: numpy array BGR format từ webcam

        Returns:
            dict chứa kết quả prediction
        """
        try:
            # Convert BGR to RGB
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Resize về kích thước model
            img = cv2.resize(img, (self.img_size, self.img_size))

            # Chuẩn hóa pixel values về [0, 1]
            img = img.astype('float32') / 255.0

            # Thêm batch dimension
            img = np.expand_dims(img, axis=0)

            # Predict
            predictions = self.model.predict(img, verbose=0)

            # Lấy class có confidence cao nhất
            predicted_class_idx = np.argmax(predictions[0])
            confidence = float(predictions[0][predicted_class_idx])
            predicted_class = self.class_names[predicted_class_idx]

            # Lấy top 5 predictions
            top5_indices = np.argsort(predictions[0])[-5:][::-1]
            top5_predictions = []
            for idx in top5_indices:
                top5_predictions.append({
                    'class': self.class_names[idx],
                    'confidence': float(predictions[0][idx])
                })

            return {
                'success': True,
                'predicted_class': predicted_class,
                'confidence': confidence,
                'top5_predictions': top5_predictions
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def get_class_names(self):
        """
        Lấy danh sách tất cả class names
        """
        return self.class_names
