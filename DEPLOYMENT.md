# IPL Ticket Monitor - Deployment Guide

Follow this guide to deploy the application using GitHub Actions.

## Table of Contents
1. [Local Setup and Testing](#local-setup-and-testing)
2. [GitHub Actions Deployment](#github-actions-deployment)
3. [Notification Setup](#notification-setup)
4. [Troubleshooting](#troubleshooting)

## Local Setup and Testing

Before deploying, you should test the application locally to ensure it works correctly:

1. Clone or download the repository to your local machine
2. Install the required dependencies:
   ```
   pip install requests beautifulsoup4
   ```
3. Add the missing values in config.json. Follow [Notification Setup](#notification-setup) for detailed steps. 
4. Test the application:
   ```
   python main.py
   ```

The application should check the ticket status and send notification if current status is in `config.platforms.district.notify_statuses`. You can enter the current status manually in the `config.json` file to test the notification system.

## GitHub Actions Deployment

GitHub Actions is a free service that can run your script on a schedule. This is the recommended deployment method:

1. Fork this GitHub repository
2. Set up GitHub Secrets:
   - Go to your repository → _Settings_ → _Secrets and variables_ → _Actions_ -> _Secrets_ -> _Repository secrets_
   - Add the following secrets:
     - `TELEGRAM_BOT_TOKEN`: Your Telegram bot token
     - `TELEGRAM_CHAT_ID`: Your Telegram chat ID
     - `EMAIL_SENDER`: Your sender email address
     - `EMAIL_PASSWORD`: Your email password or app password
     - `EMAIL_RECIPIENT`: Your recipient email address
3. Set up GitHub Variables:
   - Go to your repository → _Settings_ → _Secrets and variables_ → _Actions_ -> _Variables_ -> _Repository variables_
   - Add the following variables:
     - `CRON_SCHEDULE`: Cron expression for the schedule (e.g. `*/5 * * * *` for every 5 minutes). Workflow file (`.github/workflows/ticket_monitor.yml`) is already configured to run on this schedule.
     - `MONITOR_MATCH_IDENTIFIER`: Match identifier on webpage (e.g. `Delhi Capitals vs Gujarat Titans`)
     - `MONITOR_MATCH_URL`: URL of the match page (e.g. `https://www.district.in/events/delhi-capitals-team`)
     - `DISTRICT_NOTIFY_STATUSES`: Comma-separated list of statuses for which notification is to be sent (e.g. `["Book tickets", "Coming soon"]`)

    
## Notification Setup

### Telegram Notification Setup

1. Create a Telegram Bot
    - Search for `@BotFather` in Telegram
    - Send `/newbot` command
    - Follow the prompts to name your bot
    - Save the API token (format: `123456789:ABCdefGHIjklMnOpQRSTuvwxyz`)


2. Get Your Chat/Channel ID
    #### For Personal Notifications:
      - Search for `@userinfobot` in Telegram
      - Start a chat with it
      - It will reply with your personal `chat_id`

    #### For Channel Notifications (Recommended):
      - Create a new channel (e.g., "IPL Ticket Alerts")
      - Add your bot as administrator:
      - Open channel info
      - Select Administrators → Add Admin
      - Choose your bot from the list 
      - To get the channel ID, forward any message from your channel to `@getidsbot`. It will reply with your `Channel ID` (format: `-1001234567890`)

3. If opting for personal notifications, you must start a chat with your bot manually:
   - Search for your bot's username (@YourBotName)
   - Send any message (e.g., "/start")

4. Update Configuration
```json
"telegram": {
    "enabled": true,
    "bot_token": "YOUR_BOT_TOKEN",
    "chat_id": "YOUR_CHAT_OR_CHANNEL_ID"
}
   ```

### Email Notification Setup

1. If using Gmail, create an App Password:
   - Go to your Google Account → Security
   - Enable 2-Step Verification if not already enabled
   - Go to App passwords, select "Mail" and "Other"
   - Generate and copy the app password

2. Update your `config.json` with your email settings:
   ```json
   "email": {
       "enabled": true,
       "smtp_server": "smtp.gmail.com",
       "smtp_port": 587,
       "sender_email": "your-email@gmail.com",
       "sender_password": "your-app-password",
       "recipient_email": "your-email@gmail.com"
   }
   ```

## Troubleshooting

- **No notifications received**: Check your notification settings in `config.json` and ensure your credentials are correct.
- **"Match not found" error**: The website structure may have changed. Check the website manually and update the scraper code if needed.
- **Rate limiting issues**: Reduce the check frequency in your configuration to avoid being blocked by the website.

For any other issues, check the logs in the deployment platform or the local log file (`ticket_monitor.log`).
