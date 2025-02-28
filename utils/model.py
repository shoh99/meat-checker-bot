import groq
import logging


from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class GroqAnalyzer:
    """Handles interaction with Groq API for text analysis."""

    def __init__(self, api_key: str):
        self.client = groq.Client(api_key=api_key)

    async def analyze_text(self, content: str) -> str:
        """Analyze text for pork-related content."""
        """Analyze text for non-Halal ingredients with a focused prompt."""
        prompt = f"""Analyze this food product description for Halal compliance. Check for:
        1. Pork or derivatives (including lard, gelatin, enzymes)
        2. Alcohol-based ingredients
        3. Other types of meats

        Product text: {content}

        Reply format:
        - Use HTML tags for formatting (e.g., <b> for bold instead of **).
        - Product type: [with one or two word, wrapped in <b> tags]
        - Issues: [List main concerns if any, use <b> tags for key points]
        - Advice: [Brief recommendation, use <b> tags for emphasis]

        Example:
        <b>Product type:</b> Granola
        <b>Issues:</b>
        1. <b>Pork:</b> The product contains pork, which is a major concern for Halal compliance.

        <b>Advice:</b> This product is not suitable for Halal consumption due to the presence of pork. Avoid this product or look for Halal-certified granola products.
        """

        try:
            chat = [{"role": "system", "content": prompt}]
            chat_completion = self.client.chat.completions.create(
                messages=chat,
                model="llama3-70b-8192",
                temperature=0.1  # Lower temperature for more consistent responses
            )
            return chat_completion.choices[0].message.content

        except groq.APIConnectionError as e:
            logger.error(f"Groq API connection error: {str(e)}")
            raise
        except groq.RateLimitError as e:
            logger.error(f"Groq API rate limit exceeded: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in analyze_text: {str(e)}")
            raise

