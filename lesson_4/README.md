1. Make the script executable:
   ```bash
   chmod +x health_check.sh
   ```

2. Run the script:
   ```bash
   ./health_check.sh
   ```

3. Add Dockerfile and create a new python script 'main.py'. Then run the following script
   ```bash
   docker build . -t test-dockerfile
   docker run --rm -it test-dockerfile
   ```