# Meat Checker Bot

Meat Checker Bot is a Telegram bot designed to help users verify whether a product contains non-halal ingredients. The bot works in both Uzbek and English and is tailored for analyzing Korean-written product descriptions.

## Features
- Accepts photos of product descriptions from users.
- Extracts text from images.
- Translates Korean text to English using the Naver Papago API.
- Analyzes the translated product description using Llama 3 AI to detect non-halal ingredients.
- Translates the results into Uzbek using the Google Translate package.
- Supports two languages: Uzbek and English.

## Bot Name
**Meat Checker Bot**

## Prerequisites
To run this bot, you need the following:
- Python 3.9+
- Telegram account to interact with the bot
- Telegram API credentials
- Naver Papago API credentials
- GROQ credentials for Llama 3
- Required Python packages (listed below)

## Technology Stack
- **Telegram Framework**: aiogram 3.x
- **Image Text Translation**: Naver Papago API
- **Image Description Analysis**: Llama 3
- **Uzbek Translation**: Google Translate package

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/meat-checker-bot.git
    cd meat-checker-bot
    ```

2. Set up a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up your environment variables:
    - Create a `.env` file in the project root and add the following keys:
      ```env
      TELEGRAM_TOKEN=<your-telegram-bot-token>
      NAVER_CLIENT_ID=<your-naver-client-id>
      NAVER_CLIENT_SECRET=<your-naver-client-secret>
      GROQ_API=<your-groq-api-key>
      ```

## Usage

1. Start the bot on Telegram by searching for **Meat Checker Bot** and clicking "Start."
2. Send a photo of a product description written in Korean.
3. The bot will:
   - Extract the text from the image.
   - Translate the text from Korean to English using Naver Papago.
   - Analyze the translated text with Llama 3 to detect non-halal ingredients.
   - Translate the results into Uzbek (if requested).
4. The bot will return the analysis results in the selected language (Uzbek or English).

## Example Commands
- **/start**: Start the bot and get a welcome message.
- **/help**: View instructions on how to use the bot.
- **/language [uz/en]**: Change the bot’s response language to Uzbek or English.


## Notes
- Ensure your API keys are valid and have sufficient quotas for usage.
- The bot’s accuracy depends on the quality of the image and the text’s readability.
- For better results, ensure the product description is in clear Korean text.


## Contributing
Contributions are welcome! Please open an issue or submit a pull request to propose changes or report bugs.

## Acknowledgments
- **Telegram** for providing the bot platform.
- **Naver Papago API** for Korean-to-English translation.
- **Groq Llama 3** for text analysis.
- **Google Translate** for English-to-Uzbek translation.

---

Enjoy using Meat Checker Bot to ensure your products meet halal standards!

