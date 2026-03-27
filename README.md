# Cloud Deployment Choices & Microservices Performance (CMPT 756 Project)

This project explores how different cloud deployment strategies impact the performance of a microservices-based web application. We build a simple e-commerce system and evaluate latency across multiple deployment environments.

---

## Overview

The application is designed using a **microservices architecture**, where each core function is implemented as an independent service:

- Browse Catalog  
- Register Customer  
- Add to Cart  
- Place Order  
- Notifications / Confirmation  

Each microservice is developed using **Python + FastAPI** and connected to a shared **MySQL database**.

---

## Objective

The goal of this project is to analyze how deployment choices affect system performance:

- Virtual Machines (Compute Engine)  
- Containers (Cloud Run)  
- Serverless Functions (Cloud Functions)  

We compare these approaches primarily using **latency**.


## System Architecture
