## Lesson 12

- Build image from Dockerfile

```bash
cd nuxt-s3
docker build -t lesson_12:001 .
```

- Run image

```bash
docker run --rm -d -it --name lesson_12 -p "3000:3000" -v "$PWD:/app" lesson_12:001
```

- Check connection with localhost:

  - Check app: [http://localhost:3000](http://localhost:3000)

- Run the following command to generate .output/public folder:

```bash
docker exec lesson_12 npm run generate
```

- Upload .output/public folder to S3: create a bucket name "lesson-12-bucket"

- Setting up cloudfront:

  - Origin domain: select lesson-12-bucket

  - Default root object: index.html

- Access with cloudfront domain: [https://d2bcrvsyvtvmzi.cloudfront.net/](https://d2bcrvsyvtvmzi.cloudfront.net/)