import asyncio
import logging

from pathlib import Path
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from datetime import datetime
from dotenv import load_dotenv
from utils.config import Config
from utils.model import GeminiAnalyzer
from utils import helper

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# state management for user language selection
class UserState(StatesGroup):
    selecting_language = State()
    ready_for_image = State()


TRANSLATION = {
    'en': {
        'name':'ENGLISH',
        'welcome': "Welcome to Food Checker Bot! Please select your language:",
        'language_selected': "Language set to English. You can now send food product images for Halal checking.",
        'processing': "Processing your image... Please wait.",
        'translating': "Translating text from image...",
        'analyzing': "Analyzing ingredients...",
        'error': "Sorry, an error occurred. Please make sure the image is clear and try again.",
        'send_image': "Please send a food product's description image for checking.",
        "disclaimer": "We do not claim or certify any product as ✅ Halal or ❌ Non-Halal. "
                      "🤖 Our bot only checks for the presence of prohibited ingredients or components 🔍 based on "
                      "the provided product information."
                      "📌 The final decision regarding the suitability of the product rests solely with the user."
                      "🛑 Please consult reliable sources or authorities if confirmation is needed."
    },
    'uz': {
        'name':'UZBEK',
        'welcome': "Ovqat mahsulotlarini Tekshirish botiga xush kelibsiz! Iltimos, tilni tanlang:",
        'language_selected': "Til o'zbek tiliga o'rnatildi. Endi mahsulotni tekshirish uchun oziq-ovqat mahsulotlarining rasmlarini yuborishingiz mumkin.",
        'processing': "Rasm qayta ishlanmoqda... Iltimos, kuting.",
        'translating': "Rasmdagi matn tarjima qilinmoqda...",
        'analyzing': "Tarkibiy qismlar tahlil qilinmoqda...",
        'error': "Kechirasiz, xatolik yuz berdi. Iltimos, rasm aniq ekanligiga ishonch hosil qiling va qaytadan urinib ko'ring.",
        'send_image': "Iltimos, maxsulotni tekshirish uchun oziq-ovqat mahsulotining tarkibini rasmini yuboring.",
        "disclaimer": "Biz hech qanday mahsulotni ✅ halol yoki ❌ nohalol deb da'vo qilmaymiz yoki sertifikatlamaymiz."
                      " 🤖 Bizning bot faqat taqdim etilgan mahsulot ma'lumotlariga asoslanib, "
                      "taqiqlangan ingredientlar yoki tarkibiy qismlarni 🔍 aniqlash uchun tekshiradi. "
                      "📌 Mahsulotning mosligi haqidagi yakuniy qaror foydalanuvchining o‘ziga bog‘liq."
                      "🛑 Iltimos, zarur bo‘lsa, ishonchli manbalar yoki mutasaddi tashkilotlarga murojaat qiling."
    }
}


def get_keyboard():
    """Create persistent keyboard with language selectio """
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="English 🇬🇧"),
                KeyboardButton(text="O'zbek 🇺🇿")
            ]
        ],
        resize_keyboard=True,
    )


class PorkCheckerBot:
    """Main bot class handling Telegram interactions."""

    def __init__(self, config: Config):
        self.config = config,
        self.bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        self.dp = Dispatcher()
        self.analyzer = GeminiAnalyzer(config.GEMINI_API)
        self._register_handlers()

    def _create_media_dir(self):
        media_dir = Path("media")
        media_dir.mkdir(exist_ok=True)
        return media_dir

    def _register_handlers(self):
        """Register message handlers"""
        self.dp.message.register(self.cnd_start, Command("start"))
        self.dp.message.register(self.handle_language_selection,
                                 lambda msg: msg.text in ["English 🇬🇧", "O'zbek 🇺🇿"])
        self.dp.message.register(self.handle_photo, lambda msg: msg.photo, UserState.ready_for_image)

    async def cnd_start(self, message: Message, state: FSMContext):
        """Handle /start command."""
        await state.set_data({'language': 'en'})  # Default to English
        await message.reply(
            TRANSLATION['en']['welcome'],
            reply_markup=get_keyboard()
        )

    async def handle_language_selection(self, message: Message, state: FSMContext):
        """Handle language selection."""
        language = 'en' if message.text == "English 🇬🇧" else 'uz'
        await state.update_data(language=language)
        await state.set_state(UserState.ready_for_image)

        await message.reply(
            TRANSLATION[language]['language_selected'],
            reply_markup=get_keyboard()
        )

    async def handle_photo(self, message: Message, state: FSMContext):
        """Handle incoming photos."""
        user_data = await state.get_data()
        language = user_data.get("language", "en")

        status_message = await message.reply(TRANSLATION[language]['processing'])
        temp_file = None

        try:
            # Download photo
            photo = message.photo[-1]
            file = await self.bot.get_file(photo.file_id)
            self._create_media_dir()
            img_path = f"media/temp_{datetime.now().timestamp()}.jpg"
            temp_file = Path(img_path)

            await self.bot.download_file(file.file_path, img_path)
            response_language = TRANSLATION[language]["name"]

            await status_message.edit_text(TRANSLATION[language]['analyzing'])
            analysis = await self.analyzer.analyze_image(img_path, response_language)

            helper.insert_data(analysis, message)

            # Send final response
            if language == "uz":
                response = (
                    f"🔍 <b>Tahlil natijasi:</b>\n\n"
                    f"✨ <b>Tahlil:</b>\n{analysis}\n\n"
                    f"⚠️ <b>Ogohlantirish:</b>\n{TRANSLATION[language]['disclaimer']}"
                )
            else:
                response = (
                    f"🔍 <b>Analysis Result:</b>\n\n"
                    f"✨ <b>Analysis:</b>\n{analysis}\n\n"
                    f"⚠️ <b>Disclaimer:</b>\n{TRANSLATION[language]['disclaimer']}"
                )
            await message.reply(response)

        except Exception as e:
            error_msg = "Sorry, an error occurred while processing your image. Please try again."
            logger.error(f"Error processing photo: {str(e)}")
            await message.reply(TRANSLATION[language]['error'])

        finally:
            # Cleanup temporary file
            if temp_file and temp_file.exists():
                temp_file.unlink()

    async def start(self):
        """Start the bot"""
        try:
            logger.info("Starting bot...")
            await self.dp.start_polling(self.bot)
        except Exception as e:
            logger.error(f"Error starting bot: {str(e)}")
            raise


async def main():
    """Main function to run the bot"""
    try:
        config = Config()
        bot = PorkCheckerBot(config)
        await bot.start()
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
