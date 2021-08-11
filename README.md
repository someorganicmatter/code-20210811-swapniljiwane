# Project Overview
This repository is an IaaC framework written in Python/AWS CDK as well as AWS CloudFormation.

It sets up a number of AWS resources to deploy a stack of
- **`AWS SNS`**: Publishes a message with some dummy message data
- **`AWS SQS`**: Queues the messages from SNS and triggers a lambda function
- **`AWS LAMBDA`**: This downstream component takes the data pushes by SQS through an `event` object and write the data into a text file and uploads it to an s3 bucket
- **`S3`**: Hosts the uploaded file and triggers a downstream SNS topic 
- **`AWS SNS`**: Sends a notification mail to the registered email ID specified in app.py file

<br>

# Description
There are two branches in this repo: 
- Current branch - Python CDK code that was reponsible for generating the CFT you see in default branch.

- The other branch CloudFormation template for this project lies. This is the default branch.

> Use `git checkout <branch_name>` to switch the branches and look at the code you want to explore.

<br>
<br>

---
# Welcome to your CDK Python project!

This is a blank project for Python development with CDK.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
