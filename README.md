# BLT Contact BOT

BLT Contact BOT is a Python script that sets up a Telegram bot allowing users to create and post content to a specific channel with inline buttons for actions like messaging and visiting a website.

## Requirements

- Python 3.x
- `python-telegram-bot` library
- `dotenv` library

Install the required packages using the following:

```bash
pip install -r requirements.txt
```

## Usage

1. Clone or download this repository.

2. Create a `.env` file in the root directory with the following content:

   ```plaintext
   BOT_TOKEN=your_bot_token_here
   CHANNEL_ID=your_channel_id_here
   ```

   Replace `your_bot_token_here` with your actual bot token obtained from the BotFather on Telegram, and replace `your_channel_id_here` with the ID of the channel where you want to post content.

3. Run the script:

   ```bash
   python src/bot.py
   ```

4. Start a conversation with your bot on Telegram and send the `/start` command to begin creating and posting content.

## How It Works

- Users can start a conversation with the bot using the `/start` command.

- The bot guides users through the process of creating a post by asking for content, a message address, and a website URL.

- Once the content is ready, the bot displays the post along with inline buttons for messaging and visiting the website.

- Users can approve or decline the post using inline keyboard buttons.
