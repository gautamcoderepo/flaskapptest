Program Execution instructions:

1. Copy the entire folder to desired AWS Ec2 instance
2. Generate secret key for flask and set environment variable **flaskapptest** to the key value
3. Execute **docker build -t flaskapp_test .**
4. Execute **docker run --env flaskapptest -d -p 5000:5000 flaskapp_test:latest**
5. Application is accessible at <instance_ip>:5000  


