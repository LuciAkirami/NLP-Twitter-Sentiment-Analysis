# Sentiment Analysis API

This project provides a FastAPI-based sentiment analysis service that utilizes a Fine-Tuned Hugging Face model for sentiment prediction.

Link to the Fine-Tuned Model: https://huggingface.co/Akirami/twitter-roberta-sentiment-analysiss-lr-1e-5

**Updated (Nov 11)**

Link to the ONNX Quantized Model: [Akirami/twitter-roberta-sentiment-analysiss-onnx-quantized](https://huggingface.co/Akirami/twitter-roberta-sentiment-analysiss-onnx-quantized)

(See below to know the performance compared to the vanilla model)

## Files in this Project

- **`NLP-Assignment.ipynb`**: This notebook contains the code for analyzing the tweet data and fine-tuning a Roberta Model on top of it.
- **`Optimum_ONNX_Runtime_Experimentation.ipynb`**: This notebook contains experimentation of converting the fine-tuned model into onnx format.
- **`df_cleaned.csv`**: Contains the pre-processed version of train data located in `nlp_data.xlsx`
- **`deployment`**: Contains the files for deployment.
- **`nlp_data.xlsx`**: Data used for training and testing the model.
- **`test_predictions.csv/.xlsx`**: Contains the predictions for the test data that is present in `nlp_data.xlsx`
- **`request_data.json`**: Contains an example JSON to test the endpoint.

  ## Files in Deployment Folder
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


## Update - Nov 11 -> ONNX Experimentation

This table emphasizes the benefits of ONNX optimization, especially with quantization, which provides both the largest speedup and the smallest size. 

- Everything was tested on CPU in Free Tier Google Colab.
- The model has been converted to ONNX and quantized via the HuggingFace Optimum Library
- The model inference was done through the same Optimum Library
- For evaluation, the 1000 rows of the cleaned tweet data is taken

| Model Variant         | Accuracy | Total Time (s) | Improvement from Original (%) | Samples per Second | Latency (s) | Size (MB) |
|-----------------------|----------|----------------|-------------------------------|---------------------|-------------|-----------|
| **Original Model**    | 0.599    | 147.82        | 0.00%                         | 6.77               | 0.148       | 499       |
| **ONNX**              | 0.599    | 118.68        | 19.71%                        | 8.43               | 0.119       | 477       |
| **ONNX Optimized**    | 0.599    | 103.06        | 30.28%                        | 9.70               | 0.103       | 477       |
| **ONNX Quantized**    | **0.614**| **77.18**     | **47.78%**                    | **12.96**          | **0.077**   | **121**   |

### Observations:
- **Size Reduction**: The ONNX Quantizer model is significantly smaller, at 121 MB, compared to the original (499 MB) and other ONNX variants (477 MB). 
- **Performance Gains**: The ONNX Quantizer model achieves nearly half the original model’s total time and a substantial reduction in size, enhancing both storage efficiency and processing speed. The Quantized Model should not be achieving greater accuracy, but it might be due to some randomness in the weights and the dataset quality
- **ONNX Optimizations**: Both ONNX and ONNX Optimizer reduce the model size slightly (to 477 MB) while also delivering marked improvements in time and latency.

The quantized onnx model has been deployed to the HuggingFace Hub and can be called via the following code
Note: The latest optimum package is giving out errors, use the following version `optimum[exporters,onnxruntime]==1.19.0`
```python
from optimum.pipelines import pipeline

task_type = "text-classification"
onx_cls = pipeline(task_type, model="Akirami/twitter-roberta-sentiment-analysiss-onnx-quantized")
```

## TODO

- [x] Convert the Model to Onnx and Run via OnnxRuntime / Optimum
- [ ] Replace the existing model with ONNX within the deployments folder
- [ ] Test the ONNX Model latency with TensorRT in a Nvidia Optimized Container
- [ ] Quantize the Model and check the Inference and Performance
- [ ] Try multiprocessing from Torch to speed up the Inference
- [ ] Create a Deployment file for Kubernetes 
- [ ] Setup scaling in Kubernetes and loading balancing via NGINX
- [ ] Send the logs to a monitoring tool
