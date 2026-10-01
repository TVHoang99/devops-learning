## Lesson 5-6

### 1. In Local (Development)
- Sử dụng [Dockerfile](file:///home/hoangtv/dev/devops-learning/lesson_5-6/Dockerfile) và [.env.local](file:///home/hoangtv/dev/devops-learning/lesson_5-6/.env.local) (hỗ trợ `reload=true`, self-signed SSL):
  ```bash
  cd lesson_5-6
  # Build image for local environment
  docker build -f Dockerfile -t lesson_5-6:local .

  # Run container with .env.local file
  docker run --rm -it --env-file .env.local -p 443:8000 lesson_5-6:local
  ```
- Access browser: [https://localhost/helloworld](https://localhost/helloworld) *(or 8443 if mapping `-p 8443:8000`)*.

---

### 2. In Production (Server / Domain `hoangtv.io.vn`)
- Use [Dockerfile.prod](file:///home/hoangtv/dev/devops-learning/lesson_5-6/Dockerfile.prod) (integrated Certbot) and [.env.prod](file:///home/hoangtv/dev/devops-learning/lesson_5-6/.env.prod) (with `reload=false`):
  ```bash
  cd lesson_5-6
  # Build image for production environment
  docker build -f Dockerfile.prod -t lesson_5-6:prod .

  # Run container on VPS/Server
  docker run --rm -it --env-file .env.prod \
    -p 80:80 \
    -p 443:8000 \
    -v letsencrypt_certs:/etc/letsencrypt \
    lesson_5-6:prod
  ```
- Access browser: **[https://hoangtv.io.vn/helloworld](https://hoangtv.io.vn/helloworld)** (SSL certificate from Let's Encrypt).
- *Note:* Open port 80 for Certbot to verify HTTP-01 challenge from Let's Encrypt when issuing the certificate for the first time. The `/etc/letsencrypt` directory is persisted through Docker volume.