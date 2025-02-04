# Tri-Api


**Tri-Api** is a FastAPI-based SaaS platform demonstration that serves as a central hub for security automation. It provides a suite of cybersecurity tools to enhance software security, manage cloud security configurations, and analyze attack surfaces.



## Features

- **FastAPI-powered:** Leverages FastAPI for high-performance API development.
- **Asynchronous Task Management:** Utilizes Celery and RabbitMQ for efficient background task execution.
- **Database Support:** Integrates with MongoDB for storing and managing security-related data.
- **Comprehensive Security Suite:** Offers tools for software security, cloud security, and attack surface analysis.



## Security Tools

Our suite of cybersecurity tools includes:

- **Software Bill of Materials (SBOM):** Generates an inventory of software components to ensure supply chain security.
- **Software Composition Analysis (SCA):** Identifies vulnerabilities in open-source dependencies.
- **Static Application Security Testing (SAST):** Analyzes source code for security vulnerabilities without executing the program.
- **Cloud Security Posture Management (CSPM):** Monitors and secures cloud configurations.
- **Attack Surface Analysis:** Evaluates system exposure and generates security findings.
- **Attack Surface Discovery:** Identifies assets exposed to potential threats.
- **Dynamic Application Security Testing (DAST):** Detects vulnerabilities in running applications.
- **Secret Exposure Analysis:** Scans codebases for hardcoded secrets and credentials.



## Project Structure

The project is organized as follows:

```
📁 tri_api
│   ├── 📁 authorization
│   │   ├── __init__.py
│   │   ├── json_web_token.py
│   ├── 📁 aws
│   │   ├── __init__.py
│   │   ├── utils.py
│   ├── 📁 celery
│   │   ├── __init__.py
│   │   ├── app.py
│   │   ├── tasks.py
│   ├── 📁 core
│   │   ├── __init__.py
│   │   ├── logger.py
│   ├── 📁 models
│   │   ├── 📁 scanner
│   │   ├── 📁 super
│   │   ├── 📁 tenant
│   │   │   ├── authorization.py
│   │   │   ├── tenant.py
│   │   │   ├── user.py
│   │   ├── 📁 trove
│   │       ├── cve.py
│   │       ├── taxonomy.py
│   ├── 📁 mongo
│   │   ├── __init__.py
│   │   ├── connection.py
│   ├── 📁 rabbitmq
│   │   ├── __init__.py
│   │   ├── connections.py
│   ├── 📁 routes
│   │   ├── 📁 scanner
│   │   ├── 📁 super
│   │   ├── 📁 tenant
│   │   ├── 📁 trove
│   ├── 📁 support
│   │   ├── config.py
│   │   ├── mail.py
│   │   ├── password.py
│   ├── __init__.py
│   ├── __version__.py
│   ├── app.py
│   ├── main.py
```


## Getting Started

### Prerequisites

- Python 3.12+
- Docker (for containerized deployment)
- MongoDB (for data storage)
- RabbitMQ & Celery (for background task processing)



## Building the Docker Image


1. Build the Docker image using the following command:

   ```bash
   sudo docker build --no-cache . -f Dockerfile -t tri-api:latest
   ```

   This command builds a Docker image named tri-api based on the instructions in the Dockerfile.



## Running the Docker Container

To run the tri-api Tool inside a Docker container, use the following command structure:

```bash
sudo docker compose up -d
```

In API container. Execute the below command 
```sh
uvicorn tri_api.main:app --reload --host 0.0.0.0 --port 8080
```


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.