# Telegram AI Chat Bot

A Telegram bot powered by OpenAI's GPT-4o-mini that can engage in conversations and answer questions.

## Features

- `/start` command to initiate conversation with the bot
- `/chat` command to ask questions and get AI-powered responses
- Conversation history tracking for context-aware responses
- Secure API key management through environment variables

## Prerequisites

- Python 3.12 or higher
- UV for running the project
- A Telegram account
- OpenAI API key
- Telegram Bot Token (from BotFather)

## Setup Guide

1. **Clone the Repository**
   ```bash
   git clone <your-repository-url>
   cd telegram-bot
   ```

2. **Set Up Environment Variables**
   
   Create a `.env` file in the project root and add your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key
   TG_BOT_TOKEN=your_telegram_bot_token
   ```

3. **Install Dependencies**
   ```bash
   uv sync
   ```

4. **Run the Bot**
   ```bash
   uv run main.py
   ```

## How to Use

1. **Start the Bot**
   - Open Telegram and search for your bot using its username
   - Send the `/start` command to begin interaction

2. **Chat with the Bot**
   - Use the `/chat` command followed by your question
   - Example: `/chat What is the capital of France?`
   - The bot will process your question and respond with an AI-generated answer

## Project Structure

- `main.py`: Core bot logic and command handlers
- `.env`: Environment variables (API keys)
- `.gitignore`: Specifies which files Git should ignore
- `README.md`: Project documentation (you're reading it!)

## Technical Details

The bot is built using:
- `python-telegram-bot`: For Telegram Bot API integration
- `openai`: For GPT-3.5 API access
- `python-dotenv`: For environment variable management

The code implements:
- Asynchronous command handling
- Message history tracking
- Error logging
- Secure API key management

## Limitations

- The bot needs to be restarted for each new conversation to reset context
- Responses are not streamed word-by-word (Telegram limitation)
- No visual feedback during response generation

## Future Improvements

- Implement conversation context management
- Add user-specific conversation history
- Enhance error handling and user feedback
- Add more commands and features

## Contributing

Feel free to fork this project and submit pull requests with improvements!

## License

This project is open source and available under the MIT License.
