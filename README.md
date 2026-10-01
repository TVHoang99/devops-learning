## Lesson 5-6
1. In local
- Make the script executable:
   ```bash
   cd lesson_5-6
   docker build . -t lesson_5-6
   docker run --rm -it -p 80:8000 lesson_5-6
   ```

- Open browser and access to [http://localhost/helloworld](http://localhost/helloworld)

2. In production, access to [http://hoangtv.io.vn/helloworld](http://hoangtv.io.vn/helloworld)