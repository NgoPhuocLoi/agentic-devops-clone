# Multi-Agent CD Manifest Generator

A sophisticated multi-agent system using OpenAI Agents SDK to automatically generate Dockerfile and Kubernetes deployment manifests from GitHub repositories.

## 🎯 Overview

This system uses **five specialized agents** coordinated by an orchestrator to:

1. **Analyze** GitHub repositories to understand structure and requirements
2. **Generate** optimized, production-ready Dockerfiles
3. **Create** complete Kubernetes deployment manifests
4. **Enable** user fine-tuning and refinement
5. **Produce** deployment-ready artifacts

## 🤖 Multi-Agent Architecture

### Agent 1: Repository Analyzer

- Detects programming language and framework
- Identifies runtime version requirements
- Finds dependency files and build commands
- Determines application entry points
- Provides deployment recommendations

**Supported Languages:**

- Python (Flask, FastAPI, Django)
- Node.js (Express, Next.js, React, Vue)
- Java (Spring Boot with Maven/Gradle)
- Go

### Agent 2: Dockerfile Generator

- Creates multi-stage Dockerfiles
- Implements security best practices
- Optimizes layer caching
- Configures non-root users
- Includes health checks

**Features:**

- Multi-stage builds for smaller images
- Minimal base images (Alpine, slim, scratch)
- Security hardening
- Production optimizations

### Agent 3: Kubernetes Engineer

- Generates Deployment manifests
- Creates Services for networking
- Sets up ConfigMaps for configuration
- Configures Horizontal Pod Autoscaler
- Creates Ingress for external access

**Generated Manifests:**

- `Deployment` - with resource limits and health probes
- `Service` - ClusterIP for internal access
- `ConfigMap` - application configuration
- `HorizontalPodAutoscaler` - auto-scaling (optional)
- `Ingress` - external access with TLS (optional)

### Agent 4: Refinement Specialist

- Applies user-requested modifications
- Maintains best practices
- Validates changes
- Explains impact of refinements

### Agent 5: DevOps Orchestrator

- Coordinates all agents
- Manages workflow
- Handles user interactions
- Ensures artifact quality

## 📋 Prerequisites

### Required

1. **OpenAI API Key**

   ```bash
   export OPENAI_API_KEY='your-api-key-here'
   ```

2. **Python Dependencies**
   ```bash
   cd agentic_devops
   pip install -r requirements.txt
   ```

### Optional

3. **GitHub Token** (for private repositories)
   ```bash
   export GITHUB_TOKEN='your-github-token'
   ```

## 🚀 Quick Start

### Basic Usage

```bash
cd examples
python cd_manifest_generator.py
```

### Interactive Prompts

The system will ask for:

1. **Repository Details**

   - Owner (e.g., 'facebook')
   - Repository name (e.g., 'react')
   - Branch (default: 'main')

2. **Deployment Configuration**
   - Application name (default: repo name)
   - Number of replicas (default: 3)
   - Domain for Ingress (optional)

### Example Session

```
🚀 CD Manifest Generator - Multi-Agent System
================================================================================

Enter GitHub repository details:
  Repository owner (e.g., 'facebook'): myorg
  Repository name (e.g., 'react'): myapp
  Branch (default: 'main'): main

Application name for K8s (default: repo name): myapp
Number of replicas (default: 3): 3
Domain for Ingress (optional, e.g., 'app.example.com'): myapp.example.com

================================================================================
🤖 Initializing agents...
================================================================================

📊 Phase 1: Repository Analysis
--------------------------------------------------------------------------------

🎯 Executing workflow for: myorg/myapp

[Agents analyze repository, generate Dockerfile and K8s manifests]

================================================================================
✅ GENERATION COMPLETE
================================================================================

[Dockerfile and K8s manifests displayed]

================================================================================
🔧 REFINEMENT PHASE
================================================================================

You can now fine-tune the generated artifacts.
Type your refinement instructions or 'done' to finish.

Examples:
  - Change Python version to 3.12
  - Increase memory limit to 1Gi
  - Add Redis as a dependency
  - Change replicas to 5

💬 Refinement (or 'done'): Change replicas to 5

🔄 Applying refinement...

[Updated manifests displayed]

💬 Refinement (or 'done'): done

================================================================================
✨ All done! Your deployment artifacts are ready.
================================================================================

💾 Save artifacts to files? (y/n): y

📁 Artifacts would be saved to: ./output/myapp
   - Dockerfile
   - k8s-deployment.yaml
   - k8s-service.yaml
   - k8s-configmap.yaml
   - k8s-hpa.yaml (if enabled)
   - k8s-ingress.yaml (if enabled)

✅ Implementation complete!
```

## 🎨 Generated Artifacts

### Dockerfile

The generated Dockerfile includes:

- **Multi-stage builds** - Separates build and runtime dependencies
- **Security hardening** - Non-root user, minimal base images
- **Layer optimization** - Efficient caching for faster builds
- **Health checks** - Container orchestration support
- **Best practices** - Industry-standard patterns

**Example (Python Flask):**

```dockerfile
# Multi-stage build for Python Flask application
# Build stage
FROM python:3.11-slim as builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /root/.local /root/.local
COPY . .

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

ENV PATH=/root/.local/bin:$PATH

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/health', timeout=2)" || exit 1

CMD python app.py
```

### Kubernetes Manifests

#### Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  namespace: default
  labels:
    app: myapp
    version: v1
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
        version: v1
    spec:
      containers:
        - name: myapp
          image: myapp:latest
          ports:
            - containerPort: 5000
              name: http
          resources:
            requests:
              memory: 256Mi
              cpu: 100m
            limits:
              memory: 512Mi
              cpu: 500m
          livenessProbe:
            httpGet:
              path: /health
              port: 5000
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /health
              port: 5000
            initialDelaySeconds: 5
            periodSeconds: 5
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
```

#### Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp
  namespace: default
spec:
  selector:
    app: myapp
  ports:
    - protocol: TCP
      port: 80
      targetPort: 5000
  type: ClusterIP
```

#### HPA (Horizontal Pod Autoscaler)

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp
  namespace: default
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  minReplicas: 3
  maxReplicas: 9
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
```

#### Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp
  namespace: default
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
    - hosts:
        - myapp.example.com
      secretName: myapp-tls
  rules:
    - host: myapp.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: myapp
                port:
                  number: 80
```

## 🔧 Refinement Examples

### Common Refinements

1. **Change Base Image Version**

   ```
   Change Python version to 3.12
   ```

2. **Adjust Resources**

   ```
   Increase memory limit to 1Gi and CPU to 1000m
   ```

3. **Modify Replicas**

   ```
   Change replicas to 5
   ```

4. **Add Environment Variables**

   ```
   Add environment variable DATABASE_URL
   ```

5. **Change Ports**

   ```
   Change application port to 8080
   ```

6. **Add Dependencies**
   ```
   Add Redis as a dependency in the deployment
   ```

## 🏗️ Deployment Workflow

### 1. Build Docker Image

```bash
docker build -t myapp:latest .
```

### 2. Push to Registry

```bash
docker tag myapp:latest myregistry/myapp:latest
docker push myregistry/myapp:latest
```

### 3. Update K8s Manifests

Update image reference in deployment.yaml:

```yaml
image: myregistry/myapp:latest
```

### 4. Deploy to Kubernetes

```bash
kubectl apply -f k8s-deployment.yaml
kubectl apply -f k8s-service.yaml
kubectl apply -f k8s-configmap.yaml
kubectl apply -f k8s-hpa.yaml
kubectl apply -f k8s-ingress.yaml
```

### 5. Verify Deployment

```bash
kubectl get pods
kubectl get svc
kubectl get ingress
kubectl describe deployment myapp
```

## 🔍 Repository Analysis Details

### Detected Patterns

The analyzer identifies:

1. **Language Detection**

   - Based on GitHub API
   - Confirmed by dependency files

2. **Framework Detection**

   - Python: Flask, FastAPI, Django
   - Node.js: Express, Next.js, React, Vue
   - Java: Spring Boot
   - Go: Standard library

3. **Dependency Files**

   - Python: `requirements.txt`, `pyproject.toml`
   - Node.js: `package.json`
   - Java: `pom.xml`, `build.gradle`
   - Go: `go.mod`

4. **Build Commands**

   - Detected from package scripts
   - Framework-specific defaults
   - Best practice commands

5. **Start Commands**
   - Entry point detection
   - Framework-specific patterns
   - Production configurations

## 🛡️ Security Features

### Dockerfile Security

- Non-root user execution
- Minimal base images
- No unnecessary packages
- Layer optimization
- Security scanning ready

### Kubernetes Security

- Pod Security Context
- Resource limits
- Non-root containers
- Network policies ready
- RBAC compatible

## 📚 Best Practices

### Dockerfile

1. **Multi-stage builds** - Reduce image size
2. **Layer caching** - Faster builds
3. **Non-root user** - Security
4. **Health checks** - Reliability
5. **Minimal base** - Attack surface reduction

### Kubernetes

1. **Resource limits** - Prevent resource exhaustion
2. **Health probes** - Auto-healing
3. **HPA** - Auto-scaling
4. **Labels** - Organization
5. **Security context** - Pod security

## 🤝 Contributing

To add support for more languages/frameworks:

1. Update `analyze_repository` tool
2. Add language-specific Dockerfile templates
3. Update documentation
4. Test with real repositories

## 📝 License

This project is part of the DevOps Agentic System.

## 🆘 Troubleshooting

### Common Issues

1. **Import errors**

   - Ensure you're in the correct directory
   - Check Python path configuration

2. **GitHub API rate limits**

   - Use GITHUB_TOKEN for higher limits
   - Wait for rate limit reset

3. **OpenAI API errors**

   - Verify API key is set
   - Check account credits

4. **Agent timeouts**
   - Large repositories may take longer
   - Be patient during analysis

## 🎓 Learn More

- [OpenAI Agents SDK Documentation](https://github.com/openai/swarm)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Multi-Agent Systems](https://en.wikipedia.org/wiki/Multi-agent_system)

## ⭐ Features

- ✅ Automatic language and framework detection
- ✅ Multi-stage Docker builds
- ✅ Production-ready Kubernetes manifests
- ✅ Interactive refinement system
- ✅ Security hardening
- ✅ Best practices enforcement
- ✅ Health check configuration
- ✅ Auto-scaling support
- ✅ Ingress with TLS
- ✅ Resource optimization

## 🚀 Future Enhancements

- [ ] Support for more languages (Rust, Ruby, PHP)
- [ ] Helm chart generation
- [ ] CI/CD pipeline integration
- [ ] Cost estimation
- [ ] Security scanning integration
- [ ] Monitoring configuration
- [ ] GitOps integration
- [ ] Multi-environment support

---

**Happy Deploying! 🎉**
