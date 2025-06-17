#!/bin/bash

# Install linters if not already installed
pip install --upgrade pip
pip install pylint cfn-lint

# Run pylint for more detailed linting
echo "Running pylint..."
pylint lambda/

# Run cfn-lint for CloudFormation templates
echo "Running cfn-lint..."
find . -maxdepth 2 -name "*.yml" -o -name "*.yaml" | grep -v "\.github" | xargs cfn-lint
if [ $? -ne 0 ]; then
  echo "cfn-lint detected issues in CloudFormation templates."
  exit 1
fi

echo "Pre-commit hooks completed successfully!"
