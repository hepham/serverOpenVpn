# Dockerfile
FROM python:3.9-slim

# Thiết lập thư mục làm việc
WORKDIR /app

# Sao chép tệp yêu cầu vào container
COPY requirements.txt .

# Cài đặt các thư viện cần thiết
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép mã nguồn vào container
COPY . .

# Mở cổng cho ứng dụng
EXPOSE 5000

# Chạy ứng dụng
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]