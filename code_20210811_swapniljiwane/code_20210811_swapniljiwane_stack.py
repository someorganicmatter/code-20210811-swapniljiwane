from aws_cdk import (
    core,
    core as cdk,
    aws_lambda as _lambda,
    aws_s3 as s3,
    aws_iam as iam,
    aws_sns as sns,
    aws_s3_notifications as s3_notif,
    aws_sqs as sqs
)

from base_configuration.ResourceBase import ResourceBase

class Code20210811SwapniljiwaneStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, PUSHNOTIFICATIONEMAIL, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ########### GENERATE RESOURCE NAMES DYNAMICALLY FOR CONSISTENCY AND EASE ###########
        bucket_resource = ResourceBase("s3bucket", "demoxyz", "dev", "us-east-1")
        BUCKETRESOURCENAME = bucket_resource.get_resource_name()

        lambda_resource = ResourceBase("lambda", "demoxyz", "dev", "us-east-1")
        LAMBDARESOURCENAME = lambda_resource.get_resource_name()

        role_resource = ResourceBase("iamrole", "demoxyz", "dev", "us-east-1")
        ROLERESOURCENAME = role_resource.get_resource_name()

        sqs_resource = ResourceBase("sqsqueue", "demoxyz", "dev", "us-east-1")
        SQSRESOURCENAME = sqs_resource.get_resource_name()

        source_topic_resource = ResourceBase("sourcesnstopic", "demoxyz", "dev", "us-east-1")
        SOURCETOPICRESOURCENAME = source_topic_resource.get_resource_name()

        email_topic_resource = ResourceBase("emailsnstopic", "demoxyz", "dev", "us-east-1")
        EMAILTOPICRESOURCENAME = email_topic_resource.get_resource_name()

        notif_resource = ResourceBase("snsnotification", "demoxyz", "dev",
                                      "us-east-1")
        SUBSCRIPTIONRESOURCENAME = notif_resource.get_resource_name()

        ########### CREATE AN SQS QUEUE TO RESPOND TO SQS MESSAGES ###########

        queue = sqs.Queue(self,
                        SQSRESOURCENAME,
                        queue_name = SQSRESOURCENAME
        )

        queue.add_to_resource_policy(
            iam.PolicyStatement(sid="snstosqsaccess",
                                        principals=[iam.ServicePrincipal("sns.amazonaws.com")],
                                        actions=["SQS:*"],
                                        effect=iam.Effect.ALLOW,
                                        resources=[queue.queue_arn]
                                )
        )


        ########### CREATE AN SNS TOPIC TO RESPOND TO SQS MESSAGES ###########

        sns_topic = sns.Topic(self,
                              SOURCETOPICRESOURCENAME,
                              topic_name=SOURCETOPICRESOURCENAME,
                              display_name=SOURCETOPICRESOURCENAME)

        sns_sub = sns.Subscription(self,
                                   id=SUBSCRIPTIONRESOURCENAME,
                                   topic=sns_topic,
                                   protocol=sns.SubscriptionProtocol.SQS,
                                   endpoint=queue.queue_arn)

        # uploadbucket.add_event_notification(s3.EventType.OBJECT_CREATED,
        #                                     s3_notif.SnsDestination(sns_topic))


        ########### CREATE AN S3 BUCKET TO UPLOAD THE TEXT FILE TO ###########

        uploadbucket = s3.Bucket(
            self,
            BUCKETRESOURCENAME,
            bucket_name=BUCKETRESOURCENAME,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            encryption=None,
            removal_policy=core.RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            versioned=True)

        ########### CREATE A LAMBDA WITH PERMISSIONS TO WRITE IN S3 BUCKET ABOVE ###########

        lambda_role = iam.Role(
            self,
            ROLERESOURCENAME,
            role_name=ROLERESOURCENAME,
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            inline_policies={
                "s3access":
                iam.PolicyDocument(statements=[
                    iam.PolicyStatement(sid="lambdas3writeaccess",
                                        actions=["s3:PutObject"],
                                        effect=iam.Effect.ALLOW,
                                        resources=[
                                            uploadbucket.bucket_arn,
                                            f"{uploadbucket.bucket_arn}/*"
                                        ]
                    )
                ])
            },
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "service-role/AWSLambdaBasicExecutionRole")
            ])

        base_lambda = _lambda.Function(
            self,
            LAMBDARESOURCENAME,
            function_name=LAMBDARESOURCENAME,
            handler='lambda-handler.handler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            role=lambda_role,
            environment={"BUCKETNAME": uploadbucket.bucket_name},
        )

        base_lambda.add_event_source_mapping("sqs-lambda-trigger",
            enabled=True,
            event_source_arn=queue.queue_arn,
        )

        lambda_role.add_to_policy(
            iam.PolicyStatement(sid="sqslambdapoller",
                                actions=["sqs:DeleteMessage",
                                    "sqs:GetQueueAttributes",
                                    "sqs:ReceiveMessage"
                                ],
                                effect=iam.Effect.ALLOW,
                                resources=[queue.queue_arn]
                                )
        )

        ########### SNS TOPIC AND SUBSCRIPTION TOGETHER RESPOND TO S3 OBJECT CREATION AND SEND OUT AN EMAIL NOTIFICATION ###########

        email_sns_topic = sns.Topic(self,
                              EMAILTOPICRESOURCENAME,
                              topic_name=EMAILTOPICRESOURCENAME,
                              display_name=EMAILTOPICRESOURCENAME)

        email_sns_sub = sns.Subscription(self,
                                   id=f'{SUBSCRIPTIONRESOURCENAME}-email',
                                   topic=email_sns_topic,
                                   protocol=sns.SubscriptionProtocol.EMAIL,
                                   endpoint=PUSHNOTIFICATIONEMAIL)

        uploadbucket.add_event_notification(s3.EventType.OBJECT_CREATED,
                                            s3_notif.SnsDestination(email_sns_topic))
