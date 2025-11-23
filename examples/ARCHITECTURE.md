# Multi-Agent CD Manifest Generator Architecture

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              USER INPUT                                  │
│  - GitHub Repository (owner/repo)                                        │
│  - Branch, App Name, Replicas, Domain                                    │
└─────────────────────────────┬───────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR AGENT (GPT-4)                            │
│  - Workflow coordination                                                 │
│  - User interaction management                                           │
│  - Quality assurance                                                     │
└─────────────────────────────┬───────────────────────────────────────────┘
                              │
                              │ Delegates to specialized agents
                              │
              ┌───────────────┼───────────────┐
              │               │               │
              ▼               ▼               ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│   REPOSITORY    │ │   DOCKERFILE    │ │   KUBERNETES    │
│     ANALYZER    │ │    GENERATOR    │ │    ENGINEER     │
│    (GPT-4)      │ │    (GPT-4)      │ │    (GPT-4)      │
│                 │ │                 │ │                 │
│ • Language      │ │ • Multi-stage   │ │ • Deployment    │
│ • Framework     │ │ • Security      │ │ • Service       │
│ • Dependencies  │ │ • Optimization  │ │ • ConfigMap     │
│ • Runtime       │ │ • Health checks │ │ • HPA           │
│ • Build cmds    │ │ • Best practice │ │ • Ingress       │
└────────┬────────┘ └────────┬────────┘ └────────┬────────┘
         │                   │                    │
         │                   │                    │
         └───────────────────┴────────────────────┘
                             │
                             ▼
                   ┌──────────────────┐
                   │  GENERATED       │
                   │  ARTIFACTS       │
                   │                  │
                   │ • Dockerfile     │
                   │ • deployment.yml │
                   │ • service.yml    │
                   │ • configmap.yml  │
                   │ • hpa.yml        │
                   │ • ingress.yml    │
                   └────────┬─────────┘
                            │
                            │ Present to user
                            ▼
                   ┌──────────────────┐
                   │  USER REVIEW &   │
                   │  REFINEMENT      │
                   └────────┬─────────┘
                            │
                            │ Refinement instructions
                            ▼
                   ┌──────────────────┐
                   │  REFINEMENT      │
                   │  SPECIALIST      │
                   │  (GPT-4)         │
                   │                  │
                   │ • Apply changes  │
                   │ • Validate       │
                   │ • Explain impact │
                   └────────┬─────────┘
                            │
                            │ Updated artifacts
                            ▼
                   ┌──────────────────┐
                   │  FINAL OUTPUT    │
                   │                  │
                   │ • Save to files  │
                   │ • Ready to use   │
                   └──────────────────┘
```

## Data Flow Diagram

```
GitHub Repository
       │
       │ API Call
       ▼
   ┌─────────┐
   │ PyGithub│
   └────┬────┘
        │ Repository metadata & files
        ▼
   ┌──────────────────┐
   │ analyze_repository│  ←── Function Tool
   └────┬─────────────┘
        │ RepositoryAnalysis
        ▼
   ┌──────────────────┐
   │generate_dockerfile│  ←── Function Tool
   └────┬─────────────┘
        │ DockerfileArtifact
        ▼
   ┌──────────────────────────┐
   │generate_kubernetes_manifests│  ←── Function Tool
   └────┬─────────────────────┘
        │ KubernetesManifests
        ▼
   ┌──────────────┐
   │ User Review  │
   └────┬─────────┘
        │ Refinement instructions
        ▼
   ┌──────────────┐
   │refine_manifest│  ←── Function Tool
   └────┬─────────┘
        │ Updated artifacts
        ▼
   ┌──────────────┐
   │ Output Files │
   └──────────────┘
```

## Agent Communication Flow

```
┌─────────┐
│  User   │
└────┬────┘
     │ "Generate manifests for owner/repo"
     ▼
┌─────────────────┐
│ Orchestrator    │ ───┐
└────┬────────────┘    │
     │                 │ Handoff
     │                 │
     ├─────────────────┼────────────────┐
     │                 │                │
     ▼                 ▼                ▼
┌──────────┐    ┌──────────┐    ┌──────────┐
│Analyzer  │    │Dockerfile│    │K8s       │
│          │    │Generator │    │Engineer  │
└────┬─────┘    └────┬─────┘    └────┬─────┘
     │               │               │
     │ Analysis      │ Dockerfile    │ Manifests
     └───────────────┴───────────────┘
                     │
                     ▼
              ┌──────────────┐
              │ Orchestrator │
              └──────┬───────┘
                     │ Present results
                     ▼
              ┌──────────┐
              │   User   │
              └──────┬───┘
                     │ Refinement request
                     ▼
              ┌──────────────┐
              │ Orchestrator │ ───┐
              └──────┬───────┘    │
                     │             │ Handoff
                     ▼             ▼
              ┌──────────────┐
              │ Refinement   │
              │ Specialist   │
              └──────┬───────┘
                     │ Updated artifacts
                     ▼
              ┌──────────┐
              │   User   │
              └──────────┘
```

## Component Interaction

```
┌────────────────────────────────────────────────────────────┐
│                    OpenAI Agents SDK                        │
│                                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ Agent 1  │  │ Agent 2  │  │ Agent 3  │  │ Agent 4  │  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  │
│       │             │             │             │         │
│       └─────────────┴─────────────┴─────────────┘         │
│                     │                                      │
│              ┌──────▼──────┐                               │
│              │   Runner    │                               │
│              └──────┬──────┘                               │
└─────────────────────┼───────────────────────────────────────┘
                      │
              ┌───────▼────────┐
              │ DevOpsContext  │
              │                │
              │ - user_id      │
              │ - github_org   │
              │ - github_token │
              │ - metadata     │
              └───────┬────────┘
                      │
         ┌────────────┼────────────┐
         │            │            │
         ▼            ▼            ▼
   ┌─────────┐  ┌─────────┐  ┌─────────┐
   │ GitHub  │  │ Docker  │  │   K8s   │
   │   API   │  │  Image  │  │ Cluster │
   └─────────┘  └─────────┘  └─────────┘
```

## Technology Stack

```
┌─────────────────────────────────────────────────────────┐
│                    Application Layer                     │
│  cd_manifest_generator.py, cd_manifest_demo.py          │
└─────────────────────────┬───────────────────────────────┘
                          │
┌─────────────────────────┴───────────────────────────────┐
│                    Agent Layer                           │
│  - Orchestrator Agent                                    │
│  - Repository Analyzer Agent                             │
│  - Dockerfile Generator Agent                            │
│  - Kubernetes Engineer Agent                             │
│  - Refinement Specialist Agent                           │
└─────────────────────────┬───────────────────────────────┘
                          │
┌─────────────────────────┴───────────────────────────────┐
│                    Framework Layer                       │
│  - OpenAI Agents SDK (multi-agent orchestration)         │
│  - GPT-4 (language model)                                │
│  - Pydantic (data validation)                            │
└─────────────────────────┬───────────────────────────────┘
                          │
┌─────────────────────────┴───────────────────────────────┐
│                    Integration Layer                     │
│  - PyGithub (GitHub API)                                 │
│  - PyYAML (YAML generation)                              │
│  - Requests (HTTP client)                                │
└─────────────────────────┬───────────────────────────────┘
                          │
┌─────────────────────────┴───────────────────────────────┐
│                    External Services                     │
│  - GitHub API (repository data)                          │
│  - OpenAI API (GPT-4)                                    │
└─────────────────────────────────────────────────────────┘
```

## Workflow Sequence

```
1. User Input
   ├─ Repository: owner/repo
   ├─ Branch: main
   ├─ App name: myapp
   ├─ Replicas: 3
   └─ Domain: app.example.com

2. Initialization
   ├─ Create DevOpsContext
   ├─ Set up GitHub credentials
   └─ Initialize 5 agents

3. Analysis Phase
   ├─ Orchestrator delegates to Analyzer
   ├─ Analyzer fetches repo via PyGithub
   ├─ Detect language, framework, runtime
   ├─ Find dependencies and build commands
   └─ Return RepositoryAnalysis

4. Generation Phase
   ├─ Orchestrator delegates to Dockerfile Generator
   │  ├─ Use analysis results
   │  ├─ Generate multi-stage Dockerfile
   │  └─ Return DockerfileArtifact
   │
   └─ Orchestrator delegates to K8s Engineer
      ├─ Use analysis results
      ├─ Generate Deployment, Service, ConfigMap
      ├─ Generate HPA, Ingress (if requested)
      └─ Return KubernetesManifests

5. Presentation Phase
   ├─ Orchestrator presents all artifacts
   └─ Show explanations and best practices

6. Refinement Phase (Loop)
   ├─ User provides refinement instructions
   ├─ Orchestrator delegates to Refinement Specialist
   ├─ Apply modifications
   ├─ Present updated artifacts
   └─ Repeat until user says "done"

7. Output Phase
   ├─ Save Dockerfile
   ├─ Save k8s-deployment.yaml
   ├─ Save k8s-service.yaml
   ├─ Save k8s-configmap.yaml
   ├─ Save k8s-hpa.yaml (if enabled)
   └─ Save k8s-ingress.yaml (if enabled)
```

## Security Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Security Layers                       │
└─────────────────────────┬───────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Dockerfile   │  │ Kubernetes   │  │   Runtime    │
│  Security    │  │   Security   │  │   Security   │
│              │  │              │  │              │
│• Non-root    │  │• PodSecurity │  │• Secrets     │
│  user        │  │  Context     │  │  management  │
│• Minimal     │  │• Resource    │  │• Network     │
│  base image  │  │  limits      │  │  policies    │
│• No secrets  │  │• RBAC ready  │  │• Monitoring  │
│  in image    │  │• Network     │  │• Logging     │
│• Layer       │  │  policies    │  │• Auditing    │
│  optimization│  │• TLS/HTTPS   │  │              │
└──────────────┘  └──────────────┘  └──────────────┘
```

## Scalability Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Scalability Features                  │
└─────────────────────────┬───────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Application  │  │ Kubernetes   │  │ Monitoring   │
│  Level       │  │   Level      │  │              │
│              │  │              │  │              │
│• Multi-stage │  │• HPA         │  │• Metrics     │
│  build       │  │  (auto-scale)│  │  collection  │
│• Optimized   │  │• Rolling     │  │• Dashboards  │
│  image size  │  │  updates     │  │• Alerts      │
│• Health      │  │• Resource    │  │• Logs        │
│  checks      │  │  limits      │  │  aggregation │
│• Stateless   │  │• Multiple    │  │• Tracing     │
│  design      │  │  replicas    │  │              │
└──────────────┘  └──────────────┘  └──────────────┘
```

## File Output Structure

```
output/
└── {app-name}/
    ├── Dockerfile
    ├── k8s-deployment.yaml
    ├── k8s-service.yaml
    ├── k8s-configmap.yaml
    ├── k8s-hpa.yaml
    └── k8s-ingress.yaml
```

## Key Technologies Matrix

| Component          | Technology        | Purpose                  |
| ------------------ | ----------------- | ------------------------ |
| AI/ML              | GPT-4             | Reasoning & generation   |
| Orchestration      | OpenAI Agents SDK | Multi-agent coordination |
| Data Validation    | Pydantic          | Type safety & validation |
| GitHub Integration | PyGithub          | Repository access        |
| YAML Generation    | PyYAML            | Manifest creation        |
| HTTP Client        | Requests          | API calls                |
| CLI                | Python asyncio    | Interactive interface    |

## Agent Capabilities Matrix

| Agent                 | Primary Function      | Tools Used                    | Output                |
| --------------------- | --------------------- | ----------------------------- | --------------------- |
| Orchestrator          | Workflow coordination | All agents                    | Coordinated execution |
| Analyzer              | Repository analysis   | analyze_repository            | RepositoryAnalysis    |
| Dockerfile Generator  | Docker config         | generate_dockerfile           | DockerfileArtifact    |
| K8s Engineer          | K8s manifests         | generate_kubernetes_manifests | KubernetesManifests   |
| Refinement Specialist | Artifact modification | refine_manifest               | Updated artifacts     |

---

**Architecture designed for scalability, security, and maintainability**
