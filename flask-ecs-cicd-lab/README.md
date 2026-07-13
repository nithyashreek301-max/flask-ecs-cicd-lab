# Flask ECS CI/CD Lab

A containerized Flask application deployed to **AWS ECS Fargate** via two complete CI/CD pipelines.

## Project Structure

```
flask-ecs-cicd-lab/
├── app.py              # Flask application (/ and /health endpoints)
├── requirements.txt    # Python dependencies
├── Dockerfile          # Container image definition
├── .dockerignore       # Files excluded from Docker build context
├── Jenkinsfile         # Pipeline A — Jenkins CI/CD
├── buildspec.yml       # Pipeline B — AWS CodeBuild (used by CodePipeline)
├── .gitignore
└── README.md
```

## Architecture

```
GitHub Push
    │
    ├──► Jenkins (EC2 t2.micro)          ──► ECR ──► ECS Fargate
    │     Jenkinsfile pipeline                        flask-ecs-cluster
    │     [Checkout → Build → Trivy → Push → Deploy]
    │
    └──► AWS CodePipeline                ──► ECR ──► ECS Fargate
          buildspec.yml pipeline                      flask-ecs-cluster
          [Source → CodeBuild → ECS Deploy]
```

## CI/CD Stages (both pipelines)

| Stage | What happens |
|---|---|
| Source | GitHub push triggers pipeline automatically |
| Build | `docker build` creates image tagged with build number / commit SHA |
| Scan | Trivy scans for HIGH/CRITICAL CVEs — pipeline fails if found |
| Push | Image pushed to ECR with versioned tag + `latest` |
| Deploy | ECS service updated, waits for tasks to be healthy |

## Before You Use This Repo

Replace the following placeholders in `Jenkinsfile` and `buildspec.yml`:

- `<YOUR_AWS_ACCOUNT_ID>` → your 12-digit AWS account ID
- `<YOUR_GITHUB_USERNAME>` → your GitHub username (Jenkinsfile only)

## Application Endpoints

| Endpoint | Response |
|---|---|
| `GET /` | HTML page showing version and deploy method |
| `GET /health` | JSON `{"status": "healthy"}` — used by ECS health checks |

## Tech Stack

- **App**: Python / Flask / Gunicorn
- **Container**: Docker (non-root user, layer-cached builds)
- **Registry**: AWS ECR (private, scan on push enabled)
- **Orchestration**: AWS ECS Fargate
- **Pipeline A**: Jenkins (self-hosted on EC2, Jenkinsfile)
- **Pipeline B**: AWS CodePipeline + CodeBuild (buildspec.yml)
- **Security**: Trivy image scanning, IAM instance roles (no stored keys)
