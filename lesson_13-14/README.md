# Deploy Python AWS Lambda with DynamoDB

## Goal

Deploy a Python AWS Lambda function connected to DynamoDB and expose a
`GET /users` API through Amazon API Gateway.

## Configuration

  Component            Value
  -------------------- --------------------
  Runtime              Python 3.12
  Lambda function      `get-users`
  Memory               `1024 MB` (1 GB)
  Timeout              `30 seconds`
  DynamoDB table       `Users`
  Partition key        `user_id` (String)
  API type             HTTP API
  Method               `GET`
  Route                `/users`
  Example AWS Region   `ap-northeast-1`

## Steps

### 1. Create the DynamoDB table

1.  Open the [DynamoDB
    Console](https://console.aws.amazon.com/dynamodbv2/).
2.  Select the AWS Region.
3.  Go to **Tables** → **Create table**.
4.  Set the table name to `Users`.
5.  Set the partition key to `user_id` with type `String`.
6.  Create the table.
7.  Open **Explore table items**.
8.  Add these sample items:

``` json
{
  "user_id": "user-001",
  "name": "Nguyen Van A",
  "email": "a@example.com",
  "age": 25
}
```

``` json
{
  "user_id": "user-002",
  "name": "Tran Thi B",
  "email": "b@example.com",
  "age": 28
}
```

``` json
{
  "user_id": "user-003",
  "name": "Le Van C",
  "email": "c@example.com",
  "age": 30
}
```

### 2. Create the IAM role

1.  Open the [IAM Console](https://console.aws.amazon.com/iam/).
2.  Go to **Roles** → **Create role**.
3.  Select **AWS service** as the trusted entity.
4.  Select **Lambda** as the use case.
5.  Attach the `AWSLambdaBasicExecutionRole` policy.
6.  Create the role named `lambda-dynamodb-users-role`.
7.  Open the new role.
8.  Select **Add permissions** → **Create inline policy**.
9.  Select the JSON editor and add the following policy. Replace
    `YOUR_ACCOUNT_ID` with your AWS account ID.

``` json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:Scan"
      ],
      "Resource": "arn:aws:dynamodb:ap-northeast-1:YOUR_ACCOUNT_ID:table/Users"
    }
  ]
}
```

10. Name the policy `LambdaUsersDynamoDBAccess`.
11. Create the policy.

### 3. Create the Lambda function

1.  Open the [Lambda Console](https://console.aws.amazon.com/lambda/).
2.  Select **Create function** → **Author from scratch**.
3.  Set the function name to `get-users`.
4.  Select runtime `Python 3.12`.
5.  Select architecture `x86_64`.
6.  Select **Use an existing role**.
7.  Choose `lambda-dynamodb-users-role`.
8.  Create the function.

### 4. Add the Lambda code

1.  Open the `get-users` function.
2.  Go to the **Code** tab.
3.  Open `lambda_function.py`.
4.  Replace the file contents with:

``` python
import json
import os
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def lambda_handler(event, context):
    try:
        response = table.scan()
        users = response.get("Items", [])

        while "LastEvaluatedKey" in response:
            response = table.scan(
                ExclusiveStartKey=response["LastEvaluatedKey"]
            )
            users.extend(response.get("Items", []))

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "success": True,
                "total": len(users),
                "data": users
            }, default=str)
        }

    except Exception as e:
        print(f"Error: {str(e)}")

        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "success": False,
                "message": "Internal server error"
            })
        }
```

5.  Select **Deploy**.

### 5. Configure Lambda environment variables

1.  Open **Configuration** → **Environment variables**.
2.  Select **Edit** → **Add environment variable**.
3.  Set `TABLE_NAME` to `Users`.
4.  Save the changes.

### 6. Configure Lambda memory and timeout

1.  Open **Configuration** → **General configuration**.
2.  Select **Edit**.
3.  Set Memory to `1024 MB`.
4.  Set Timeout to `30 seconds`.
5.  Save the changes.

### 7. Test the Lambda function

1.  Open the **Test** tab.
2.  Create a test event.
3.  Use an empty JSON event:

``` json
{}
```

4.  Save the test event.
5.  Select **Test**.
6.  Verify that the response has `statusCode: 200` and returns the three
    sample users.

### 8. Create the API Gateway HTTP API

1.  Open the [API Gateway
    Console](https://console.aws.amazon.com/apigateway/).
2.  Select **Create API**.
3.  Under **HTTP API**, select **Build**.
4.  Add a Lambda integration.
5.  Select the AWS Region.
6.  Select the Lambda function `get-users`.
7.  Set the API name to `users-api`.
8.  Create the route:
    -   Method: `GET`
    -   Resource path: `/users`
    -   Integration target: `get-users`
9.  Set the stage name to `$default`.
10. Enable **Auto-deploy**.
11. Create the API.

### 9. Get the API endpoint

1.  Open the `users-api` API.
2.  Find and copy the **Invoke URL**.
3.  Append `/users` to the Invoke URL.

Endpoint format:

``` text
https://YOUR_API_ID.execute-api.ap-northeast-1.amazonaws.com/users
```

### 10. Test the API

**Using curl:**

``` bash
curl -i https://YOUR_API_ID.execute-api.ap-northeast-1.amazonaws.com/users
```

**Using Postman:**

1.  Create a new request.
2.  Select method `GET`.
3.  Enter the API endpoint.
4.  Select **Send**.
5.  Verify that the response returns HTTP `200` and the users data.

## Completion checklist

-   [ ] Create DynamoDB table `Users`.
-   [ ] Add sample users.
-   [ ] Create IAM role and attach the required policies.
-   [ ] Create Lambda function `get-users`.
-   [ ] Deploy the Python code.
-   [ ] Set `TABLE_NAME=Users`.
-   [ ] Set Lambda memory to `1024 MB`.
-   [ ] Set Lambda timeout to `30 seconds`.
-   [ ] Test the Lambda function.
-   [ ] Create API Gateway HTTP API.
-   [ ] Configure `GET /users`.
-   [ ] Test the API with Postman or curl.

## Cleanup

To avoid ongoing charges, delete the lab resources when they are no
longer needed:

1.  Delete the API Gateway API `users-api`.
2.  Delete the Lambda function `get-users`.
3.  Delete the DynamoDB table `Users`.
4.  Delete the IAM role `lambda-dynamodb-users-role` if it is not used
    by other workloads.

## AWS Documentation

-   [AWS
    Lambda](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)
-   [Lambda memory
    configuration](https://docs.aws.amazon.com/lambda/latest/dg/configuration-memory.html)
-   [Lambda with
    DynamoDB](https://docs.aws.amazon.com/lambda/latest/dg/with-ddb.html)
-   [DynamoDB Scan
    API](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_Scan.html)
-   [API Gateway HTTP API Lambda
    integration](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html)
-   [Lambda execution
    roles](https://docs.aws.amazon.com/lambda/latest/dg/lambda-intro-execution-role.html)
