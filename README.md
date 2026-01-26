# Titanic API - Production DevOps Implementation

A production-ready containerized Flask API with PostgreSQL backend, demonstrating enterprise DevOps practices including Docker, Kubernetes, and CI/CD automation.

---

## Quick Start

### Prerequisites

- Docker Desktop (with Kubernetes enabled) OR Minikube
- Python 3.11+
- kubectl
- Git

### Local Development (Docker Compose)
```bash
# Clone repository
git clone https://github.com/YOUR-USERNAME/titanic-api.git
cd titanic-api

# Start services
docker-compose up -d

# Check health
curl http://localhost:5000/health

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

**Access the API:** http://localhost:5000

---

## Features

### Application
- ✅ RESTful API for Titanic passenger data
- ✅ PostgreSQL database backend
- ✅ Health check endpoints
- ✅ Environment-based configuration

### DevOps Implementation
- ✅ Multi-stage Docker build (361MB optimized image)
- ✅ Docker Compose for local development
- ✅ Production-grade Kubernetes manifests
- ✅ Horizontal Pod Autoscaling (2-5 replicas)
- ✅ Network policies for security
- ✅ CI/CD pipeline with GitHub Actions
- ✅ Automated security scanning
- ✅ High availability configuration

---

## Architecture
```
┌─────────────┐
│   GitHub    │ ──> CI/CD Pipeline
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Kubernetes  │
│  ┌────────┐ │
│  │ API x2 │ │ ──> Auto-scaling (HPA)
│  └───┬────┘ │
│      │      │
│  ┌───▼────┐ │
│  │  DB    │ │ ──> Persistent Volume
│  └────────┘ │
└─────────────┘
```

---

## Docker

### Build Image
```bash
docker build -t titanic-api:latest .
```

### Run Container
```bash
# With environment variables
docker run -d \
  -p 5000:5000 \
  -e DATABASE_URL=postgresql://user:pass@host:5432/db \
  titanic-api:latest
```

### Image Details
- **Base:** python:3.11-slim
- **Size:** 361MB
- **User:** Non-root (UID 1001)
- **Health Check:** Built-in

---

## Kubernetes

### Deploy to Kubernetes
```bash
# Deploy everything
kubectl apply -k k8s/base/

# Check deployment
kubectl get all -n titanic

# Watch pods start
kubectl get pods -n titanic -w
```

### Access Application
```bash
# Using Minikube
minikube service titanic-api-service -n titanic --url

# Using port-forward
kubectl port-forward -n titanic svc/titanic-api-service 8080:80
```

### Scale Application
```bash
# Manual scaling
kubectl scale deployment titanic-api -n titanic --replicas=5

# Auto-scaling (HPA already configured)
kubectl get hpa -n titanic
```

### View Logs
```bash
# API logs
kubectl logs -n titanic -l app=titanic-api --tail=100 -f

# Database logs
kubectl logs -n titanic titanic-db-0 --tail=100
```

---

## CI/CD Pipeline

### GitHub Actions Workflows

**Automatic on Push:**
- ✅ Code linting (flake8)
- ✅ Docker image build
- ✅ Security scanning (Trivy)
- ✅ Automated testing

**View Pipeline:** https://github.com/Wiryenkfea-Eric/titanic-api/actions

### Manual Deployment
```bash
# Trigger deployment via GitHub UI
# Actions > CD Pipeline > Run workflow > Select environment
```

---

## Testing

### Local Testing
```bash
# Test with Docker Compose
docker-compose up -d
curl http://localhost:5000/health
curl http://localhost:5000/

# Expected responses:
# /health: {"status":"healthy","database":"connected","service":"titanic-api"}
# /: Welcome to the Titanic API
```

### Kubernetes Testing
```bash
# Deploy to local cluster
kubectl apply -k k8s/base/

# Test health endpoint
kubectl run test --rm -i --tty --image=curlimages/curl -- \
  curl http://titanic-api-service.titanic.svc.cluster.local/health
```

---

## Project Structure
```
titanic-api/
├── .github/
│   └── workflows/          # CI/CD pipelines
│       ├── ci-cd.yml       # Main pipeline
│       └── README.md       # Pipeline documentation
├── k8s/
│   └── base/               # Kubernetes manifests
│       ├── namespace/      # Namespace definition
│       ├── configmap/      # Configuration
│       ├── secret/         # Secrets
│       ├── database/       # PostgreSQL StatefulSet
│       ├── api/            # API Deployment
│       ├── networking/     # Services, Ingress, Network Policies
│       ├── autoscaling/    # HPA configuration
│       └── kustomization.yaml
├── src/                    # Application source code
│   ├── app.py              # Flask application
│   ├── models/             # Database models
│   └── views/              # API endpoints
├── docker-compose.yml      # Production-like compose
├── docker-compose.dev.yml  # Development compose
├── Dockerfile              # Multi-stage build
├── .dockerignore           # Docker build exclusions
├── Makefile                # Common commands
├── requirements.txt        # Python dependencies
├── init-db.sql             # Database initialization
├── SOLUTION.md             # Detailed documentation
└── README.md               # This file
```

---

## Development

### Setup Local Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your configuration

# Run locally (requires PostgreSQL)
python run.py
```

### Using Makefile
```bash
make help          # Show available commands
make build         # Build Docker images
make up            # Start services
make down          # Stop services
make logs          # View logs
make shell-api     # Shell into API container
make shell-db      # Shell into database
make clean         # Clean everything
```

---

## Security

### Implemented Security Measures

-  Non-root container user (UID 1001)
-  Read-only root filesystem (where possible)
-  Dropped Linux capabilities
-  Network policies (pod-to-pod isolation)
-  Secrets management (never hardcoded)
-  Container image scanning (Trivy)
-  Resource limits (prevent DoS)
-  Health checks (auto-restart unhealthy pods)

### Security Scanning
```bash
# Scan Docker image
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy image titanic-api:latest

# Scan Kubernetes manifests
kubectl apply --dry-run=client -k k8s/base/
```

---

##  Monitoring & Observability

### Health Checks
```bash
# Application health
curl http://localhost:5000/health

# Kubernetes pod health
kubectl get pods -n titanic
kubectl describe pod <pod-name> -n titanic
```

### Logs
```bash
# Docker Compose logs
docker-compose logs -f api

# Kubernetes logs
kubectl logs -n titanic -l app=titanic-api -f --tail=100
```

### Metrics
```bash
# HPA metrics
kubectl get hpa -n titanic

# Resource usage
kubectl top pods -n titanic
kubectl top nodes
```

---

##  Deployment

### Staging Environment
```bash
# Automatic deployment on push to main branch
git push origin main

# Monitor deployment
kubectl rollout status deployment/titanic-api -n titanic
```

### Production Environment
```bash
# Manual approval required
# GitHub UI: Actions > CD Pipeline > Run workflow > production

# Verify deployment
kubectl get pods -n titanic-prod
curl https://api.production.com/health
```

### Rollback
```bash
# Rollback to previous version
kubectl rollout undo deployment/titanic-api -n titanic

# Rollback to specific revision
kubectl rollout undo deployment/titanic-api -n titanic --to-revision=2

# View rollout history
kubectl rollout history deployment/titanic-api -n titanic
```

---

##  Troubleshooting

### Pods Not Starting
```bash
# Check pod status
kubectl get pods -n titanic

# Describe pod for events
kubectl describe pod <pod-name> -n titanic

# Check logs
kubectl logs <pod-name> -n titanic

# Common issues:
# - Image pull errors: Check image name and availability
# - CrashLoopBackOff: Check application logs
# - Pending: Check resource availability
```

### Database Connection Issues
```bash
# Test database connectivity
kubectl exec -it -n titanic titanic-db-0 -- psql -U titanic_user -d titanic_db

# Check service DNS
kubectl run -it --rm debug --image=busybox --restart=Never -- \
  nslookup titanic-db-service.titanic.svc.cluster.local

# Verify secrets
kubectl get secret titanic-secrets -n titanic -o yaml
```

### CI/CD Pipeline Failures
```bash
# Check workflow logs in GitHub Actions tab
# Common issues:
# - Test failures: Fix code and push
# - Build failures: Check Dockerfile syntax
# - Security scan failures: Update vulnerable dependencies
```

---

## Performance

### Resource Requirements

**API Pods:**
- Requests: 128Mi RAM, 100m CPU
- Limits: 256Mi RAM, 500m CPU

**Database:**
- Requests: 256Mi RAM, 250m CPU
- Limits: 512Mi RAM, 500m CPU

### Auto-Scaling

- **Min Replicas:** 2 (high availability)
- **Max Replicas:** 5 (cost optimization)
- **Target CPU:** 70% utilization
- **Scale-up:** Aggressive (100% in 30s)
- **Scale-down:** Conservative (50% in 5min)

---

## Cost Estimation

### Development (AWS us-east-1)
- **Monthly:** ~$170
- EKS cluster, 2x t3.medium, RDS t3.micro

### Production (AWS us-east-1)
- **Monthly:** ~$340
- EKS cluster, 3x t3.large, RDS t3.small Multi-AZ

**Optimization:** Use spot instances for 60% savings

---

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'feat: add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 📄 License

This project is for assessment purposes.

---

## Support

For issues or questions:
- Create GitHub Issue
- Review `SOLUTION.md` for detailed documentation
- Check GitHub Actions logs for CI/CD issues

---

## Acknowledgments

- **PipeOps** for the technical assessment
- **Titanic Dataset** for demo data
- **Kubernetes Community** for excellent documentation

---


**Last Updated:** January 26, 2026
