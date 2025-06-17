
# ShrimpTips Repository Overview

## Repository Purpose
The ShrimpTips repository powers an efficient serverless web application that delivers health and safety guidance tailored exclusively for wild shrimp navigating the perils of the open ocean. Leveraging AWS-native technologies, this app generates wellness tips rooted in marine ecology, environmental science, and a touch of nautical whimsy. Each guideline is transformed into a striking, retro-style Occupational Safety & Health Administration (OSHA)-inspired poster—as if designed by a union of ocean-floor safety inspectors. With taglines like “Beware the Bottom Trawlers!” and “Current Awareness is Self-Awareness,” the posters offer survival wisdom for the free-roaming shrimp of the seas. Whether dodging predators, avoiding pollution zones, or just trying to stay upright in a strong current, ShrimpTips is a spirited salute to shellfish safety in the wild, presented with style, satire, and serious crustacean care.

## Setup Instructions
//TODO 1. TODO

## Repository Structure
- `/src`: Core application code
- `/tests`: Test suite
- `/docs`: Documentation
- `README.md`: Readme with helpful guidance

## CI/CD Workflows
- `.openhands/pre-commit.sh`: Runs various linters and formatters on Python code and CloudFormation templates before commits.


# Development Guidelines
Always make sure any tests are passing before committing changes. If an approach isn't working and needs revision, first verify compliance with official documentation online. If errors are encountered as part of script execution, check online for context around the error before attempting a new solution. If errors indicate failure due to preexisting infrastructure, stop attempting to resolve the issue and prompt the user. 