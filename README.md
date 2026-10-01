## Lesson 5-6

### 1. In Local (Development)
- Use [Dockerfile](file:///home/hoangtv/dev/devops-learning/lesson_5-6/Dockerfile) and [.env.local](file:///home/hoangtv/dev/devops-learning/lesson_5-6/.env.local) (supporting `reload=true`, self-signed SSL):
  ```bash
  cd lesson_5-6
  cp .env.local .env

  # Build image for local environment
  docker build -f Dockerfile . -t lesson_5-6:local

  # Run container with .env.local file
  docker run --rm -p "80:80" -p "443:443" lesson_5-6:local
  ```
- Access browser: [https://localhost/helloworld](https://localhost/helloworld)
---

### 2. In Production (Server / Domain `hoangtv.io.vn`)
- Use [Dockerfile.prod](file:///home/hoangtv/dev/devops-learning/lesson_5-6/Dockerfile.prod) (integrated Certbot) and [.env.prod](file:///home/hoangtv/dev/devops-learning/lesson_5-6/.env.prod) (with `reload=false`):
  ```bash
  cd lesson_5-6
  cp .env.prod .env

  # Build image for production environment
  docker build -f Dockerfile.prod . -t lesson_5-6:prod

  # Run container on VPS/Server
  docker run --rm -p "80:80" -p "443:443" -v letsencrypt_certs:/etc/letsencrypt lesson_5-6:prod
  ```
- Access browser: [https://hoangtv.io.vn/helloworld](https://hoangtv.io.vn/helloworld)