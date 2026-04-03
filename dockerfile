# FROM apache/airflow:latest

# USER root
# RUN apt-get update && \
#     app-get -y install git && \
#     app-get clean

# USER airflow

# Tên file: Dockerfile

# Stage 1: Sử dụng image Airflow chính thức, đã được build sẵn Python và các dependencies cơ bản
# Tốt nhất là dùng tag cụ thể thay vì :latest (ví dụ: 2.8.3-python3.11)
FROM apache/airflow:latest 

# 1. Chuyển sang USER root để có quyền cài đặt packages hệ thống
# Đây là bước cần thiết vì Airflow user (default) không có quyền này
USER root

# 2. Tối ưu hóa lệnh RUN (kết hợp, sử dụng --no-install-recommends, dọn dẹp triệt để)
# Lệnh được sửa lỗi gõ sai và tối ưu hóa layer
RUN apt-get update --yes \
    && apt-get install --yes --no-install-recommends \
        git \
        # Thêm các packages hệ thống khác nếu cần (ví dụ: libpq-dev cho PostgreSQL)
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 3. Cài đặt các thư viện Python tùy chỉnh (nếu có)
# Thêm file requirements.txt vào thư mục build
# COPY requirements.txt .

# RUN pip install --upgrade pip
# RUN pip install --no-cache-dir -r requirements.txt

# 4. Trở lại USER airflow theo khuyến nghị bảo mật
# Đây là bước bắt buộc để Airflow chạy với quyền hạn thấp nhất
USER airflow