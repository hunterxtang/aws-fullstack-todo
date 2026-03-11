# AWS Full-Stack Todo App
A full-stack todo application deployed on AWS with persistent cloud database storage.

## Architecture
- Backend: Flask + Gunicorn (AWS App Runner)
- Frontend: React (Vite) deployed on Amazon S3
- Container registry: Amazon ECR
- Database: DataStax Astra DB (Managed Cassandra, eu-west-1)
- Cloud infrastructure: AWS
- External API: Open-Meteo Weather API

## Live Deployment
Frontend: 
http://huntertang-todo-frontend-20260303.s3-website.us-east-2.amazonaws.com

Backend Base URL:
https://a8ui9rgiex.us-east-2.awsapprunner.com

Backend Endpoints:
- Health Check: https://a8ui9rgiex.us-east-2.awsapprunner.com/health
- Current Weather: https://a8ui9rgiex.us-east-2.awsapprunner.com/api/weather
- Todos API: https://a8ui9rgiex.us-east-2.awsapprunner.com/api/todos

## Features
- Create todos
- Toggle completion
- Delete todos
- RESTful API design
- Live weather display (current temperature, humidity, wind)
- Persistent data storage via Astra DB (todos survive container restarts and redeployments)
- Production container build
- Cloud deployment using AWS services

## Weather Integration
The backend fetches real-time weather data from the Open-Meteo API and exposes it through the endpoint:

    GET /api/weather

The frontend consumes this endpoint and displays:

    Temperature (°F)
    Humidity (%)
    Wind Speed (mph)

This demonstrates backend-to-external API integration and frontend-to-backend communication in a deployed cloud environment.

## Database Integration
Todos are persisted in a DataStax Astra DB (managed Apache Cassandra) instance. This replaces the previous in-memory store, ensuring data is not lost on container restarts or scaling events.

- Driver: cassandra-driver (Python)
- Authentication: Secure Connect Bundle + token-based credentials
- Credentials managed via AWS App Runner environment variables

## Tech Stack
Frontend:
- React
- Vite
- JavaScript

Backend:
- Flask
- Gunicorn
- Requests
- Flask-CORS
- cassandra-driver

Infrastructure:
- Docker
- AWS ECR
- AWS App Runner
- AWS S3 (Static Hosting)

Database:
- DataStax Astra DB (Serverless Cassandra)

## Local Development
Backend:
```bash
cd backend
python3 app.py
```

Frontend:
```bash
cd frontend
npm run dev
```

## Environment Variables
The following environment variables must be set in App Runner for the backend to function:

| Variable | Description |
|---|---|
| ASTRA_CLIENT_ID | DataStax Astra DB Client ID |
| ASTRA_CLIENT_SECRET | DataStax Astra DB Client Secret |
