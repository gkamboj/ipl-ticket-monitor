import json
import logging
import os
from pathlib import Path

log_path = Path(__file__).parent.parent.parent / "ticket_monitor.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(log_path)
    ]
)

logger = logging.getLogger("github_action_updater")


with open('config.json', 'r') as f:
    config = json.load(f)

monitor_url = os.environ.get('MONITOR_URL', '')
district_config = config['platforms']['district']
if config['monitor']['platform'] == 'district' and district_config['enabled'] and os.environ.get('MONITOR_MATCH_IDENTIFIER') and district_config['base_url'] in monitor_url:
    config['monitor']['url'] = os.environ.get('MONITOR_URL')
    config['monitor']['match_identifier'] = os.environ.get('MONITOR_MATCH_IDENTIFIER')
    notify_statuses = [status.strip() for status in os.environ.get('NOTIFY_STATUSES').split(',')]
    district_config['notify_statuses'] = notify_statuses
else:
    logger.error("Invalid platform or missing URL, match identifier. Please check the environment variables.")

if config['telegram']['enabled']:
    if os.environ.get('TELEGRAM_BOT_TOKEN') and os.environ.get('TELEGRAM_CHAT_ID'):
        config['telegram']['bot_token'] = os.environ.get('TELEGRAM_BOT_TOKEN')
        config['telegram']['chat_id'] = os.environ.get('TELEGRAM_CHAT_ID')
    else:
        config['telegram']['enabled'] = False
        logger.warning("Disabling Telegram notifications: required secrets are missing.")

if config['email']['enabled']:
    if os.environ.get('EMAIL_SENDER') and os.environ.get('EMAIL_PASSWORD') and os.environ.get('EMAIL_RECIPIENT'):
        config['email']['sender_email'] = os.environ.get('EMAIL_SENDER')
        config['email']['sender_password'] = os.environ.get('EMAIL_PASSWORD')
        config['email']['recipient_email'] = os.environ.get('EMAIL_RECIPIENT')
    else:
        config['email']['enabled'] = False
        logger.warning('Disabling Email notifications: required secrets are missing.')

with open('config.json', 'w') as f:
    json.dump(config, f, indent=4)

logger.info("Configuration update complete")
