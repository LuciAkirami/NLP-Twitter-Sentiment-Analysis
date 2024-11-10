from transformers import pipeline
import logging

# Set up logging for this module
logger = logging.getLogger(__name__)

class SentimentModel:
    def __init__(self, model_name: str):
        """Initialize the model and pipeline."""
        self.model_name = model_name
        self.pipe = None
        self.load_model()

    def load_model(self):
        """Load the model into the pipeline."""
        try:
            logger.info(f"Loading model: {self.model_name}")
            self.pipe = pipeline("text-classification", model=self.model_name)
            logger.info("Model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            self.pipe = None  # Set pipe to None to indicate failure

    def predict(self, text: str):
        """Predict sentiment from the given text."""
        if self.pipe is None:
            raise ValueError("Model is not loaded or available.")
        
        try:
            result = self.pipe(text)
            return result
        except Exception as e:
            logger.error(f"Error during inference: {e}")
            raise ValueError(f"Inference failed: {e}")

# Initialize the model object globally so it can be accessed in the app
sentiment_model = SentimentModel("Akirami/twitter-roberta-sentiment-analysiss-lr-1e-5")
