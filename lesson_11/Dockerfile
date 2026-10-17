# 1. Sửa lỗi tag (Python 3.14 chưa có bản stable, khuyên dùng bản 3.11 hoặc 3.12-slim để giảm dung lượng)
FROM python:3.12-slim

# 2. Định nghĩa các biến môi trường cần thiết cho Python và Poetry
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PIP_ROOT_USER_ACTION=ignore

# Sửa chính tả từ /fasiapi thành /fastapi
WORKDIR /fastapi

# 3. Cài đặt các gói hệ thống cần thiết (nếu thư viện của bạn cần để compile gói C)
# RUN apt-get update && apt-get install -y --no-install-recommends curl gcc && rm -rf /var/lib/apt/lists/*

# 4. Sao chép các file cấu hình dependency trước để tận dụng Docker cache layer
COPY ./pyproject.toml ./poetry.lock* /fastapi/

# 5. Cài đặt Poetry và cài các dependencies của dự án (bỏ qua dev dependencies nếu chạy production)
RUN pip install --no-cache-dir poetry && \
    poetry install --no-root --only main

# 6. Sao chép mã nguồn vào sau cùng
COPY ./main.py /fastapi/main.py

# 7. Khởi chạy ứng dụng (Bỏ cờ --reload nếu chạy trên AWS Production để tối ưu hiệu năng)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
