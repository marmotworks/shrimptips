# 🦐 ShrimpTips

ShrimpTips is a serverless web application that delivers hilarious and visually striking health and safety guidance tailored exclusively for wild shrimp navigating the perils of the open ocean. 

Leveraging advanced AI, the app generates unique, retro-style Occupational Safety & Health Administration (OSHA)-inspired posters. Each poster features a creative safety tip and a high-quality visual scenario, as if designed by a union of ocean-floor safety inspectors. With taglines like "Beware the Bottom Trawlers!" and "Current Awareness is Self-Awareness," ShrimpTips offers survival wisdom for the free-roaming shrimp of the seas with style, satire, and serious crustacean care.

## 🏗️ Architecture

ShrimpTips uses a sophisticated multi-stage AI pipeline built on AWS serverless technologies:

1.  **Web Interface**: A responsive HTML/JavaScript frontend served via **Amazon CloudFront** and **Amazon API Gateway** with **AWS Lambda**.
2.  **AI Prompt Engineering**: When a user requests a poster, the **Poster Generator Lambda** calls **Amazon Bedrock (Amazon Nova Pro)** to generate a highly creative and contextually rich image generation prompt.
3.  **AI Image Generation**: The generated prompt is then passed to **Amazon Bedrock (Amazon Nova Canvas)** to produce a unique, high-quality, OSHA-style safety poster.
4.  **Infrastructure as Code (IaC)**: The entire environment is provisioned and managed using **AWS CloudFormation**, including CloudFront, ACM, and Route 53.
5.  **Custom Domain & Security**: **Amazon CloudFront** serves HTTPS traffic via an **ACM**-managed certificate, with **Route 53** alias records routing `shrimp.tips` to the CloudFront distribution.

## 🚀 Quick Deployment

### Prerequisites

1.  **AWS CLI** configured with appropriate credentials and access to the `us-east-1` region.
2.  **Python 3.12+** installed.
3.  **AWS Bedrock Model Access**: Ensure you have access to the following models in `us-east-1`:
    - `amazon.nova-pro-v1:0` (for prompt generation)
    - `amazon.nova-canvas-v1:0` (for image generation)
4.  **Boto3** installed (`pip install boto3`).

### Deploy the Application

1.  **Clone and navigate to the repository:**
    ```bash
    git clone <repository-url>
    cd shrimptips
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Deploy the stack:**
    ```bash
    python deploy.py
    ```

4.  **Access your application:**
    Open `https://shrimp.tips` in your browser to see your ShrimpTips application in action!
    The CloudFront distribution serves the web interface and routes API requests to Lambda via API Gateway.

### Custom Domain Setup

To use the `shrimp.tips` domain, CloudFormation manages the entire delivery path automatically:

1.  Ensure you have a Route 53 hosted zone for `shrimp.tips`.
2.  Run `python deploy.py` — the deploy script passes the hosted zone ID (`Z07886121VL0W5WNRWN26`) by default.
3.  The stack creates:
    - **ACM certificate** with DNS validation in your Route 53 hosted zone
    - **CloudFront distribution** with the ACM certificate and shrimp.tips as an alias
    - **Route 53 A record** (alias) pointing shrimp.tips to the CloudFront distribution
    - **Origin Access Control (OAC)** for secure API Gateway access

The deploy script automatically removes the legacy CloudFront distribution (E1XNJL0XEWSTK) before deploying the new CloudFormation-managed one, freeing the shrimp.tips CNAME.

## 📁 Project Structure

```
shrimptips/
├── lambdas/
│   ├── poster_generator.py    # Nova Pro + Nova Canvas image generation
│   └── web_interface.py       # HTML web interface & API routing
├── templates/
│   └── shrimptips-stack.yaml  # CloudFormation template
├── deploy.py                  # Deployment automation script
├── check_deployment.py        # Utility to verify Lambda sync
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🎨 Features

- **Multi-Stage AI Generation**: Uses a combination of Nova Pro and Nova Canvas for unparalleled creativity.
- **Retro OSHA Aesthetic**: High-quality, vintage-style safety posters.
- **Randomized Content**: Every visit generates a new, unique safety tip and visual.
- **Serverless & Scalable**: Scales automatically with demand and costs only when used.
- **Responsive Design**: Works seamlessly on desktop and mobile devices.

## 🔧 Configuration

### AWS Requirements

The application requires access to the following AWS services:
- **Amazon Bedrock**: For Nova Pro and Nova Canvas model invocation.
- **AWS Lambda**: To run the web interface and poster generation logic.
- **Amazon API Gateway**: To host the RESTful API and web interface.
- **AWS CloudWatch**: For application logging and monitoring.

## 🛠️ Development

### Local Testing

To test the Lambda functions locally:

1.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2.  Set up AWS credentials with access to Bedrock in `us-east-1`.

3.  Run individual functions with test events using a local testing tool or `pytest`.

### Verifying Deployment

After deploying, you can verify that your local code is synchronized with the deployed Lambda functions using the utility script:

```bash
python check_deployment.py
```

## 📊 Monitoring

The application uses **Amazon CloudWatch** for:
- Logging Bedrock request/response cycles.
- Error tracking and debugging.
- Performance monitoring of Lambda execution.

## 🔒 Security

- **IAM Least Privilege**: Lambda execution roles are scoped to minimum required permissions.
- **HTTPS-only**: All traffic is served over HTTPS via CloudFront with ACM-managed certificate.
- **CORS**: Properly configured for secure browser access.

## 💰 Cost Optimization

This architecture is designed for maximum cost-efficiency:
- **Pay-per-use**: Lambda, API Gateway, and Bedrock are all consumption-based.
- **Zero Idle Cost**: No running servers or always-on infrastructure.

## 🤝 Contributing

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Test thoroughly (using `pytest` and `check_deployment.py`).
5. Submit a pull request.

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues or questions:
1. Check the CloudWatch logs for error details.
2. Verify AWS Bedrock model access in `us-east-1`.
3. Ensure proper IAM permissions for the Lambda execution role.
