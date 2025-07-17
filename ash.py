# ash.py

import typer
from cli.backend import generate_backend

app = typer.Typer(help="Ash CLI - Generate full-stack apps from entity definitions.")

@app.command()
def genapp(
    mode: str = typer.Argument(..., help="What to generate: backend / frontend / deploy"),
    file: str = typer.Option(..., "--file", "-f", help="Path to entity definition file (YAML/JSON)"),
    language: str = typer.Option(..., "--language", "-l", help="Programming language (java, python, go, ts)"),
    project_name: str = typer.Option(..., "--project-name", "-p", help="Name of the generated project"),
    deploy_aws: bool = typer.Option(False, "--deploy-aws", help="Enable AWS deployment support"),
    auth: str = typer.Option("jwt", "--auth", help="Authentication method: jwt / oauth / sso"),
    resume: bool = typer.Option(False, "--resume", help="Resume from previous failed step"),
    docker: bool = typer.Option(False, "--docker", "-d", help="Include Dockerfile and .dockerignore"),
):
    """
    Generates a backend or frontend application based on entity config.
    """
    if mode == "backend":
        generate_backend(file, language, project_name, deploy_aws, auth, resume, docker)
    elif mode == "frontend":
        typer.echo("Frontend generation is not yet implemented.")
    elif mode == "deploy":
        typer.echo("Deployment scaffolding is not yet implemented.")
    else:
        typer.echo(f"[ERROR] Unsupported mode: {mode}")

if __name__ == "__main__":
    app()