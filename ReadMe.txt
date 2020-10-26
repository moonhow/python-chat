Introduction
------------
This project is consists of 
1. Serverless functions deployed to AWS as Lambda functions & exposed as WebSocket API, at wss://jbhdr7m2o0.execute-api.ap-southeast-1.amazonaws.com/dev
2. A Chat CLI client which accept the first argument as username.

Run Python-Chat Client (Python3)
--------------------------------
1. Go to client folder.
2. Run "pipenv install" to install all dependencies.
2. Run "pipenv run python main.py [username]"

Test AWS WebSocket API using wscat
----------------------------------
1. Run "npm install wscat" to install wscat tool.
2. Run "wscat -c wss://jbhdr7m2o0.execute-api.ap-southeast-1.amazonaws.com/dev?username=moonhow"
3. Run "{"action":"onMessage", "data":"hello world"}" to pass the message.

Unit Test
---------
1. This project is yet to be extended with unit testing by using either unittest, nose2 or pytest library. 
2. As the interaction with AWS infrastructure is implemented with boto3, we'll need a library (such as moto) to mock the requests to AWS services (such as DynamoDB). Please refer to https://blog.codecentric.de/en/2020/01/testing-aws-python-code-with-moto/.
