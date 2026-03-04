# AWS Full-Stack Todo App

A full-stack todo application deployed on AWS.

## Architecture

- Backend: Flask + Gunicorn (AWS App Runner)
- Frontend: React (Vite) deployed on Amazon S3
- Container registry: Amazon ECR
- Cloud infrastructure: AWS
- External API: Open-Meteo Weather API

## Live Deployment

Frontend: 

http://huntertang-todo-frontend-20260303.s3-website.us-east-2.amazonaws.com

Backend Base URL:

https://a8ui9rgiex.us-east-2.awsapprunner.com

Backend Endpoints:

Health Check: https://a8ui9rgiex.us-east-2.awsapprunner.com/health

Current Weather: https://a8ui9rgiex.us-east-2.awsapprunner.com/api/weather

Todos API: https://a8ui9rgiex.us-east-2.awsapprunner.com/api/todos

## Features

- Create todos
- Toggle completion
- Delete todos
- RESTful API design
- Live weather display (current temperature, humidity, wind)
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

Infrastructure:
- Docker
- AWS ECR
- AWS App Runner
- AWS S3 (Static Hosting)

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
