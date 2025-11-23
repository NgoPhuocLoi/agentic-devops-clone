"""
Simple demo script for CD Manifest Generator

This script demonstrates programmatic usage of the multi-agent system
to generate Dockerfile and Kubernetes manifests for a GitHub repository.
"""

import os
import asyncio
import sys
import re
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'agentic_devops'))

from agents import Agent, Runner
from src.core import DevOpsContext


def extract_code_blocks(text: str) -> dict:
    """Extract code blocks from agent response."""
    artifacts = {}
    pattern = r'```(\w+)?\s*(?:#\s*(.+?))?\n(.*?)```'
    matches = re.finditer(pattern, text, re.DOTALL)
    
    for match in matches:
        lang = match.group(1) or ''
        filename = match.group(2) or ''
        content = match.group(3).strip()
        
        if 'dockerfile' in lang.lower():
            artifacts['Dockerfile'] = content
        elif 'yaml' in lang.lower() or 'yml' in lang.lower():
            if 'kind: Deployment' in content:
                artifacts['k8s-deployment.yaml'] = content
            elif 'kind: Service' in content:
                artifacts['k8s-service.yaml'] = content
            elif 'kind: ConfigMap' in content:
                artifacts['k8s-configmap.yaml'] = content
            elif 'kind: HorizontalPodAutoscaler' in content:
                artifacts['k8s-hpa.yaml'] = content
    
    return artifacts


async def generate_manifests(owner: str, repo: str, branch: str = "main"):
    """
    Generate Dockerfile and K8s manifests for a GitHub repository.
    
    Args:
        owner: Repository owner
        repo: Repository name
        branch: Branch to analyze (default: main)
    """
    print(f"\n{'='*80}")
    print(f"🚀 Generating manifests for {owner}/{repo}")
    print(f"{'='*80}\n")
    
    # Create context
    context = DevOpsContext(
        user_id="demo-user",
        github_org=owner
    )
    
    # Add GitHub token if available
    if "GITHUB_TOKEN" in os.environ:
        context.github_token = os.environ["GITHUB_TOKEN"]
    
    # Create agents
    analyzer = Agent(
        name="Repository Analyzer",
        instructions="Analyze GitHub repositories to understand their structure and requirements.",
        model="gpt-4o"
    )
    
    dockerfile_gen = Agent(
        name="Dockerfile Generator",
        instructions="""Generate production-ready Dockerfiles with multi-stage builds.
        Output in ```dockerfile code blocks.""",
        model="gpt-4o"
    )
    
    k8s_gen = Agent(
        name="Kubernetes Engineer",
        instructions="""Generate complete Kubernetes manifests.
        Output each in separate ```yaml code blocks.""",
        model="gpt-4o"
    )
    
    orchestrator = Agent(
        name="Manifest Generator",
        instructions="""Coordinate agents to generate deployment artifacts.
        Present all artifacts in properly formatted code blocks.""",
        handoffs=[
            {"agent": analyzer, "description": "Analyzes repositories"},
            {"agent": dockerfile_gen, "description": "Generates Dockerfiles"},
            {"agent": k8s_gen, "description": "Creates K8s manifests"}
        ],
        model="gpt-4o"
    )
    
    query = f"""
    Generate deployment artifacts for {owner}/{repo} (branch: {branch}):
    
    1. Dockerfile - Production-ready with multi-stage build
    2. Kubernetes Deployment (3 replicas)
    3. Kubernetes Service
    4. Kubernetes ConfigMap
    5. Kubernetes HPA
    
    Output each in code blocks with appropriate language tags.
    """
    
    try:
        result = await Runner.run(orchestrator, query, context=context)
        
        print("\n" + "="*80)
        print("✅ GENERATION COMPLETE")
        print("="*80)
        print("\n" + result.final_output)
        
        # Extract and show artifacts
        artifacts = extract_code_blocks(result.final_output)
        if artifacts:
            print(f"\n📦 Extracted {len(artifacts)} artifact(s):")
            for name in artifacts.keys():
                print(f"   - {name}")
        
        return result
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None


async def main():
    """Run the demo."""
    
    # Check for required environment variables
    if "OPENAI_API_KEY" not in os.environ:
        print("❌ Error: Please set the OPENAI_API_KEY environment variable")
        print("   export OPENAI_API_KEY='your-api-key-here'")
        return
    
    print("\n🎯 CD Manifest Generator - Simple Demo")
    print("   Powered by OpenAI Agents SDK\n")
    
    # Example repositories to test
    examples = [
        ("pallets", "flask", "main"),  # Python Flask
        # ("vercel", "next.js", "canary"),  # Next.js (large repo, commented out)
        # ("spring-projects", "spring-boot", "main"),  # Spring Boot (large repo)
    ]
    
    # Get user input or use example
    use_example = input("Use example repository (Flask)? (y/n): ").strip().lower()
    
    if use_example == 'y':
        owner, repo, branch = examples[0]
        print(f"\n📦 Using example: {owner}/{repo} (branch: {branch})")
    else:
        owner = input("Repository owner: ").strip()
        repo = input("Repository name: ").strip()
        branch = input("Branch (default: main): ").strip() or "main"
    
    if not owner or not repo:
        print("❌ Error: Owner and repository name are required")
        return
    
    # Generate manifests
    await generate_manifests(owner, repo, branch)
    
    print("\n" + "="*80)
    print("✨ Demo complete!")
    print("="*80)
    print("\nTo save artifacts and enable refinement, use the full version:")
    print("  python cd_manifest_generator.py")
    print()


if __name__ == "__main__":
    asyncio.run(main())
