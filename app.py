"""
Flask API cho Hand Sign Detection
"""
import os
import base64
import numpy as np
import cv2
from flask import Flask, request, render_template, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from src.prediction_service import PredictionService

# Khởi tạo Flask app
app = Flask(__name__)

# Cấu hình
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

# Tạo thư mục uploads nếu chưa có
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Khởi tạo prediction service
print("Đang khởi tạo Prediction Service...")
prediction_service = PredictionService(
    model_path='models/sign_model.h5',
    info_path='models/training_info.json'
)
print("Prediction Service đã sẵn sàng!")


def allowed_file(filename):
    """
    Kiểm tra file extension có hợp lệ không
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """
    Trang chủ
    """
    return render_template('index.html')


@app.route('/api/predict', methods=['POST'])
def predict():
    """
    API endpoint để nhận diện hand sign từ ảnh upload
    """
    # Kiểm tra có file trong request không
    if 'file' not in request.files:
        return jsonify({
            'success': False,
            'error': 'Không có file được gửi lên'
        }), 400

    file = request.files['file']

    # Kiểm tra có chọn file không
    if file.filename == '':
        return jsonify({
            'success': False,
            'error': 'Chưa chọn file'
        }), 400

    # Kiểm tra file extension
    if not allowed_file(file.filename):
        return jsonify({
            'success': False,
            'error': 'Định dạng file không hợp lệ. Chỉ chấp nhận: PNG, JPG, JPEG, GIF, BMP'
        }), 400

    try:
        # Lưu file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Predict
        result = prediction_service.predict(filepath)

        # Thêm đường dẫn ảnh vào kết quả
        if result['success']:
            result['image_url'] = f'/static/uploads/{filename}'

        return jsonify(result)

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Lỗi xử lý: {str(e)}'
        }), 500


@app.route('/api/classes', methods=['GET'])
def get_classes():
    """
    API endpoint để lấy danh sách tất cả classes
    """
    return jsonify({
        'success': True,
        'classes': prediction_service.get_class_names(),
        'total': len(prediction_service.get_class_names())
    })


@app.route('/api/predict_realtime', methods=['POST'])
def predict_realtime():
    """
    API endpoint để nhận diện hand sign từ webcam frame (base64 encoded)
    """
    try:
        # Lấy image data từ request
        data = request.get_json()

        if not data or 'image' not in data:
            return jsonify({
                'success': False,
                'error': 'Không có image data'
            }), 400

        # Decode base64 image
        image_data = data['image'].split(',')[1] if ',' in data['image'] else data['image']
        image_bytes = base64.b64decode(image_data)

        # Convert to numpy array
        nparr = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if frame is None:
            return jsonify({
                'success': False,
                'error': 'Không thể decode image'
            }), 400

        # Predict
        result = prediction_service.predict_from_frame(frame)

        return jsonify(result)

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Lỗi xử lý: {str(e)}'
        }), 500


@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    """
    Serve uploaded files
    """
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    print("\n" + "="*60)
    print("HAND SIGN DETECTION API")
    print("="*60)
    print(f"Model: models/sign_model.h5")
    print(f"Classes: {len(prediction_service.get_class_names())}")
    print(f"Upload folder: {app.config['UPLOAD_FOLDER']}")
    print("="*60)
    print("\nChạy tại: http://localhost:5000")
    print("Nhấn Ctrl+C để dừng\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
