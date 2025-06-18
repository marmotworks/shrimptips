# 🦐 ShrimpTips

The ShrimpTips repository powers an efficient serverless web application that delivers health and safety guidance tailored exclusively for wild shrimp navigating the perils of the open ocean. Leveraging AWS-native technologies, this app generates wellness tips rooted in marine ecology, environmental science, and a touch of nautical whimsy. Each guideline is transformed into a striking, retro-style Occupational Safety & Health Administration (OSHA)-inspired poster—as if designed by a union of ocean-floor safety inspectors. With taglines like "Beware the Bottom Trawlers!" and "Current Awareness is Self-Awareness," the posters offer survival wisdom for the free-roaming shrimp of the seas. Whether dodging predators, avoiding pollution zones, or just trying to stay upright in a strong current, ShrimpTips is a spirited salute to shellfish safety in the wild, presented with style, satire, and serious crustacean care.

## 🏗️ Architecture

This serverless application uses:
- **AWS Lambda** - Serverless compute for poster generation and web interface
- **AWS Bedrock Nova Canvas** - AI image generation for OSHA-style safety posters
- **API Gateway** - RESTful API and web hosting
- **CloudFormation** - Infrastructure as Code (IaC)
- **Route 53** - DNS management for custom domain (optional)
- **Certificate Manager** - SSL/TLS certificates (optional)

## 🚀 Quick Deployment

### Prerequisites

1. AWS CLI configured with appropriate credentials
2. Python 3.12+ installed
3. Access to AWS Bedrock Nova Canvas model in us-east-1 region

### Deploy the Application

1. **Clone and navigate to the repository:**
   ```bash
   git clone <repository-url>
   cd shrimptips
   ```

2. **Set up AWS credentials:**
   ```bash
   export AWS_ACCESS_KEY_ID=your_access_key
   export AWS_SECRET_ACCESS_KEY=your_secret_key
   export AWS_DEFAULT_REGION=us-east-1
   ```

3. **Deploy the stack:**
   ```bash
   python deploy.py
   ```

4. **Access your application:**
   The deployment script will output the API Gateway URL where your application is accessible.

### Custom Domain Setup (Optional)

To use the `shrimp.tips` domain:

1. Ensure you have a Route 53 hosted zone for `shrimp.tips`
2. Update the deployment script or CloudFormation parameters with your hosted zone ID
3. Redeploy the stack

## 📁 Project Structure

```
shrimptips/
├── lambda/
│   ├── poster_generator.py    # Nova Canvas image generation
│   └── web_interface.py       # HTML web interface
├── templates/
│   └── shrimptips-stack.yaml  # CloudFormation template
├── deploy.py                  # Deployment automation script
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🎨 Features

- **AI-Generated Safety Posters**: Uses AWS Bedrock Nova Canvas to create unique OSHA-style safety posters
- **Randomized Content**: Each visit generates a new poster with different safety tips and visual styles
- **Responsive Design**: Works on desktop and mobile devices
- **Serverless Architecture**: Scales automatically and costs only for usage
- **Custom Domain Support**: Can be configured to work with shrimp.tips domain

## 🔧 Configuration

### Environment Variables

The Lambda functions use the following AWS services:
- **Bedrock Runtime**: For Nova Canvas image generation
- **CloudWatch Logs**: For application logging

### Safety Tips Database

The application includes 15+ predefined safety tips for wild shrimp:
- "Beware the Bottom Trawlers!"
- "Current Awareness is Self-Awareness"
- "Stay Alert in Kelp Forests"
- "Predator Detection Saves Lives"
- And many more...

## 🛠️ Development

### Local Testing

To test the Lambda functions locally:

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up AWS credentials for Bedrock access

3. Run individual functions with test events

### Updating the Application

To update the application after making changes:

1. Modify the Lambda function code in the `lambda/` directory
2. Run the deployment script again:
   ```bash
   python deploy.py
   ```

## 📊 Monitoring

The application includes CloudWatch logging for:
- Image generation requests and responses
- Error tracking and debugging
- Performance monitoring

## 🔒 Security

- IAM roles with minimal required permissions
- CORS enabled for web browser access
- HTTPS-only access through API Gateway
- No sensitive data stored or logged

## 💰 Cost Optimization

This serverless architecture is designed for cost efficiency:
- Pay-per-request pricing for Lambda and API Gateway
- Bedrock Nova Canvas charges per image generated
- No always-on infrastructure costs
- Automatic scaling based on demand

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues or questions:
1. Check the CloudWatch logs for error details
2. Verify AWS Bedrock model access in us-east-1
3. Ensure proper IAM permissions for Lambda execution role
4. Review the CloudFormation stack events for deployment issues