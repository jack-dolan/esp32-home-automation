# IoT Home Automation System

A containerized microservices application for home temperature monitoring and device control using ESP32 microcontrollers, AWS cloud infrastructure, and a responsive web interface.

## Project Overview

This project allows for remote monitoring and control of home temperature and devices (blinds, thermostats) through a web interface. The system uses ESP32 microcontrollers to collect temperature data and control physical devices, with a containerized backend deployed on AWS.

### Key Features

- Remote temperature monitoring from multiple sensors
- Automated and manual control of thermostats
- Automated and manual control of window blinds
- Historical temperature data visualization (24-hour period)
- Mobile-friendly web interface
- Secure user authentication

### Learning Goals

This project aims to provide hands-on experience with:

- Docker containers and containerization
- AWS cloud services (ECR, ECS, IoT Core)
- CI/CD pipelines with GitHub Actions
- Microservices architecture
- Serverless computing (AWS Lambda)
- Message queues and event-driven architecture
- Security scanning and testing automation

## Architecture

### Hardware Components

- ESP32 microcontrollers (2-3 for temperature sensors)
- ESP32 microcontrollers with servo motors (3 for thermostat control)
- ESP32 microcontrollers with stepper motors (3 for blind control)
- Temperature sensors (DHT22 or BME280)

### Software Components

#### Containerized Microservices (AWS ECS/Fargate)

1. **API Service**: RESTful API for the web application
2. **Device Management Service**: Handles device registration and control
3. **Analytics Service**: Processes and serves temperature history data

#### Serverless Components

1. **AWS Lambda Functions**: Event-driven processing of sensor data
2. **AWS IoT Core**: MQTT broker for device communication

#### Frontend

- Responsive web application (React/TypeScript)
- Hosted on AWS S3 as a static website

### AWS Infrastructure

![Architecture Diagram]
*(Architecture diagram to be added)*

- **Amazon ECR**: Stores Docker container images
- **Amazon ECS with Fargate**: Runs containerized services
- **AWS IoT Core**: Connects ESP32 devices via MQTT
- **AWS Lambda**: Processes sensor data and triggers actions
- **Amazon DynamoDB**: Stores device state and temperature data
- **Amazon S3**: Hosts the static web application
- **Amazon API Gateway**: Provides HTTP endpoints for the web app
- **Amazon CloudWatch**: Monitors application and costs

## Development Environment

### Prerequisites

- AWS Account
- Docker Desktop
- Node.js and npm
- Python 3.8+
- Arduino IDE (for ESP32 development)
- Git

### Local Development Setup

1. Clone this repository
```bash
git clone https://github.com/yourusername/home-automation.git
cd home-automation
```

2. Install dependencies
```bash
# Backend dependencies
cd services/api
pip install -r requirements.txt

# Frontend dependencies
cd ../../frontend
npm install
```

3. Run services locally with Docker Compose
```bash
docker-compose up
```

4. Access the web interface at `http://localhost:3000`

## CI/CD Pipeline

The project uses GitHub Actions for continuous integration and deployment:

1. **Build Stage**:
   - Run unit tests
   - Build Docker images
   - Scan for vulnerabilities (Snyk, SonarQube)
   - Check code coverage (minimum 80%)

2. **Deploy Stage**:
   - Push Docker images to Amazon ECR
   - Update ECS services
   - Deploy frontend to S3

## Project Structure

```
├── .github/
│   └── workflows/         # GitHub Actions workflow definitions
├── frontend/              # React/TypeScript web application
├── services/              # Containerized microservices
│   ├── api/               # API Service
│   ├── device-mgmt/       # Device Management Service
│   └── analytics/         # Analytics Service
├── lambda/                # AWS Lambda functions
├── infrastructure/        # Infrastructure as Code (CloudFormation)
├── esp32/                 # ESP32 firmware for different devices
│   ├── temperature/       # Temperature sensor firmware
│   ├── thermostat/        # Thermostat control firmware
│   └── blinds/            # Blind control firmware
├── docker-compose.yml     # Local development orchestration
└── README.md              # This file
```

## Contributing

This is a personal project, so external contributions are not expected. Development will follow a simple GitHub Flow:

1. Create a feature branch from `main`
2. Develop and test the feature
3. Create a pull request to merge back to `main`
4. Merge after tests pass

## License

MIT

## Acknowledgments

- AWS Free Tier for cloud resources
- ESP32 community for libraries and examples
