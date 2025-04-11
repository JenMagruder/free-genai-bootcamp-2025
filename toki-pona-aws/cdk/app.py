from aws_cdk import App
from cdk_stack import CdkStack

app = App()
CdkStack(app, "TokiPonaApp")
app.synth()