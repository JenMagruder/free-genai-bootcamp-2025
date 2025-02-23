from aws_cdk import (
    Stack,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_ec2 as ec2,
    aws_ecr_assets as ecr_assets,
    aws_s3 as s3,
    aws_lambda as lambda_,
    aws_apigateway as apigateway,
    aws_iam as iam,
    aws_logs as logs,
    CfnOutput,
    Duration,
)
from constructs import Construct

class TokiPonaStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create VPC for our services
        vpc = ec2.Vpc(
            self, "TokiPonaVPC",
            max_azs=2,
            nat_gateways=1
        )

        # Create ECS Cluster
        cluster = ecs.Cluster(
            self, "TokiPonaCluster",
            vpc=vpc
        )

        # Build Docker image from local Dockerfile
        image_asset = ecr_assets.DockerImageAsset(
            self, "TokiPonaImage",
            directory="../app"  # Points to directory containing Dockerfile
        )

        # Create Fargate Service for Streamlit App
        fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self, "TokiPonaService",
            cluster=cluster,
            cpu=1024,
            memory_limit_mib=2048,
            desired_count=1,
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_docker_image_asset(image_asset),
                container_port=8501,  # Streamlit default port
                environment={
                    "STREAMLIT_SERVER_PORT": "8501",
                    "STREAMLIT_SERVER_ADDRESS": "0.0.0.0"
                },
                log_driver=ecs.LogDriver.aws_logs(
                    stream_prefix="TokiPona",
                    log_retention=logs.RetentionDays.ONE_WEEK
                )
            ),
            public_load_balancer=True
        )

        # Allow inbound traffic to Streamlit
        fargate_service.target_group.configure_health_check(
            path="/healthz",
            healthy_http_codes="200"
        )

        # S3 bucket for storing OCR training data and models
        model_bucket = s3.Bucket(
            self, "TokiPonaModelBucket",
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED
        )

        # Lambda function for OCR inference
        ocr_lambda = lambda_.DockerImageFunction(
            self, "TokiPonaOCRFunction",
            code=lambda_.DockerImageCode.from_image_asset(
                "../app",  # Uses same Dockerfile but different entry point
                cmd=["inference.handler"]
            ),
            memory_size=2048,
            timeout=Duration.seconds(30),
            environment={
                "MODEL_BUCKET": model_bucket.bucket_name
            }
        )

        # Grant Lambda access to S3
        model_bucket.grant_read(ocr_lambda)

        # Create API Gateway
        api = apigateway.RestApi(
            self, "TokiPonaApi",
            rest_api_name="Toki Pona OCR API",
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_origins=["*"],  # Replace with your Streamlit app domain in production
                allow_methods=["POST"],
                allow_headers=["*"]
            )
        )

        # Add OCR endpoint
        ocr_integration = apigateway.LambdaIntegration(ocr_lambda)
        api.root.add_resource("ocr").add_method("POST", ocr_integration)

        # Outputs
        CfnOutput(self, "StreamlitAppURL", 
                 value=fargate_service.load_balancer.load_balancer_dns_name)
        CfnOutput(self, "APIURL", 
                 value=api.url)
        CfnOutput(self, "ModelBucketName", 
                 value=model_bucket.bucket_name)