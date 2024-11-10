import logging
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from model import sentiment_model  # Import the SentimentModel instance
from starlette.responses import JSONResponse
import time

# Initialize FastAPI app
app = FastAPI()

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic model for input validation
class TextInput(BaseModel):
    text: str

# Health check endpoint
@app.get("/")
async def health_check():
    """Health check endpoint to ensure the server is running."""
    if sentiment_model.pipe is None:
        raise HTTPException(status_code=503, detail="Model is not loaded properly")
    return {"status": "healthy", "message": "The service is up and running"}

# Inference endpoint to predict sentiment
@app.post("/predict")
async def predict_sentiment(input: TextInput):
    """Endpoint to predict sentiment from provided text."""
    if sentiment_model.pipe is None:
        raise HTTPException(status_code=503, detail="Model is not available")

    try:
        start_time = time.time()
        result = sentiment_model.predict(input.text)
        inference_time = time.time() - start_time

        logger.info(f"Prediction: {result} | Inference time: {inference_time:.4f} seconds")
        return {"sentiment": result, "inference_time": inference_time}
    
    except ValueError as e:
        logger.error(f"Error during inference: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Custom error handler for unhandled exceptions
@app.exception_handler(Exception)
async def validation_exception_handler(request: Request, exc: Exception):
    """Custom handler for unhandled exceptions."""
    logger.error(f"Unhandled error: {exc} | Request: {request.url}")
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error. Please try again later."},
    )
