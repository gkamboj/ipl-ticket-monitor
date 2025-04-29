import logging
from typing import Dict, Any

from src.scrapers.base_scraper import TicketStatusMonitor
from src.scrapers.district_scrapper import DistrictStatusMonitor

logger = logging.getLogger('scraper_factory')


class ScraperFactory:

    @staticmethod
    def create_scraper(config: Dict[str, Any]) -> 'TicketStatusMonitor':
        monitor_config = config.get('monitor')
        platform = monitor_config.get('platform', '')
        url = monitor_config.get('url', '')
        match_identifier = monitor_config.get('match_identifier')

        logger.info(f'Attempting to create scraper for URL: {url}')

        platforms_config = config.get('platforms', {})
        if platform not in platforms_config:
            error_msg = f"Platform '{platform}' not found in configuration"
            logger.error(error_msg)
            raise ValueError(error_msg)

        platform_config = platforms_config[platform]
        if not platform_config.get('enabled', False):
            error_msg = f"Platform '{platform}' is disabled in configuration"
            logger.error(error_msg)
            raise ValueError(error_msg)

        if not url or not match_identifier:
            error_msg = f'URL or match identifier not found in configuration'
            logger.error(error_msg)
            raise ValueError(error_msg)

        logger.info(f"Platform '{platform}' configuration validated successfully")

        if platform == 'district':
            return DistrictStatusMonitor(platform_config, url, match_identifier)
        else:
            error_msg = f'Unsupported platform: {platform}'
            logger.error(error_msg)
            raise ValueError(error_msg)
