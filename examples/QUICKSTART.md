# 🚀 CD Manifest Generator - Quick Start Guide

Generate Dockerfile and Kubernetes manifests from any GitHub repository using AI-powered multi-agent system!

## ⚡ Quick Start (5 minutes)

### Step 1: Setup

```bash
cd examples
./setup_cd_generator.sh
```

### Step 2: Set Environment Variables

```bash
# Required: OpenAI API Key
export OPENAI_API_KEY='sk-...'

# Optional: GitHub Token (for private repos or higher rate limits)
export GITHUB_TOKEN='ghp_...'
```

### Step 3: Activate Virtual Environment

```bash
source ../agentic_devops/.venv/bin/activate
```

### Step 4: Run!

#### Option A: Full Interactive Mode (Recommended)

```bash
python cd_manifest_generator.py
```

This provides:

- ✅ Complete multi-agent workflow
- ✅ Interactive refinement
- ✅ Save artifacts to files
- ✅ Full explanations

#### Option B: Simple Demo Mode

```bash
python cd_manifest_demo.py
```

This provides:

- ✅ Quick generation
- ✅ Example repository
- ✅ Basic output

## 📋 What You'll Get

### 1. Dockerfile

```dockerfile
# Multi-stage production-ready Dockerfile
# - Optimized for your language/framework
# - Security best practices
# - Health checks
# - Non-root user
```

### 2. Kubernetes Deployment

```yaml
# Complete deployment configuration
# - Resource limits
# - Health probes
# - Security context
# - Labels and selectors
```

### 3. Kubernetes Service

```yaml
# Service for networking
# - ClusterIP configuration
# - Port mapping
```

### 4. ConfigMap

```yaml
# Configuration management
# - Environment variables
# - App settings
```

### 5. Horizontal Pod Autoscaler (HPA)

```yaml
# Auto-scaling configuration
# - CPU-based scaling
# - Memory-based scaling
# - Min/max replicas
```

### 6. Ingress (if domain provided)

```yaml
# External access configuration
# - TLS/HTTPS support
# - Domain routing
# - cert-manager integration
```

## 🎯 Example Session

```bash
$ python cd_manifest_generator.py

🚀 CD Manifest Generator - Multi-Agent System
================================================================================

Enter GitHub repository details:
  Repository owner (e.g., 'facebook'): pallets
  Repository name (e.g., 'react'): flask
  Branch (default: 'main'): main

Application name for K8s (default: repo name): my-flask-app
Number of replicas (default: 3): 3
Domain for Ingress (optional, e.g., 'app.example.com'): flask.example.com

================================================================================
🤖 Initializing agents...
================================================================================

📊 Phase 1: Repository Analysis
--------------------------------------------------------------------------------

✅ Repository analyzed:
   - Language: Python
   - Framework: Flask
   - Runtime: Python 3.11
   - Port: 5000

🐳 Generating Dockerfile...
   - Multi-stage build
   - Security hardened
   - Health checks included

☸️  Generating Kubernetes manifests...
   - Deployment (3 replicas)
   - Service (ClusterIP)
   - ConfigMap
   - HPA (min: 3, max: 9)
   - Ingress (flask.example.com)

================================================================================
✅ GENERATION COMPLETE
================================================================================

[Artifacts displayed with explanations]

================================================================================
🔧 REFINEMENT PHASE
================================================================================

💬 Refinement (or 'done'): Change Python version to 3.12

[Updated Dockerfile shown]

💬 Refinement (or 'done'): Increase memory limit to 1Gi

[Updated K8s manifests shown]

💬 Refinement (or 'done'): done

💾 Save artifacts to files? (y/n): y

✅ Artifacts saved to: ./output/my-flask-app/
```

## 🎨 Supported Languages & Frameworks

### Python

- ✅ Flask
- ✅ FastAPI
- ✅ Django
- ✅ General Python apps

### Node.js

- ✅ Express
- ✅ Next.js
- ✅ React
- ✅ Vue

### Java

- ✅ Spring Boot (Maven)
- ✅ Spring Boot (Gradle)

### Go

- ✅ Standard library
- ✅ Web frameworks

## 💡 Use Cases

### 1. New Project Deployment

Quickly bootstrap deployment configuration for a new application.

### 2. Modernizing Existing Apps

Generate containerization and K8s configs for legacy applications.

### 3. Learning & Experimentation

Understand best practices through generated examples.

### 4. Template Generation

Create base templates for your organization's deployment standards.

### 5. CI/CD Integration

Automate deployment manifest generation in pipelines.

## 🔧 Refinement Examples

After initial generation, you can refine artifacts with commands like:

### Dockerfile Refinements

```
- Change Python version to 3.12
- Use alpine base image
- Add build-essential package
- Change working directory to /opt/app
- Add multi-stage build optimization
```

### Kubernetes Refinements

```
- Increase memory limit to 1Gi
- Change replicas to 5
- Set CPU request to 200m
- Add environment variable DATABASE_URL
- Enable readiness probe on /ready endpoint
- Change port to 8080
```

## 📦 Deployment Workflow

### 1. Generate Manifests

```bash
python cd_manifest_generator.py
```

### 2. Build Docker Image

```bash
cd your-repo
docker build -t myapp:v1.0 .
```

### 3. Test Locally

```bash
docker run -p 8080:5000 myapp:v1.0
```

### 4. Push to Registry

```bash
docker tag myapp:v1.0 myregistry.io/myapp:v1.0
docker push myregistry.io/myapp:v1.0
```

### 5. Update K8s Manifests

Update image reference in deployment.yaml

### 6. Deploy to Kubernetes

```bash
cd output/myapp
kubectl apply -f .
```

### 7. Verify

```bash
kubectl get pods
kubectl get svc
kubectl logs deployment/myapp
```

## 🛡️ Security Features

### Dockerfile Security

- ✅ Non-root user execution
- ✅ Minimal base images
- ✅ No unnecessary packages
- ✅ Layer optimization
- ✅ Security scanning ready

### Kubernetes Security

- ✅ Pod Security Context
- ✅ Resource limits
- ✅ Non-root containers
- ✅ Network policies ready
- ✅ RBAC compatible

## 🐛 Troubleshooting

### "Import errors"

```bash
# Make sure you're in the virtual environment
source ../agentic_devops/.venv/bin/activate

# Verify Python path
python -c "import sys; print(sys.path)"
```

### "OPENAI_API_KEY not set"

```bash
# Set the API key
export OPENAI_API_KEY='sk-your-key-here'

# Verify it's set
echo $OPENAI_API_KEY
```

### "GitHub API rate limit"

```bash
# Use a GitHub token for higher limits
export GITHUB_TOKEN='ghp_your-token-here'
```

### "Agent timeout"

```bash
# Large repositories take longer
# Be patient and wait for analysis to complete
# Consider using a smaller/simpler repo for testing
```

## 📚 Learn More

- 📖 [Full Documentation](./CD_MANIFEST_GENERATOR_README.md)
- 🎯 [OpenAI Agents SDK](https://github.com/openai/swarm)
- 🐳 [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- ☸️ [Kubernetes Docs](https://kubernetes.io/docs/)

## 🆘 Getting Help

### Common Questions

**Q: How long does generation take?**
A: Usually 30-60 seconds for analysis + generation. Refinements are faster.

**Q: Can I use with private repositories?**
A: Yes! Just set the `GITHUB_TOKEN` environment variable.

**Q: What if my language isn't supported?**
A: The system uses GPT-4 and can handle many languages. Try it and provide feedback!

**Q: Can I customize the generated artifacts?**
A: Yes! Use the interactive refinement mode to make changes.

**Q: Is this production-ready?**
A: The generated artifacts follow best practices but should be reviewed and tested before production use.

## ✨ Next Steps

1. ✅ Generate your first manifests
2. ✅ Review and understand the artifacts
3. ✅ Test locally with Docker
4. ✅ Deploy to a dev cluster
5. ✅ Refine based on your needs
6. ✅ Use as templates for similar projects

## 🎉 Success!

You're now ready to generate production-grade deployment artifacts for any GitHub repository!

---

**Happy Deploying! 🚀**

Need help? Check the [full documentation](./CD_MANIFEST_GENERATOR_README.md) or open an issue.
