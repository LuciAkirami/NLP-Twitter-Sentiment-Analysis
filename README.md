# Sentiment Analysis API

This project provides a FastAPI-based sentiment analysis service that utilizes a pre-trained Hugging Face model for sentiment prediction.

## Files in This Project

- **`app.py`**: Contains the FastAPI application, including the health check and sentiment prediction endpoints.
- **`model.py`**: Defines `SentimentModel`, which loads and uses the pre-trained model to make sentiment predictions.
- **`requirements.txt`**: Lists all Python dependencies needed to run the application.
- **`Dockerfile`**: Configures the application for deployment using Docker.

## Deployment Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/LuciAkirami/NLP-Twitter-Sentiment-Analysis
cd sentiment-analysis-api
```

### 2. Build the Docker Image

```bash
docker build -t sentiment-analysis-api .
```

### 3. Run the Docker Container Locally

```bash
docker run -d -p 8000:8000 sentiment-analysis-api
```

The application will be accessible at `http://localhost:8000`.

## Deploying the Docker Container to a Cloud Platform

To deploy the Docker container to a cloud platform for production, consider one of the following options:

### Option 1: Deploying to AWS Elastic Container Service (ECS)

1. **Push the Image to Amazon ECR**: Create a repository in Amazon Elastic Container Registry (ECR) and push your Docker image there.
2. **Set Up an ECS Cluster**: Use the ECS console or CLI to create an ECS cluster.
3. **Run a Task on ECS**: Configure a task definition to use the Docker image from ECR and deploy it to your ECS cluster with appropriate settings (like instance type, scaling policies, etc.).
4. **Load Balancer and Security Groups**: Use an Application Load Balancer to manage traffic and configure security groups for access.

### Option 2: Deploying to Google Cloud Run

1. **Push the Image to Artifact Registry (GCR)**: Tag your Docker image and push it to Artifact Registry.
2. **Deploy to Cloud Run**:
   - Use Google Cloud Console to deploy the image from Artifact Registry to Cloud Run.
   - Cloud Run automatically handles scaling, and you can set environment variables and other configurations easily.

### Option 3: Deploying to Azure Container Instances (ACI)

1. **Push the Image to Azure Container Registry (ACR)**: Create a container registry in Azure and push your Docker image.
2. **Deploy to ACI**:
   - Use the Azure portal or Azure CLI to create a new container instance.
   - Configure the instance to pull the Docker image from ACR and set appropriate environment variables and resource configurations.

## Usage

- **Health Check**: `GET /` - Ensures the service is running and the model is loaded.
- **Sentiment Prediction**: `POST /predict` - Accepts JSON input with `"text"` and returns the sentiment.

Example request:

```json
{
  "text": "I love this new feature in Ipad!"
}
```

---

Example output:

```json
{
  "sentiment": [
    {
      "label": "Positive emotion",
      "score": 0.9898064732551575
    }
  ],
  "inference_time": 0.06999492645263672
}
```

## Monitoring the Application in Production

To ensure optimal performance and uptime, here are key areas to monitor, along with recommended tools:

### 1. **Application Health**

   - **Uptime Monitoring**: Use uptime monitoring services like **Pingdom** or **UptimeRobot** to regularly ping your API’s health check endpoint (`GET /`) to ensure the service is operational.
   - **Error Rates**: Monitor error rates on endpoints (`/predict`) to identify issues. FastAPI logs errors, which can be sent to centralized logging services (e.g., **AWS CloudWatch**, **Google Cloud Logging**, **ELK Stack**).

### 2. **Performance Metrics**

   - **Response Time**: Track the response time of each endpoint, especially `/predict`, using **APM tools** (like **New Relic** or **Datadog**). This helps ensure the model responds within acceptable limits.
   - **Memory and CPU Usage**: Since sentiment models can be memory-intensive, use monitoring services (like **Prometheus** with **Grafana** for visualization) to track memory and CPU usage, allowing for adjustments to the instance size if needed.

### 3. **Model Inference Times**

   - **Inference Time Logging**: In `app.py`, inference time is logged. Ensure this data is accessible in a centralized logging platform to monitor average and peak inference times.
   - **Alerting on High Inference Times**: Configure alerts if inference time exceeds acceptable limits, which may indicate performance degradation or an overloaded server.

### 4. **Scaling and Load Handling**

   - **Auto-scaling**: Enable auto-scaling on platforms that support it (e.g., ECS, Cloud Run, or Kubernetes) to handle spikes in traffic.
   - **Load Testing**: Use load-testing tools (e.g., **k6**, **Apache JMeter**) before deployment to determine how the application performs under heavy load and adjust instance count or size accordingly.

### 5. **Security Monitoring**

   - **Endpoint Protection**: Use API gateways or WAFs (Web Application Firewalls) on AWS, Google Cloud, or Azure to monitor for potential threats, rate limit requests, and prevent abuse.
   - **Access Logs**: Enable access logging to keep track of IP addresses and request patterns, alerting on suspicious activity.

By monitoring these aspects, you can ensure that your sentiment analysis API is reliable, responsive, and capable of handling production-level demands effectively.
By following the steps above, you can deploy the sentiment analysis service to a cloud provider of your choice. Each option has its specific steps, but all are well-suited for hosting Dockerized applications.

Note: Created the deployment scripts using ChatGPT. Created a container and tested the endpoints to ensure everything is working perfectly

## TODO

- [ ] Convert the Model to Onnx and Run via TensorRT / OnnxRuntime
- [ ] Quantize the Model and check the Inference and Performance
- [ ] Try multiprocessing from Torch to speed up the Inference
- [ ] Create a Deployment file for Kubernetes 
- [ ] Setup scaling in Kubernetes and loading balancing via NGINIX
- [ ] Send the logs to a monitoring tool