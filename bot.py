import os
import requests
from datetime import datetime, timedelta
import locale
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_data_from_google_sheet(sheet_url, sheet_range):
    # Get data from the public Google Sheet using the URL
    response = requests.get(f"{sheet_url}/gviz/tq?tqx=out:csv&sheet={sheet_range}")

    if response.ok:
        data = response.text
        rows = data.split("\n")
        return [row.split(",") for row in rows if row.strip()]
    else:
        print("Failed to fetch data from Google Sheet.")
        return None

def pin_telegram_message(bot_token, chat_id, message_id):
    url = f'https://api.telegram.org/bot{bot_token}/pinChatMessage'
    payload = {'chat_id': chat_id, 'message_id': message_id}

    response = requests.post(url, data=payload)

    if response.ok:
        print('Telegram message pinned successfully.')
    else:
        print('Failed to pin Telegram message.')

def send_telegram_message(bot_token, chat_id, message):
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {'chat_id': chat_id, 'text': message}

    response = requests.post(url, data=payload)

    if response.ok:
        print('Telegram message sent successfully.')
        return response.json()  # Return the response content as JSON
    else:
        print('Failed to send Telegram message.')
        return None

def main():
    # Set the locale to French
    locale.setlocale(locale.LC_TIME, 'fr_FR')

    # Replace with your actual values or load from environment variables
    google_sheet_url = os.getenv('GOOGLE_SHEET_URL')
    google_sheet_range = 'schedule'

    telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')

    if not all([google_sheet_url, telegram_bot_token, telegram_chat_id]):
        print("Please set the GOOGLE_SHEET_URL, TELEGRAM_BOT_TOKEN, and TELEGRAM_CHAT_ID environment variables.")
        return

    # Get data from the public Google Sheet
    data = get_data_from_google_sheet(google_sheet_url, google_sheet_range)
    
    if data:
        # Get data from the first row
        names = data[0]
        
        # Find the row with the current date
        current_date = datetime.now()
        date_in_7_days = current_date + timedelta(days=7)
        date_range_str = f"Tâches du {current_date.strftime('%d %B')} au {date_in_7_days.strftime('%d %B')}"
        
        for row in data:
            if row[0].strip('"') == current_date.strftime('%d/%m/%Y'):
                message_lines = [date_range_str]
                for name, value in zip(names[1:], row[1:]):
                    print(name, value)
                    message_lines.append("{}: {}".format(name.strip('"'), value.strip('"')))
                message = "\n".join(message_lines)
                # Send the message to Telegram
                message_response = send_telegram_message(telegram_bot_token, telegram_chat_id, message)
                if message_response:
                    message_id = message_response['result']['message_id']
                    # Pin the message
                    pin_telegram_message(telegram_bot_token, telegram_chat_id, message_id)
                break
        else:
            # This else block is executed when the loop completes without encountering a break
            message_lines = [f"No data found for {date_range_str}"]
            message = "\n".join(message_lines)
            send_telegram_message(telegram_bot_token, telegram_chat_id, message)
    else:
        print("No data available from the Google Sheet.")

if __name__ == "__main__":
    main()
