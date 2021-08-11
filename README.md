# Project Overview
This repository is an IaaC framework written in Python as well as AWS CDK.

It sets up a number of AWS resources to deploy a stack of
- **`AWS SNS`**: Publishes a message with some dummy message data
- **`AWS SQS`**: Queues the messages from SNS and triggers a lambda function
- **`AWS LAMBDA`**: This downstream component takes the data pushes by SQS through an `event` object and write the data into a text file and uploads it to an s3 bucket
- **`S3`**: Hosts the uploaded file and triggers a downstream SNS topic 
- **`AWS SNS`**: Sends a notification mail to the registered email ID specified in app.py file

---
# Description
There are two branches in this repo: 
- Current branch - CloudFormation template for this project lies. This is the default branch.

- The other branch contains Python CDK code that was reponsible for generating the CFT you see in default branch.

> Use `git checkout <branch_name>` to switch the branches and look at the code you want to explore.