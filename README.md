## Introduction

This is the merchant side of electronic wallet system for IOT Midterm Exam Project, implemented using hybrid Next.js + Python app that uses Next.js as the frontend and FastAPI as the API backend. 

## How It Works

The Python/FastAPI server is mapped into to Next.js app under `/api/`.

This is implemented using [`next.config.js` rewrites](https://github.com/digitros/nextjs-fastapi/blob/main/next.config.js) to map any request to `/api/:path*` to the FastAPI API, which is hosted in the `/api` folder.

On localhost, the rewrite will be made to the `127.0.0.1:8000` port, which is where the FastAPI server is running.

In production, the FastAPI server is hosted as [Python serverless functions](https://card-payment-iot.vercel.app/) on Vercel.

## Demo

https://card-payment-iot.vercel.app/
