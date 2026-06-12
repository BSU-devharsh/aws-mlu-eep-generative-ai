---
title: "Appendix: A Free Serverless Backend (Lambda + DynamoDB)"
---

# Appendix: Building a Free Serverless Backend with AWS Lambda and DynamoDB

The generative-AI applications in this book often need a small backend, somewhere
to store data and an HTTP endpoint to call. This appendix shows how to build a
fully functional, zero-cost backend with **AWS Lambda** (compute) and **Amazon
DynamoDB** (a NoSQL database), both of which have generous "Always Free" tiers.
It is a self-contained tutorial you can adapt for chatbots, RAG metadata stores,
or any small API.

```{admonition} Verify Free Tier terms before you build
:class: warning
AWS Free Tier terms, service limits, and console layouts change over time, and
newer AWS accounts may be under a different Free Tier model than older ones.
Treat the numbers below as a guide and confirm the current limits on the
[AWS Free Tier page](https://aws.amazon.com/free/) and each service's pricing page
before relying on "free." Always set a billing alarm.
```

## The Always Free allowances (typical)

These allowances have historically reset every month, indefinitely:

- **AWS Lambda:** ~1 million free requests and 400,000 GB-seconds of compute per
  month.
- **Amazon DynamoDB:** 25 GB of storage, plus enough provisioned capacity (25 Write
  Capacity Units and 25 Read Capacity Units) to handle roughly 40 million requests
  per month.

Staying at or below those capacity units is what keeps the project free. We will
build a **serverless TODO API** to demonstrate.

## Step 1: Create the DynamoDB table

1. Sign in to the **AWS Management Console**.
2. Open **DynamoDB** and click **Create table**.
3. Configure:
   - **Table name:** `TodoTable`
   - **Partition key:** `id` (type **String**)
4. Under **Table settings**, choose **Customize settings** (not Default).
5. Set **Capacity mode** to **Provisioned**.
6. Set both **Read capacity units (RCU)** and **Write capacity units (WCU)** to
   `5`. (Staying at or below 25 keeps you in the Always Free tier.)
7. Click **Create table**.

## Step 2: Create an IAM role for Lambda

AWS resources cannot talk to each other without explicit permissions, so your
Lambda function needs an execution role.

1. Open the **IAM** console, go to **Roles**, and click **Create role**.
2. Trusted entity type: **AWS service**; use case: **Lambda**. Click **Next**.
3. Attach the managed policy **`AmazonDynamoDBFullAccess`** (for table access).
4. Also attach **`AWSLambdaBasicExecutionRole`** (for CloudWatch logging). Click
   **Next**.
5. Name the role `LambdaTodoRole` and click **Create role**.

```{admonition} Least privilege in production
:class: tip
`AmazonDynamoDBFullAccess` is convenient for learning but broad. For real systems,
scope the policy down to only the actions and the single table this function needs
(`dynamodb:PutItem`, `dynamodb:Scan`/`Query` on `TodoTable`), consistent with the
responsible-AI and security practices in Module 2.
```

## Step 3: Write the Lambda function

1. Open the **AWS Lambda** console and click **Create function**.
2. Choose **Author from scratch** and configure:
   - **Function name:** `TodoHandler`
   - **Runtime:** Python 3.12 (or your preferred language)
   - **Permissions:** choose **Use an existing role** and select `LambdaTodoRole`.
3. Click **Create function**.
4. In the code editor, replace the placeholder with this handler, then click
   **Deploy**:

```python
import json
import boto3
import uuid

# Initialize the DynamoDB client outside the handler for reuse across invocations.
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("TodoTable")


def lambda_handler(event, context):
    try:
        # Extract the HTTP method (Lambda Function URL event shape).
        http_method = event.get("requestContext", {}).get("http", {}).get("method", "GET")

        # 1. CREATE (POST)
        if http_method == "POST":
            body = json.loads(event.get("body", "{}"))
            todo_id = str(uuid.uuid4())
            item = {
                "id": todo_id,
                "task": body.get("task", "Untitled Task"),
                "completed": False,
            }
            table.put_item(Item=item)
            return response(201, item)

        # 2. READ ALL (GET)
        elif http_method == "GET":
            scan_result = table.scan()
            return response(200, scan_result.get("Items", []))

        return response(400, {"error": "Unsupported HTTP method"})

    except Exception as e:
        return response(500, {"error": str(e)})


def response(status_code, body_content):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",  # needed for browser (CORS) calls
        },
        "body": json.dumps(body_content),
    }
```

## Step 4: Expose a free Function URL

Instead of API Gateway, use a built-in **Lambda Function URL**, which is included
in Lambda's free allocation.

1. In the `TodoHandler` function, open the **Configuration** tab.
2. Select **Function URL** and click **Create function URL**.
3. Set **Auth type** to **NONE** (publicly accessible).
4. Under **Additional settings**, enable **Configure cross-origin resource sharing
   (CORS)** so browsers can call it.
5. Click **Save** and copy the generated URL.

```{admonition} "Auth type: NONE" is public
:class: warning
A `NONE` auth Function URL is open to anyone with the link. That is fine for a
learning demo, but for anything real, use **AWS_IAM** auth (or put the function
behind API Gateway with an authorizer) and never store sensitive data in a
publicly writable endpoint.
```

## Step 5: Test it

Use `curl`, Postman, or a small web page. Replace the placeholder with your copied
Function URL.

**Insert a task (POST):**

```bash
curl -X POST https://YOUR-FUNCTION-URL.lambda-url.us-east-1.on.aws/ \
     -H "Content-Type: application/json" \
     -d '{"task": "Buy groceries"}'
```

Expected response:

```json
{"id": "some-random-uuid", "task": "Buy groceries", "completed": false}
```

**Retrieve all tasks (GET):**

```bash
curl https://YOUR-FUNCTION-URL.lambda-url.us-east-1.on.aws/
```

Expected response: a JSON array of all saved task objects.

## Essential design rules for the free tier

- **Avoid table scans on large datasets.** `table.scan()` reads the entire table
  and burns Read Capacity Units. For production, use `table.query()` with a
  partition key (and global secondary indexes for other access patterns) so you
  read only what you need.
- **Keep items small.** DynamoDB caps each item at **400 KB**. It is built for
  structured records, not files, images, or large binaries, store those in Amazon
  S3 and keep only a reference in DynamoDB.
- **Set a short Lambda timeout.** Configure the execution timeout to about 3-5
  seconds so a stuck invocation cannot quietly consume your 400,000 free
  GB-seconds.
- **Add a billing alarm.** Create a CloudWatch billing alarm (or AWS Budgets alert)
  so you are notified before any accidental cost.

## Where to go next

This pattern, Lambda for logic plus DynamoDB for state behind a Function URL, is
the backbone for many small AI apps: a chatbot that persists conversation history,
a feedback store for evaluating model outputs (Module 2), or a metadata index for
a RAG system (Module 3). Natural extensions include adding **DELETE** and
**PUT** (update) handlers, swapping the scan for a query, and putting the function
behind API Gateway or Amazon Bedrock Agents.

```{admonition} Attribution
:class: seealso
This walkthrough is adapted from widely shared community guides on building a free
serverless API with AWS Lambda and DynamoDB. Verify all Free Tier limits, IAM
policy names, and console steps against current AWS documentation before use.
```
