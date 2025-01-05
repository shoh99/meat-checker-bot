import logging
import asyncio
import aiohttp
import requests
import uuid
import json

from googletrans import Translator
from os import getenv
from dotenv import load_dotenv
from requests_toolbelt import MultipartEncoder

load_dotenv()

GROQ_API = getenv('GROQ_API')

NAVER_CLIENT_ID = getenv('NAVER_CLIENT_ID')
NAVER_CLIENT_SECRET = getenv('NAVER_CLIENT_SECRET')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def google_translator(source: str) -> str:
    try:
        translator = Translator()
        result = await translator.translate(source, dest='uz')
        return result.text
    except Exception as e:
        raise


class ImageTranslator:
    """Handlers image translation using Naver Papago API"""

    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.translate_url = "https://naveropenapi.apigw.ntruss.com/image-to-text/v1/translate"

    async def translate_image(self, image_path: str) -> str:
        """Translate image text from Korean to English"""
        try:
            data = {
                'source': 'ko',
                'target': 'en',
                'image': (image_path, open(image_path, 'rb'),
                          'application/octet-stream',
                          {'Content-Transfer-Encoding': 'binary'})
            }

            m = MultipartEncoder(data, boundary=uuid.uuid4())

            headers = {
                "Content-Type": m.content_type,
                "X-NCP-APIGW-API-KEY-ID": str(self.client_id),
                "X-NCP-APIGW-API-KEY": str(self.client_secret)
            }

            res = requests.post(url=self.translate_url, headers=headers, data=m.to_string())
            if res.status_code != 200:
                logger.error(f"Translation API error: {res.text}")
                raise Exception(f"Translation API returned status {res.status_code}")

            response_data = res.json()
            if "data" not in response_data:
                logger.error(f"Unexpected response format: {response_data}")
                raise Exception('Invalid response format from translation API')

            return response_data["data"]["targetText"]

        except Exception as e:
            logger.error(f"Error in translate_image: {str(e)}")
            raise
