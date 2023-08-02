# Bot de menage
> Telegram bot that reminds everyone to clean the appartment.

The bot runs on AWS Lambda and reminds everyone to clean the appartment every week. It plugs into a Telegram group chat and sends a message to the group chat every week.

## Setup
1. Create a Telegram bot using [BotFather](https://core.telegram.org/bots#6-botfather). You will need the bot token.
2. Create a Telegram group chat and add the bot to the group. You will need the chat ID, which you can get by sending a message to the group chat and then calling the Telegram API method `getUpdates`. You will need the 'id' which is a negative number.
    ```
    curl "https://api.telegram.org/bot<botId>/getUpdates"
    ```
    
3. Create a new AWS Lambda function.
4. Add an EventBridge trigger to the Lambda function. Set the schedule with a cron expression to run every week.
5. Add the neccesary environment variables to the Lambda function:
    - `TELEGRAM_BOT_TOKEN`: The token of the Telegram bot.
    - `TELEGRAM_CHAT_ID`: The chat ID of the Telegram group chat.
6. Add the code to the Lambda function.
7. Add the `requests` layer to the Lambda function.

## How to create a Lambda layer
Sometimes, AWS Lambda does not have the neccesary packages installed. In this case, you can create a Lambda layer and add it to the Lambda function. This is how you create a Lambda layer using the Cloud9 IDE:
```
mkdir folder
cd folder
virtualenv venv
source venv/bin/activate
pip install supabase
pip install requests
deactivate
mkdir python
cd python/
cp -r ../venv/lib64/python3.7/site-packages/* .
cd ..
zip -r supabase_requests_layer.zip python
aws lambda publish-layer-version --layer-name supabase_requests --zip-file fileb://supabase_requests_layer.zip --compatible-runtimes python3.9
```

---
Built by Sasha in 2023