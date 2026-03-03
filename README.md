# AWS Full-Stack Todo App

A full-stack todo application deployed on AWS.

## Architecture

- Backend: Flask + Gunicorn (AWS App Runner)
- Frontend: React (Vite) deployed on Amazon S3
- Container registry: Amazon ECR
- Cloud infrastructure: AWS

## Live Deployment

Frontend: http://huntertang-todo-frontend-20260303.s3-website.us-east-2.amazonaws.com/
Backend API: https://a8ui9rgiex.us-east-2.awsapprunner.com

## Features

- Create todos
- Toggle completion
- Delete todos
- RESTful API
- Production build + cloud deployment

## Tech Stack

Frontend:
- React
- Vite

Backend:
- Flask
- Gunicorn

Infrastructure:
- Docker
- AWS ECR
- AWS App Runner
- AWS S3

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
