import logging
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Google Sheets setup
def setup_google_sheets():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('myanmar-flood-assistance.json', scope)
    client = gspread.authorize(creds)
    return client.open("Flood Assistance Contacts").sheet1  # Replace with your Google Sheet name

sheet = setup_google_sheets()

# Function to search for associations based on the township
async def find_associations(update: Update, context: CallbackContext) -> None:
    user_input = update.message.text.strip()
    
    try:
        # Get all data from the Google Sheet
        data = sheet.get_all_records()
        
        # Filter the data based on the user's input (Township)
        results = [row for row in data if row['Township'].strip().lower() == user_input.lower()]
        
        # If no results are found
        if not results:
            await update.message.reply_text(f"No associations found for {user_input}. Please try again with a valid township.")
            return
        
        # Create a message with the results
        reply = f"Associations in {user_input}:\n\n"
        for result in results:
            reply += f"Association: {result['Association Name']}\nContact: {result['Contact Number']}\n\n"
        
        # Send the result back to the user
        await update.message.reply_text(reply)

    except Exception as e:
        await update.message.reply_text('An error occurred while fetching the data. Please try again.')
        logger.error(f"Error: {e}")

# Main function to start the bot
def main():
    # Start the Telegram bot
    TOKEN = '7524023688:AAEVYAPeDJuLN-2QkIDBHaKEtAQlR1lVKHQ'  # Replace this with your bot token
    application = Application.builder().token(TOKEN).build()

    # Add handlers
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, find_associations))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()


