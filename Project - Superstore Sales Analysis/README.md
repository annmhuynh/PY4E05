
# Superstore Analysis

## Giới thiệu:
Project ứng dụng Python để xử lý dữ liệu bán hàng, trực quan hóa các chỉ số và hiển thị dashboard lên client-server bằng Flask
Pipeline minh họa:
[Raw Data] --> [Preprocessing] --> [Calculation] --> [Visualization] --> [Flask Dashboard]
 data/raw      data_process.py    calculation.py     visualization.py      dashboard.py

## Cấu trúc thư mục
project
|__ data/                           
|   |__ raw/                # folder lưu dữ liệu gốc để import vào DataFrame
|   |__ processed/          # folder lưu dữ liệu sau khi xử lý
|
|__ static/
|   |__ css/
|   |   |__ style.css       # file stylesheet cho HTML
|   |__ js/
|   |   |__ script.css      # file script cho HTML
|
|__ templates/
|   |__ base.html           # fixed header cho Dashboard
|   |__ dashboard.html      # HTML dashboard
|
|__ app.py                  # Flask entry point
|__ calculation.py          # hàm tính toán
|__ config.py               # cấu hình đường đãn, Flask settings
|__ data_process.py         # tiền xử lý dữ liệu
|__ dashboard.py            # Flask blueprint xuất dashboard ra web-client
|__ requirement.txt         # danh sách thư viện cần thiết

## Hướng dẫn
- Tạo môi trường ảo và cài đặt thư viện:
bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
pip install -r requirements.txt

- Chạy Flask app:
bash
python app.py

- Mở trình duyệt tại: http://127.0.0.1:5000/
