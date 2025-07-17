# core/java/project_files/docker_generator.py

from pathlib import Path

DOCKERFILE_TEMPLATE = """\
FROM eclipse-temurin:17-jdk-alpine

WORKDIR /app

COPY target/*.jar app.jar

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "app.jar"]
"""

DOCKERIGNORE_TEMPLATE = """\
target/
.idea/
*.iml
*.log
*.md
*.yaml
*.yml
*.json
*.py
__pycache__/
*.pyc
"""

DOCKER_COMPOSE_TEMPLATE = """\
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8080:8080"
    depends_on:
      - db
    environment:
      SPRING_DATASOURCE_URL: jdbc:postgresql://db:5432/{db_name}
      SPRING_DATASOURCE_USERNAME: {db_user}
      SPRING_DATASOURCE_PASSWORD: {db_password}
    networks:
      - ashnet

  db:
    image: postgres:15
    container_name: postgres-db
    restart: always
    environment:
      POSTGRES_DB: {db_name}
      POSTGRES_USER: {db_user}
      POSTGRES_PASSWORD: {db_password}
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
    networks:
      - ashnet

volumes:
  pgdata:

networks:
  ashnet:
    driver: bridge
"""

def generate_docker_files(output_path: str, logger, db_name: str = "appdb", db_user: str = "postgres", db_password: str = "password"):
    project_path = Path(output_path)

    # Dockerfile
    dockerfile = project_path / "Dockerfile"
    dockerfile.write_text(DOCKERFILE_TEMPLATE)
    logger.debug(f"🐳 Dockerfile created at {dockerfile}")

    # .dockerignore
    dockerignore = project_path / ".dockerignore"
    dockerignore.write_text(DOCKERIGNORE_TEMPLATE)
    logger.debug(f"📄 .dockerignore created at {dockerignore}")

    # docker-compose.yml
    compose = project_path / "docker-compose.yml"
    compose.write_text(DOCKER_COMPOSE_TEMPLATE.format(
        db_name=db_name,
        db_user=db_user,
        db_password=db_password
    ))
    logger.debug(f"🔧 docker-compose.yml created at {compose}")