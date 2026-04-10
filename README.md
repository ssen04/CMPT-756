# Cloud Deployment Impact on Microservices Performance

SFU CMPT 756 final project

This project studies how deployment choice affects the performance of a microservices-based web application on Google Cloud Platform. We built an e-commerce system, deployed it across VM, container, and serverless environments, and compared the resulting latency, cold start behavior, and scalability under load.

## System Overview

The application is organized as five microservices:

- Register service
- Catalog service
- Cart service
- Order service
- Notification service

Core requests are handled synchronously through HTTP APIs, while order confirmation is handled asynchronously through Pub/Sub between the Order and Notification services. The services share a centralized MySQL database so that deployment strategy, rather than storage topology, remains the main experimental variable.

## Deployment Variants

We evaluated the same application logic on three GCP deployment targets:

- VM deployment using Python services managed directly on Compute Engine
- Container deployment using Docker-based services on Cloud Run
- Serverless deployment using Cloud Functions implementations

VM and container deployments use FastAPI with `uvicorn`. Serverless deployments were rewritten as pure Python functions to avoid initialization issues in the Cloud Functions runtime.

## Evaluation

We used k6 to run low-load and high-load experiments across the services and compared:

- Average latency
- Tail latency (p95/p99 where available)
- Cold start behavior
- Error rate under load

The final experiments showed that VM provided the most stable latency overall, Cloud Run performed well for read-heavy workloads, and serverless deployment reduced high-load latency for the Order service in spite of cold starts. Across all three environments, the main scalability bottleneck was shared-database row locking in write-heavy requests.

## Repository Structure

- register-service: Register microservice and container deployment files
- catalog-service: Catalog service for VM, container, and serverless variants
- cart-service: Cart service implementation and Dockerfile
- order-service: Order service, business logic, and Pub/Sub publisher
- notification-service: Notification service and Pub/Sub subscriber
- k6: Load-testing scripts and recorded experiment outputs

## Team Members

- Jiayi Li
- Liliana Lopez Beristain
- Joohyun Park
- Hongrui Qu
- Sukanya Sen
