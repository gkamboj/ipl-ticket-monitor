import logging
import smtplib
import textwrap
import traceback
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests

logger = logging.getLogger('notifications')


class EmailNotifier:
    def __init__(self, smtp_server, smtp_port, sender_email, sender_password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password

    def send_notification(self, recipient_email, subject, message):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject

            msg.attach(MIMEText(message, 'plain'))

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)

            logger.info(f'Email notification sent to {recipient_email}')
            return True

        except Exception as e:
            logger.error(f'Failed to send email notification: {traceback.format_exc()}')
            return False


class TelegramNotifier:
    def __init__(self, bot_token):
        self.bot_token = bot_token
        self.api_url = f'https://api.telegram.org/bot{bot_token}'

    def send_message(self, chat_id, message):
        try:
            url = f'{self.api_url}/sendMessage'
            data = {
                'chat_id': chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            response = requests.post(url, data=data)
            response.raise_for_status()

            logger.info(f'Telegram message sent')
            return True

        except Exception as e:
            logger.error(f'Failed to send Telegram message: {traceback.format_exc()}')
            return False


class NotificationManager:
    def __init__(self, config):
        self.notifiers = {}
        self.config = config

        if config.get('email', {}).get('enabled', False):
            email_config = config['email']
            self.notifiers['email'] = EmailNotifier(
                email_config['smtp_server'],
                email_config['smtp_port'],
                email_config['sender_email'],
                email_config['sender_password']
            )

        if config.get('telegram', {}).get('enabled', False):
            telegram_config = config['telegram']
            self.notifiers['telegram'] = TelegramNotifier(
                telegram_config['bot_token']
            )

    def send_notifications(self, message, match_details, status, url):
        results = {}

        if not message:
            message = '🚨Tickets status update 🚨'

        formatted_message = self._format_message(message, match_details, status, url)

        logger.info(f"Sending notification to users: {message}")

        if 'email' in self.notifiers:
            email_config = self.config['email']
            recipient = email_config['recipient_email']
            subject = f"ALERT: {match_details.get('teams', '')} - {status}!"
            results['email'] = self.notifiers['email'].send_notification(
                recipient, subject, formatted_message
            )

        if 'telegram' in self.notifiers:
            telegram_config = self.config['telegram']
            chat_id = telegram_config['chat_id']
            results['telegram_message'] = self.notifiers['telegram'].send_message(
                chat_id, formatted_message
            )

        return results

    def _format_message(self, message, match_details, status, url):
        teams = match_details.get('teams', '')
        date = match_details.get('date', '')
        time = match_details.get('time', '')

        formatted_message = textwrap.dedent(f'''
            {message}
            
            Match: {teams}
            Date: {date}
            Time: {time}
            Current Status: {status}
            
            Visit: {url}
        ''')
        return formatted_message



