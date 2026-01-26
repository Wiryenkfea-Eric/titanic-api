# CI/CD Workflows

## CI/CD Pipeline
Automated testing, building, and deployment pipeline using GitHub Actions.

**Trigger:** Push to main branch, Pull requests

**Jobs:**
1. Test - Lint and validate code
2. Build - Build Docker image
3. Deploy - Deploy to Kubernetes (staging/production)

## Usage
Push to main branch to trigger automatic deployment.
