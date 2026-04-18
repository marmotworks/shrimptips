#!/usr/bin/env python3
"""
Shared configuration for ShrimpTips deployment scripts.
Loads values from .env file with fallback defaults.
"""
import os
from pathlib import Path

# Load .env file from project root
_project_root = Path(__file__).parent
_env_path = _project_root / '.env'

if _env_path.exists():
    with open(_env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            key, _, value = line.partition('=')
            key = key.strip()
            value = value.strip().strip("'\"")
            if key and value:
                os.environ.setdefault(key, value)


def get(key, default=''):
    """Get an environment variable with a default fallback."""
    return os.environ.get(key, default)


def get_int(key, default):
    """Get an integer environment variable with a default fallback."""
    return int(os.environ.get(key, default))


# AWS Configuration
AWS_REGION = get('AWS_REGION', 'us-east-1')
STACK_NAME = get('STACK_NAME', 'shrimptips-webapp')
HOSTED_ZONE_ID = get('HOSTED_ZONE_ID', 'Z07886121VL0W5WNRWN26')

# Legacy CloudFront distribution to clean up
LEGACY_CLOUDFRONT_DISTRIBUTION_ID = get('LEGACY_CLOUDFRONT_DISTRIBUTION_ID', 'E1XNJL0XEWSTK')

# Domain Configuration
DOMAIN_NAME = get('DOMAIN_NAME', 'shrimp.tips')
