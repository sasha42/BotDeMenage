# Bot de Ménage
> Telegram bot that reminds everyone to clean the apartment.

![Screenshot of bot de menage](screenshot.png "Bot de menage")

**🐏 Fetches cleaning tasks from a Google Sheet**

**💬 Sends tasks to Telegram group once a week**

**📌 Pins the message in the chat**

## Setup

1. **Create a Telegram Bot:**
   - Use [BotFather](https://core.telegram.org/bots#6-botfather) to create a new Telegram bot. You will receive a bot token upon creation.

2. **Create a Telegram Group Chat:**
   - Create a Telegram group chat and add your bot to the group.
   - Obtain the chat ID by sending a message to the group chat and then calling the Telegram API method `getUpdates`. Look for the 'id' field in the response, which is a negative number.
     ```sh
     curl "https://api.telegram.org/bot<botId>/getUpdates"
     ```

3. **Set Up Your Python Environment:**
   - Create a virtual environment and install necessary packages. Clone the repository and run the following commands:
     ```sh
     python3 -m venv venv
     source venv/bin/activate
     pip install requests python-dotenv
     ```

4. **Add .env file with Google Sheet URL, Bot Token and Chat ID:**
   - Create a `.env` file in the project directory with the following content, remember to add your own values:
     ```sh
     export GOOGLE_SHEET_URL=''
     export TELEGRAM_BOT_TOKEN=''
     export TELEGRAM_CHAT_ID=''
     ```

4. **Create a `menage.service` File:**
   - Create a `menage.service` file in `/etc/systemd/system/menage.service` with the following content:
     ```ini
     [Unit]
     Description=Sends Telegram message with cleaning tasks once a week

     [Service]
     Type=oneshot
     User=sasha
     Group=sasha
     WorkingDirectory=/home/sasha/BotMenage/
     Environment="PATH=/home/sasha/BotMenage/venv/bin"
     ExecStart=/home/sasha/BotMenage/venv/bin/python /home/sasha/BotMenage/bot.py

     [Install]
     WantedBy=multi-user.target
     ```

5. **Create a `menage.timer` File:**
   - Create a `menage.timer` file in `/etc/systemd/system/menage.timer` with the following content:
     ```ini
     [Unit]
     Description=Weekly Task Timer

     [Timer]
     OnCalendar=Mon 09:00
     Persistent=true

     [Install]
     WantedBy=timers.target
     ```

6. **Reload systemd and Enable the Timer:**
   - Reload the systemd manager configuration to recognize the new unit files, and then enable and start the timer.
     ```sh
     sudo systemctl daemon-reload
     sudo systemctl enable menage.timer
     sudo systemctl start menage.timer
     ```

9. **Ensure locale exists:**
    - If you encounter an error related to the locale, you can generate the locale by running the following command:
      ```sh
      sudo apt-get update
      sudo apt-get install locales
      sudo locale-gen fr_FR fr_FR.UTF-8
      sudo dpkg-reconfigure locales
      ```

8. **Run the Script Manually (Optional):**
   - You can manually run the script to test if everything is set up correctly.
     ```sh
     source /home/sasha/BotMenage/venv/bin/activate
     python /home/sasha/BotMenage/bot.py
     ```


Happy cleaning!

---
Built by Sasha in 2023-2024