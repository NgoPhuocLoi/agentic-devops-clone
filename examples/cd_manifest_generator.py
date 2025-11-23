"""
Multi-Agent CD Manifest Generator - Generates Dockerfile and Kubernetes deployment manifests.

This example demonstrates using OpenAI Agents SDK to create a multi-agent system that:
1. Analyzes a GitHub repository to understand its structure and requirements
2. Generates an optimized Dockerfile
3. Creates Kubernetes deployment manifests
4. Allows user to fine-tune the generated artifacts

The system uses specialized agents for each task, coordinated by an orchestrator.
Agents generate actual manifest content directly without boilerplate functions.
"""

import os
import asyncio
import re
from pathlib import Path
from typing import Optional

from agents import Agent, Runner, function_tool

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'agentic_devops'))

from src.core import DevOpsContext


def extract_code_blocks(text: str) -> dict:
    """
    Extract code blocks from agent response.
    Returns dict with filenames as keys and content as values.
    """
    artifacts = {}
    
    # Pattern to match code blocks with optional filename
    # Matches: ```dockerfile, ```yaml, ```Dockerfile, etc.
    pattern = r'```(\w+)?\s*(?:#\s*(.+?))?\n(.*?)```'
    matches = re.finditer(pattern, text, re.DOTALL)
    
    for match in matches:
        lang = match.group(1) or ''
        filename = match.group(2) or ''
        content = match.group(3).strip()
        
        # Determine artifact type
        if 'dockerfile' in lang.lower() or 'Dockerfile' in filename:
            artifacts['Dockerfile'] = content
        elif 'yaml' in lang.lower() or 'yml' in lang.lower():
            # Try to determine K8s resource type from content
            if 'kind: Deployment' in content:
                artifacts['k8s-deployment.yaml'] = content
            elif 'kind: Service' in content:
                artifacts['k8s-service.yaml'] = content
            elif 'kind: ConfigMap' in content:
                artifacts['k8s-configmap.yaml'] = content
            elif 'kind: HorizontalPodAutoscaler' in content:
                artifacts['k8s-hpa.yaml'] = content
            elif 'kind: Ingress' in content:
                artifacts['k8s-ingress.yaml'] = content
            elif filename:
                artifacts[filename] = content
            else:
                # Generic yaml file
                artifacts[f'manifest-{len(artifacts)}.yaml'] = content
    
    return artifacts


def save_artifacts(artifacts: dict, output_dir: Path) -> None:
    """Save artifacts to files."""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for filename, content in artifacts.items():
        filepath = output_dir / filename
        filepath.write_text(content)
        print(f"   ✅ Saved: {filename}")

@function_tool
async def determine_language_framework(repo_url: str, branch: str) -> Optional[dict]:
    """
    Analyze a GitHub repository to determine language, framework, and deployment requirements.
    
    Args:
        repo_url: GitHub repository URL (e.g., https://github.com/owner/repo)
        branch: Branch to analyze
        
    Returns:
        Dictionary with language, framework, version, dependencies_file, start_command, port
    """
    import requests
    import json
    
    # Extract owner and repo from URL
    parts = repo_url.rstrip('/').split('/')
    owner = parts[-2]
    repo_name = parts[-1]
    
    github_token = os.environ.get('GITHUB_TOKEN')
    headers = {'Authorization': f'token {github_token}'} if github_token else {}
    
    api_base = f"https://api.github.com/repos/{owner}/{repo_name}"
    
    try:
        # Get repository info
        repo_response = requests.get(api_base, headers=headers, timeout=10)
        if repo_response.status_code != 200:
            print(f"⚠️  Could not fetch repo info: {repo_response.status_code}")
            return None
        
        repo_data = repo_response.json()
        primary_language = repo_data.get('language', 'Unknown')
        
        # Get repository contents
        contents_url = f"{api_base}/contents?ref={branch}"
        contents_response = requests.get(contents_url, headers=headers, timeout=10)
        
        if contents_response.status_code != 200:
            print(f"⚠️  Could not fetch repo contents: {contents_response.status_code}")
            return None
        
        files = contents_response.json()
        file_names = [f['name'].lower() for f in files if f['type'] == 'file']
        
        result = {
            "language": primary_language,
            "framework": None,
            "version": None,
            "dependencies_file": None,
            "start_command": None,
            "port": 8080,
            "build_command": None
        }
        
        # Python detection
        if "requirements.txt" in file_names:
            result["dependencies_file"] = "requirements.txt"
            result["language"] = "Python"
            result["version"] = "3.11"
            result["port"] = 5000
            
            # Try to detect framework from requirements.txt
            try:
                req_url = f"{api_base}/contents/requirements.txt?ref={branch}"
                req_response = requests.get(req_url, headers=headers, timeout=10)
                if req_response.status_code == 200:
                    import base64
                    content = base64.b64decode(req_response.json()['content']).decode('utf-8').lower()
                    
                    if "flask" in content:
                        result["framework"] = "Flask"
                        result["start_command"] = "python app.py"
                        result["port"] = 5000
                    elif "fastapi" in content:
                        result["framework"] = "FastAPI"
                        result["start_command"] = "uvicorn main:app --host 0.0.0.0 --port 8000"
                        result["port"] = 8000
                    elif "django" in content:
                        result["framework"] = "Django"
                        result["start_command"] = "python manage.py runserver 0.0.0.0:8000"
                        result["port"] = 8000
            except Exception as e:
                print(f"⚠️  Could not analyze requirements.txt: {e}")
        
        elif "pyproject.toml" in file_names:
            result["dependencies_file"] = "pyproject.toml"
            result["language"] = "Python"
            result["version"] = "3.11"
            result["build_command"] = "pip install poetry && poetry install"
        
        # Node.js detection
        elif "package.json" in file_names:
            result["dependencies_file"] = "package.json"
            result["language"] = "JavaScript"
            result["version"] = "18"
            result["port"] = 3000
            
            # Try to detect framework from package.json
            try:
                pkg_url = f"{api_base}/contents/package.json?ref={branch}"
                pkg_response = requests.get(pkg_url, headers=headers, timeout=10)
                if pkg_response.status_code == 200:
                    import base64
                    content = base64.b64decode(pkg_response.json()['content']).decode('utf-8')
                    pkg_data = json.loads(content)
                    
                    deps = {**pkg_data.get('dependencies', {}), **pkg_data.get('devDependencies', {})}
                    scripts = pkg_data.get('scripts', {})
                    
                    if "express" in deps:
                        result["framework"] = "Express"
                        result["start_command"] = scripts.get('start', 'node index.js')
                    elif "next" in deps:
                        result["framework"] = "Next.js"
                        result["build_command"] = "npm run build"
                        result["start_command"] = "npm start"
                    elif "react" in deps and "react-scripts" in deps:
                        result["framework"] = "React"
                        result["build_command"] = "npm run build"
                    elif "vue" in deps:
                        result["framework"] = "Vue"
                        result["build_command"] = "npm run build"
            except Exception as e:
                print(f"⚠️  Could not analyze package.json: {e}")
        
        # Java detection
        elif "pom.xml" in file_names:
            result["dependencies_file"] = "pom.xml"
            result["language"] = "Java"
            result["framework"] = "Spring Boot"
            result["version"] = "17"
            result["build_command"] = "mvn clean package"
            result["start_command"] = "java -jar target/*.jar"
            result["port"] = 8080
        
        elif "build.gradle" in file_names:
            result["dependencies_file"] = "build.gradle"
            result["language"] = "Java"
            result["framework"] = "Spring Boot"
            result["version"] = "17"
            result["build_command"] = "gradle build"
            result["start_command"] = "java -jar build/libs/*.jar"
            result["port"] = 8080
        
        # Go detection
        elif "go.mod" in file_names:
            result["dependencies_file"] = "go.mod"
            result["language"] = "Go"
            result["framework"] = "Go"
            result["version"] = "1.21"
            result["build_command"] = "go build -o app ."
            result["start_command"] = "./app"
            result["port"] = 8080
        
        # Default start command if not set
        if not result["start_command"]:
            if result["language"] == "Python":
                result["start_command"] = "python main.py"
            elif result["language"] == "JavaScript":
                result["start_command"] = "node index.js"
        
        return result
        
    except requests.RequestException as e:
        print(f"⚠️  Network error analyzing repository: {e}")
        return None
    except Exception as e:
        print(f"⚠️  Error analyzing repository: {e}")
        return None


async def main():
    """Run the CD Manifest Generator multi-agent system."""
    
    # Check for required environment variables
    if "OPENAI_API_KEY" not in os.environ:
        print("❌ Error: Please set the OPENAI_API_KEY environment variable")
        print("   export OPENAI_API_KEY='your-api-key-here'")
        return
    
    print("=" * 80)
    print("🚀 CD Manifest Generator - Multi-Agent System")
    print("=" * 80)
    print()
    
    # Get user input
    print("Enter GitHub repository details:")
    owner = input("  Repository owner (e.g., 'pallets'): ").strip()
    repo = input("  Repository name (e.g., 'flask'): ").strip()
    branch = input("  Branch (default: 'main'): ").strip() or "main"
    
    if not owner or not repo:
        print("❌ Error: Owner and repository name are required")
        return
    
    # Get optional parameters
    app_name = input("\nApplication name for K8s (default: repo name): ").strip() or repo
    replicas = input("Number of replicas (default: 3): ").strip()
    replicas = int(replicas) if replicas.isdigit() else 3
    
    domain = input("Domain for Ingress (optional, e.g., 'app.example.com'): ").strip() or None
    
    print("\n" + "=" * 80)
    print("🤖 Initializing agents...")
    print("=" * 80)
    
    # Create DevOps context
    context = DevOpsContext(
        user_id="manifest-generator-user",
        github_org=owner
    )
    
    # Add GitHub token if available
    if "GITHUB_TOKEN" in os.environ:
        context.github_token = os.environ["GITHUB_TOKEN"]
    
    # ========================================================================
    # Create Specialized Agents
    # ========================================================================
    
    # Agent 1: Repository Analyzer
    analyzer_agent = Agent(
        name="Repository Analyzer",
        instructions="""
        You are an expert at analyzing GitHub repositories to understand their structure and deployment requirements.
        
        When analyzing a repository, determine:
        - Programming language and version
        - Framework (Flask, Express, Spring Boot, etc.)
        - Dependencies file (requirements.txt, package.json, pom.xml, etc.)
        - Build commands if needed
        - Start/run command
        - Application port
        - Any special requirements
        
        Access the repository as a public GitHub repo. Then determine and anwser which language and framework it uses.
        """,
        tools=[determine_language_framework],
        model="gpt-4o"
    )
    
    # Agent 2: Dockerfile Generator
    dockerfile_agent = Agent(
        name="Dockerfile Generator",
        instructions="""
        You are a Docker expert who creates production-ready, optimized Dockerfiles.
        
        Generate a complete Dockerfile following these principles:
        - Use multi-stage builds when appropriate
        - Use minimal base images (alpine, slim, or scratch)
        - Run as non-root user (UID 1000)
        - Include health checks
        - Optimize layer caching
        - Add security best practices
        
        Output the Dockerfile in a code block marked with ```dockerfile
        Include comments explaining key decisions.
        """,
        model="gpt-4o"
    )
    
    # Agent 3: Kubernetes Engineer
    k8s_agent = Agent(
        name="Kubernetes Engineer",
        instructions="""
        You are a Kubernetes expert who creates production-grade deployment manifests.
        
        Generate complete, ready-to-use Kubernetes YAML manifests:
        1. Deployment (with replicas, resources, health probes, security context)
        2. Service (ClusterIP type)
        3. ConfigMap (for app configuration)
        4. HorizontalPodAutoscaler (if requested)
        5. Ingress (if domain provided, with TLS)
        
        Each manifest should be in its own ```yaml code block with a comment indicating the resource type.
        Follow Kubernetes best practices:
        - Resource limits and requests
        - Liveness and readiness probes
        - Security contexts (runAsNonRoot, runAsUser: 1000)
        - Proper labels and selectors
        """,
        model="gpt-4o"
    )
    
    # Agent 4: Orchestrator
    orchestrator_agent = Agent(
        name="DevOps Orchestrator",
        instructions="""
        You coordinate specialized agents to generate deployment artifacts from GitHub repositories.
        
        Your workflow:
        1. First, analyze the repository to understand its structure
        2. Then delegate Dockerfile generation
        3. Then delegate Kubernetes manifest generation
        4. Present all artifacts clearly
        5. Handle user refinements if requested
        
        Always present generated artifacts in properly formatted code blocks.
        Be helpful and explain what was generated.
        """,
        tools=[
            analyzer_agent.as_tool(
                tool_name="analyze_repository",
                tool_description="Analyze GitHub repository structure and requirements"
            ),
            dockerfile_agent.as_tool(
                tool_name="generate_dockerfile",
                tool_description="Generate a production-ready Dockerfile"
            ),
            k8s_agent.as_tool(
                tool_name="generate_kubernetes_manifests",
                tool_description="Generate Kubernetes deployment manifests"
            )
        ],
        model="gpt-4o"
    )
    
    # ========================================================================
    # Run the orchestrator
    # ========================================================================
    print("\n📊 Analyzing repository and generating artifacts...")
    print("-" * 80)
    
    repo_url = f"https://github.com/{owner}/{repo}"
    
    initial_query = f"""
    Generate deployment artifacts for the GitHub repository: {owner}/{repo}
    - Branch: {branch}
    - Repository URL: {repo_url}
    - Application name: {app_name}
    - Replicas: {replicas}
    {f"- Domain: {domain} (enable Ingress with TLS)" if domain else "- No Ingress needed"}
    
    Please:
    1. Analyze the repository structure (you can reference it as a public GitHub repo)
    2. Generate a production-ready Dockerfile with multi-stage build
    3. Generate complete Kubernetes manifests (Deployment, Service, ConfigMap{", HPA" if replicas > 1 else ""}{", Ingress" if domain else ""})
    
    Output each artifact in properly formatted code blocks with appropriate language tags.
    """
    
    print(f"\n🎯 Processing: {owner}/{repo}")
    print()
    
    try:
        result = await Runner.run(
            orchestrator_agent,
            initial_query,
            context=context
        )
        
        final_output = result.final_output
        
        print("\n" + "=" * 80)
        print("✅ GENERATION COMPLETE")
        print("=" * 80)
        print("\n" + final_output)
        
        # Extract artifacts from the response
        print("\n" + "=" * 80)
        print("📦 Extracting artifacts...")
        print("=" * 80)
        
        artifacts = extract_code_blocks(final_output)
        
        if artifacts:
            print(f"\n✅ Found {len(artifacts)} artifact(s):")
            for filename in artifacts.keys():
                print(f"   - {filename}")
        else:
            print("\n⚠️  No artifacts found in code blocks. Attempting to parse response...")
            # Fallback: look for common patterns
            if "FROM" in final_output and ("RUN" in final_output or "COPY" in final_output):
                print("   Found Dockerfile-like content")
            if "apiVersion:" in final_output and "kind:" in final_output:
                print("   Found Kubernetes manifest-like content")
        
        # Interactive refinement loop
        print("\n" + "=" * 80)
        print("🔧 REFINEMENT PHASE")
        print("=" * 80)
        print("\nYou can now fine-tune the generated artifacts.")
        print("Type your refinement instructions or 'done' to finish.")
        print("\nExamples:")
        print("  - Change Python version to 3.12")
        print("  - Increase memory limit to 1Gi")
        print("  - Add Redis as a dependency")
        print("  - Change replicas to 5")
        print()
        
        while True:
            refinement = input("\n💬 Refinement (or 'done'): ").strip()
            
            if refinement.lower() in ['done', 'exit', 'quit', '']:
                break
            
            print(f"\n🔄 Applying refinement...")
            refinement_result = await Runner.run(
                orchestrator_agent,
                f"Please update the artifacts based on this instruction: {refinement}\n\nProvide the updated artifacts in code blocks.",
                context=context
            )
            
            refinement_output = refinement_result.final_output
            print("\n" + refinement_output)
            
            # Update artifacts with refined versions
            new_artifacts = extract_code_blocks(refinement_output)
            if new_artifacts:
                artifacts.update(new_artifacts)
                print(f"\n✅ Updated {len(new_artifacts)} artifact(s)")
        
        print("\n" + "=" * 80)
        print("✨ All done! Your deployment artifacts are ready.")
        print("=" * 80)
        
        # Save artifacts option
        if artifacts:
            save = input("\n💾 Save artifacts to files? (y/n): ").strip().lower()
            if save == 'y':
                output_dir = Path(f"./output/{app_name}")
                
                print(f"\n📁 Saving to: {output_dir}")
                save_artifacts(artifacts, output_dir)
                
                print("\n✅ All artifacts saved successfully!")
                print(f"\nTo deploy:")
                print(f"  1. Build: docker build -t {app_name}:latest .")
                print(f"  2. Push: docker push <registry>/{app_name}:latest")
                print(f"  3. Deploy: kubectl apply -f {output_dir}/")
        else:
            print("\n⚠️  No artifacts were extracted to save.")
            print("The generated content is shown above. You can manually copy it.")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


# ============================================================================
# Entry Point
# ============================================================================

if __name__ == "__main__":
    print("\n🎯 Multi-Agent CD Manifest Generator")
    print("   Powered by OpenAI Agents SDK\n")
    
    asyncio.run(main())
