Program Execution instructions:

1. Copy the entire folder to desired AWS Ec2 instance
3. Execute **docker build -t flaskapp_test .**
4. Execute **docker run -d -p 5000:5000 flaskapp_test:latest**
5. Application is accessible at <instance_ip>:5000  


<b>Flask Endpoints</b> <br/>
'/' - Homepage where you upload the csv <br/>
if csv is invalid it will internally render page 404.html <br/>
if csv is valid you will be able to download the json <br/>

