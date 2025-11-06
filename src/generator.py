from transformers import pipeline
import warnings
import logging

# Handle transformers warnings
warnings.filterwarnings("ignore")
logging.getLogger("transformers").setLevel(logging.ERROR)


class SummaryGenerator:
    def __init__(self, model="facebook/bart-large-cnn"):
        self.pipe = pipeline("summarization", model=model)

    def generate_summary(self, query, context_passages):
        # Combine passages into single text for BART to summarize
        context = " ".join(context_passages)
        input_text = f"Question: {query}. {context}"

        # Generate summary with fixed parameters to avoid warnings
        result = self.pipe(
            input_text,
            max_length=100,
            min_length=20,
            do_sample=False,
            truncation=True,
            clean_up_tokenization_spaces=True
        )
        summary = result[0]["summary_text"]

        return summary
