import json
import logging
import os
import time
from abc import abstractmethod, ABC
from typing import Dict, Any

logger = logging.getLogger('base_scraper')


class TicketStatusMonitor(ABC):
    def __init__(self, platform_config, url, match_identifier):
        self.url = url
        self.match_identifier = match_identifier
        self.config = platform_config
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.status_file = 'status_history.json'
        self.load_status_history()

    def load_status_history(self):
        if os.path.exists(self.status_file):
            try:
                with open(self.status_file, 'r') as f:
                    self.status_history = json.load(f)
            except Exception as e:
                logger.error(f'Error loading status history: {e}')
                self.status_history = {}
        else:
            self.status_history = {}

    def save_status_history(self):
        try:
            with open(self.status_file, 'w') as f:
                json.dump(self.status_history, f, indent=4)
        except Exception as e:
            logger.error(f'Error saving status history: {e}')

    def update_status_history(self, current_status, match_details):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        self.status_history[timestamp] = {
            'status': current_status,
            'match_details': match_details
        }
        self.save_status_history()

    @abstractmethod
    def get_match_info(self) -> Dict[str, Any]:
        pass
