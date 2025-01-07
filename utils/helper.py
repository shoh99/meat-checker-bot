import re
import logging

from aiogram.types import Message
from datetime import datetime
from utils.config import Config
from utils.db import DbConfig


def extract_and_clean_product_type(response_text):
    # Regular expression to find 'Product type:'
    match = re.search(r"<b>Product type:</b>\s*(.+)", response_text)
    if match:
        raw_product_type = match.group(1).strip()  # Extract the product type
        # Remove HTML tags
        clean_product_type = re.sub(r"<[^>]+>", "", raw_product_type)
        return clean_product_type.strip()
    return None


def insert_data(response: str, message: Message):
    config = Config()
    db_config = DbConfig(config.DB_NAME, config.CONNECTION_STRING)
    tg_user = message.chat
    try:
        inserted_date = {
            "tg_user_id": tg_user.id,
            "tg_user_fullname": tg_user.full_name,
            "created_date": datetime.now(),
            "product_type": extract_and_clean_product_type(response)
        }
        collection_name = "meat_check"
        db_config.insert_data(collection_name, inserted_date)
    except Exception as e:
        logging.error(f"Error occurred {str(e)}")
    finally:
        db_config.close_connection()