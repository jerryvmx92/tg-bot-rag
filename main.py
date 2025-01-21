# Import required libraries
import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()  

# Initialize OpenAI client with API key from environment variables
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# Get Telegram bot token from environment variables
tg_bot_token = os.getenv("TG_BOT_TOKEN")

# Initialize conversation history with system message
# This sets the behavior and personality of the AI assistant
messages = [{
  "role": "system",
  "content": "You are a helpful assistant that answers questions."
}]

# Configure logging to help with debugging
# This will output: timestamp - logger name - log level - message
logging.basicConfig(
  format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
  level=logging.INFO)

# Handler for the /start command
# This is called when a user starts interaction with the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="I'm a bot, please talk to me!")
  
# Handler for the /chat command
# This function processes user messages and gets responses from GPT
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
  # Add user's message to conversation history
  messages.append({"role": "user", "content": update.message.text})
  
  # Send message to OpenAI API and get response
  completion = client.chat.completions.create(model="gpt-4o-mini",
                                              messages=messages)
  completion_answer = completion.choices[0].message
  
  # Add AI's response to conversation history
  messages.append(completion_answer)

  # Send AI's response back to the user
  await context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=completion_answer.content)


if __name__ == '__main__':
  # Initialize the bot application with our token
  application = ApplicationBuilder().token(tg_bot_token).build()

  # Create command handlers for /start and /chat commands
  start_handler = CommandHandler('start', start)
  chat_handler = CommandHandler('chat', chat)

  # Register the handlers with the application
  application.add_handler(start_handler)
  application.add_handler(chat_handler)

  # Start the bot and begin polling for updates
  application.run_polling()