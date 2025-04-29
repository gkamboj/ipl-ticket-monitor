import logging
import re
import traceback
from typing import Dict, Any

import requests
from bs4 import BeautifulSoup

from src.scrapers.base_scraper import TicketStatusMonitor

logger = logging.getLogger('district_scraper')

class DistrictStatusMonitor(TicketStatusMonitor):

    def _find_section_container(self, soup, heading_text):
        try:
            # District team landing page has h1 tags with headings like 'Tickets on sale' and 'Upcoming'
            # Find the h1 tag with the exact heading_text
            heading_tag = soup.find(lambda tag: tag.name == 'h1' and tag.get_text(strip=True) == heading_text)

            if not heading_tag:
                logger.debug(f"Heading '{heading_text}' not found.")
                return None

            # Navigate up the structure: h1 -> parent -> grandparent
            # Based on the webpage HTML provided, below is the expected structure:
            # <div> <-- Grandparent (Target Container)
            #   <div> <-- Parent
            #     <h1>Tickets on sale</h1> <-- Starting point
            #     ...
            #   </div>
            # </div>
            parent_element = heading_tag.parent
            if not parent_element:
                logger.debug(f"Heading '{heading_text}' has no parent element.")
                return None

            grandparent_element = parent_element.parent
            if not grandparent_element:
                logger.debug(f"Parent of heading '{heading_text}' has no parent (grandparent).")
                return None

            return grandparent_element

        except Exception as e:
            logger.error(f"Error finding section container for '{heading_text}' via structure: {traceback.format_exc()}")
            return None

    def _find_match_details_in_container(self, container_tag, match_name_query, status_markers):
        if not container_tag:
            logger.debug('find_match_details_in_container received None container.')
            return False, None, None

        container_text = container_tag.get_text(' ', strip=True)

        if match_name_query.lower() not in container_text.lower():
            logger.debug(f"Match name '{match_name_query}' not found in container text.")
            return False, None, None
        else:
            all_container_matches = self._split_with_delimiters(container_text, status_markers)
            relevant_match = next((part for part in all_container_matches if match_name_query.lower() in part.lower()),
                                  '')

        pattern = re.compile(
            r'(?P<day>\w+)\s+'
            r'(?P<date>\d{1,2})\s+'
            r'(?P<month>\w+)\s+'
            r'.*?'
            r'(?P<time>\d{1,2}:\d{2}\s+[AP]M)\s+'
            r'onwards\s+'
            r'(?:.*?\s+)?'
            r'(?P<status>' + '|'.join(re.escape(m) for m in status_markers) + ')'
        )

        match = pattern.search(relevant_match)
        if not match:
            logger.debug('Found match but failed to extract details.')
            return False, None, None

        match_details = {
            'teams': match_name_query,
            'date': f'''{match.group('day')}, {match.group('date')} {match.group('month')}''',
            'time': match.group('time')
        }
        return True, match_details, match.group('status')

    def _split_with_delimiters(self, s, delimiters):
        delimiter = next((delim for delim in delimiters if delim.lower() in s.lower()), '')
        return [val + delimiter for val in s.split(delimiter) if val]

    def get_match_info(self) -> Dict[str, Any]:
        result = {
            'notify': False,
            'url': self.url,
            'status': 'Match status unknown / Not Found'
        }

        logger.info(f'Getting match info for match: {self.match_identifier}')

        if ' vs ' not in self.match_identifier:
            result['status'] = "Invalid match format (expected 'Team A vs Team B')"
            return result

        try:
            response = requests.get(self.url, headers=self.headers, timeout=20)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            allowed_statuses = self.config.get('possible_statuses', [])

            # Check 'Tickets on sale' section first
            on_sale_container = self._find_section_container(soup, 'Tickets on sale')
            if on_sale_container:
                found, match_details, status = self._find_match_details_in_container(on_sale_container,
                                                                                     self.match_identifier,
                                                                                     allowed_statuses)
                if found:
                    result['notify'] = status in self.config.get('notify_statuses', [])
                    result['status'] = status
                    result['match_details'] = match_details
                    result['message'] = '🚨 URGENT: Tickets are now available for booking! 🚨'
                    self.update_status_history(result['status'], result.get('match_details', {}))
                    return result

            # Check 'Upcoming' section if not found in tickets on sale
            upcoming_container = self._find_section_container(soup, 'Upcoming')
            if upcoming_container:
                found, match_details, status = self._find_match_details_in_container(upcoming_container,
                                                                                     self.match_identifier,
                                                                                     allowed_statuses)
                if found:
                    result['notify'] = status in self.config.get('notify_statuses', [])
                    result['status'] = status
                    result['match_details'] = match_details
                    self.update_status_history(result['status'], result.get('match_details', {}))
                    return result

            if not on_sale_container and not upcoming_container:
                result['message'] = 'Error: Could not locate event sections'

        except requests.exceptions.RequestException as e:
            logger.error(f"RequestException fetching page: {traceback.format_exc()}")
            result['message'] = f'Error: Could not fetch page ({str(e)})'
        except Exception as e:
            logger.error(f"Exception fetching page: {traceback.format_exc()}")
            result['message'] = f'Error: Processing failed ({str(e)})'

        self.update_status_history(result['status'], result.get('match_details', {}))
        return result
