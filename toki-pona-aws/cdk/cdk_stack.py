from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
)
from constructs import Construct
from .config import Config

class CdkStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create VPC
        vpc = ec2.Vpc(self, "TokiPonaVPC", max_azs=2)

        # Create ECS Cluster
        cluster = ecs.Cluster(self, "TokiPonaCluster", vpc=vpc)

        # Create Fargate Service
        fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self, "TokiPonaWebApp",
            cluster=cluster,
            cpu=Config.CPU,
            memory_limit_mib=Config.MEMORY,
            desired_count=Config.MIN_CAPACITY,
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_asset("../app"),
                container_port=Config.CONTAINER_PORT,
            ),
        )

        # Setup AutoScaling
        scaling = fargate_service.service.auto_scale_task_count(
            min_capacity=Config.MIN_CAPACITY,
            max_capacity=Config.MAX_CAPACITY
        )

        scaling.scale_on_cpu_utilization(
            "CpuScaling",
            target_utilization_percent=70,
            scale_in_cooldown=Duration.seconds(60),
            scale_out_cooldown=Duration.seconds(60),
        )