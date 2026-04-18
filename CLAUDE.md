# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview
ShrimpTips is a serverless web application that uses Amazon Bedrock (Nova Pro and Nova Canvas) to generate retro-style OSHA-inspired safety posters for shrimp.

## Development Commands

### Environment Setup
- Install dependencies: `pip install -r requirements.txt`

### Testing
- Run all tests: `pytest`
- Run a specific test file: `pytest tests/<test_file>.py`
- Run a specific test case: `pytest tests/<test_file>.py#<test_function_name>`

### Deployment & Verification
- Deploy the stack: `python deploy.py`
- Verify Lambda synchronization: `python check_deployment.py`

## Architecture

### Core Components
- **Lambdas** (`lambdas/`):
    - `poster_generator.py`: Orchestrates the AI pipeline. Uses Amazon Bedrock (Nova Pro) to generate prompts and Nova Canvas to generate images.
    - `web_interface.py`: Serves the HTML frontend and handles API routing via Amazon API Gateway.
- **Infrastructure** (`templates/`): Managed via AWS CloudFormation (`shrimptips-stack.yaml`).
- **AI Pipeline**: Multi-stage process leveraging Amazon Bedrock's generative models.

### Project Structure
- `lambdas/`: Contains the AWS Lambda function source code.
- `templates/`: CloudFormation templates for infrastructure as code.
- `tests/`: Unit and functional tests (using `pytest`, `moto`, and `playwright`).
- `deploy.py`: Automation script for provisioning the AWS environment.
- `check_deployment.py`: Utility to ensure local code changes are reflected in deployed Lambdas.
- `requirements.txt`: Python project dependencies.
