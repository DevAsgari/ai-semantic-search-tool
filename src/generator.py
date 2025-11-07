from transformers import pipeline
import warnings
import logging
from typing import List

# Handle transformers warnings
warnings.filterwarnings("ignore")
logging.getLogger("transformers").setLevel(logging.ERROR)


class SummaryGenerator:
    def __init__(self, model: str = "facebook/bart-large-cnn") -> None:
        """
        Initialize the summary generator with a BART model.
        
        Args:
            model: Model name or path for summarization pipeline
        """
        self.pipe = pipeline("summarization", model=model)

    def generate_summary(self, query: str, context_passages: List[str]) -> str:
        """
        Generate a summary from a query and context passages.
        
        Args:
            query: The search query string
            context_passages: List of text passages to summarize
            
        Returns:
            Generated summary string
        """
        # Combine passages into single text for BART to summarize
        context: str = " ".join(context_passages)
        input_text: str = f"Question: {query}. {context}"

        # Generate summary with fixed parameters to avoid warnings
        result = self.pipe(
            input_text,
            max_length=100,
            min_length=20,
            do_sample=False,
            truncation=True,
            clean_up_tokenization_spaces=True
        )
        summary: str = result[0]["summary_text"]

        return summary
