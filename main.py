import argparse
import json
import logging
import traceback
from datetime import datetime

from src.notifiers import NotificationManager
from src.scrapers.scraper_factory import ScraperFactory

logger = logging.getLogger('main')


def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('ticket_monitor.log')
        ]
    )


def load_config(config_path):
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config
    except Exception as e:
        logger.error(f'Error loading configuration: {e}')
        return None


def run_monitor(config_path):
    config = load_config(config_path)
    if not config:
        logger.error('Failed to load configuration. Exiting.')
        return False

    monitor = ScraperFactory.create_scraper(config)
    notification_manager = NotificationManager(config)

    try:
        logger.info(f"Checking ticket status at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}...")
        info = monitor.get_match_info()
        if info.get('notify'):
            notification_results = notification_manager.send_notifications(
                info.get('message'), info.get('match_details'), info.get('status'), info.get('url')
            )
            logger.info(f'Notification results: {notification_results}')
        else:
            logger.info(f"Skipping sending notification as notifications disabled for the current status {info.get('status')}")
    except KeyboardInterrupt:
        logger.info('Monitoring stopped by user.')
    except Exception as e:
        logger.error(f'Error in monitoring loop: {traceback.format_exc()}')
        return False

    return True


def main():
    configure_logging()
    parser = argparse.ArgumentParser(description='IPL Ticket Monitor')
    parser.add_argument('--config', default='config.json', help='Path to configuration file')
    args = parser.parse_args()

    logger.info('------------ STARTING IPL TICKET MONITOR ------------')
    success = run_monitor(args.config)

    if success:
        logger.info('------------ MONITORING COMPLETED SUCCESSFULLY ------------')
    else:
        logger.error('------------ MONITORING FAILED ------------')


if __name__ == "__main__":
    main()
