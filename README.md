# NYC Taxi Data Pipeline

[![NYC Taxi Data Pipeline CI/CD](https://github.com/yourusername/first_tryout/actions/workflows/main.yml/badge.svg)](https://github.com/yourusername/first_tryout/actions/workflows/main.yml)

A data pipeline that downloads NYC taxi trip data, processes it with Pandas and PyArrow, and loads it into a PostgreSQL database.

## Features

- Downloads NYC taxi trip data parquet files
- Processes data with Pandas and PyArrow
- Loads data into PostgreSQL database
- Containerized with Docker and Docker Compose
- CI/CD pipeline with GitHub Actions
- Poetry for dependency management

## Project Structure

```
├── .github/
│   └── workflows/
│       └── main.yml       # GitHub Actions workflow file
├── tests/
│   └── test_critical.py   # Unit tests
├── Dockerfile             # Docker image definition
├── .dockerignore          # Docker ignore file
├── pyproject.toml         # Poetry configuration
├── poetry.lock            # Poetry lock file
├── critical.py            # Main data processing script
├── docker-compose.yaml    # Container orchestration
└── README.md              # Project documentation
```

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.10+
- Poetry (for development)
- Git

### Development Setup

1. Clone the repository
2. Install dependencies with Poetry:

```bash
poetry install
```

3. Run tests:

```bash
poetry run pytest
```

### Running Locally

Run the application with Docker Compose:

```bash
docker-compose up
```

### CI/CD Pipeline

The project includes a CI/CD pipeline that:

1. Lints and tests the code with Poetry
2. Builds and pushes the Docker image (on main branch)
3. Deploys to production (placeholder for actual deployment)

## Environment Variables

To use this project with the CI/CD pipeline, you need to set up the following GitHub secrets:

- `DOCKER_HUB_USERNAME`: Your Docker Hub username
- `DOCKER_HUB_TOKEN`: Your Docker Hub access token

## License

This project is licensed under the MIT License - see the LICENSE file for details