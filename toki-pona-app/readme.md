# Streamlit Toki Pona app with AWS deployment

Learn Toki Pona with the help of a Streamlit app deployed on AWS.

## If you need deployment to HTTPS

## What is Streamlit?

Streamlit is an open-source Python library that makes it easy to create and share custom web apps for machine learning and data science. By using Streamlit you can quickly build and deploy powerful data applications. For more information about the open-source library, see the [Streamlit documentation](https://docs.streamlit.io/).

## What is Toki Pona?

Toki Pona is a language that combines elements of English, Pona, and Japanese. For more information, see the [Wikipedia entry](https://en.wikipedia.org/wiki/Toki_Pona).

## How can you learn Toki Pona with Streamlit?

The app is located at [https://jabbru-toki-pona-app.streamlit.app/](https://jabbru-toki-pona-app.streamlit.app/).

## Let's build!

### Prerequisites

- AWS Account
- [AWS CDK](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html)
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- Docker

### TL;DR - quick deploy

You can find the detailed deployment description below. But if you want to **deploy it quickly** (without testing Streamlit app locally), run the following commands in your terminal:

```
$ git clone https://github.com/jenmagruder/free-genai-bootcamp-2025/toki-pona-app.git
$ cd toki-pona-app/cdk/
$ aws configure
$ npm install -g aws-cdk
$ python3 -m venv .env
$ source .env/bin/activate
$ pip install -r requirements.txt
$ cdk bootstrap
$ cdk synth
$ cdk deploy

When deployment completes, the CDK CLI will provide outputs. Now when you open your browser and go to the `toki-pona-app/toki-pona-streamlit-app/tokiPonaStreamlitApp.StreamlitPonaWebAppServiceServiceURL`, you will see your application.

**Congrats! Your app is online!** 🎉

**Optional:**
To delete the stack and all resources, run:
$ cdk destroy


### Project Structure

toki-pona-app/
├── cdk/
│   ├── lib/
│   │   └── toki-pona-stack.ts
│   ├── bin/
│   │   └── app.ts
│   ├── test/
│   ├── cdk.json
│   └── package.json
├── frontend/
│   └── src/
├── lambda/
│   ├── ocr-inference/
│   └── api/
└── sagemaker/
    └── training/