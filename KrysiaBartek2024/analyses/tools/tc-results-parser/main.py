"""
This module is used to scrape the bridge hands from the TC Results website
and generate a LaTeX file with the hand diagrams.
"""

import argparse
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from models import Hand, BoardData
from bridgetex import build_analysis_template

class TCResultsDriver(webdriver.Chrome):
    """
    This class is used to scrape the data from the TC Results website.
    """
    def __init__(self, url_base):
        options = Options()
        options.add_argument("--headless=new")
        super().__init__(options=options)
        self.url_base = url_base
        self.active_board_number: int | None = None
        self.board_numbers = []
        self.board_data = {}

        self.prepare()

    @staticmethod
    def get_url_tail(board_number: int) -> str:
        """
        This method returns the URL tail for the given board number.
        """
        return f"#000000RB0000000000{board_number:02d}000001000001000000000000000000"

    def prepare(self):
        """
        This method prepares the driver by loading the main page and
        extracting the board numbers.
        """
        self.get(self.url_base)
        self.board_numbers = self.execute_script("return settings.BoardsNumbers")

    def set_active_board(self, board_number):
        """
        This method sets the active board number.
        """
        url = self.url_base + TCResultsDriver.get_url_tail(board_number)
        print(f"GET: {url}")
        self.get(url)
        # hehe
        time.sleep(0.5)
        # TODO improve waiting maybe sth like that
        # try:
        #     WebDriverWait(driver, 30).until(
        #         lambda d: d.execute_script("return document.readyState") == "complete"
        #     )
        # except TimeoutException as err:
        #     raise TimeoutError("Page not loaded") from err
        self.active_board_number = board_number

    def get_cards(self, span_name) -> Hand:
        """
        This method extracts the cards from the given span element.
        """
        try:
            element = self.find_element(By.ID, span_name)
            html_content = element.get_attribute("innerHTML")

            spades, hearts, diamonds, clubs = "", "", "", ""

            if 'spades.gif' in html_content:
                spades, spades_length = self.extract_cards(html_content, 'spades.gif', -1)
            if 'hearts.gif' in html_content:
                hearts, hearts_length = self.extract_cards(html_content, 'hearts.gif', -1)
            if 'diamonds.gif' in html_content:
                diamonds, diamonds_length = self.extract_cards(html_content, 'diamonds.gif', -1)
            if 'clubs.gif' in html_content:
                clubs, _clubs_length = self.extract_cards(html_content, 'clubs.gif', \
                    13 - (spades_length + hearts_length + diamonds_length))

            return Hand(spades, hearts, diamonds, clubs)

        except TimeoutException:
            print(f"Error loading element: {span_name}")
            return Hand("", "", "", "")

    def extract_cards(self, html_content, suit_img, suit_length):
        """
        This method extracts the card string that follows the suit image (gif).
        """
        suit_index = html_content.index(suit_img)

        card_start = html_content.find('>', suit_index) + 1
        card_end = (html_content.find('<', card_start) if suit_length == \
                    -1 else card_start + suit_length + 1)
        result = html_content[card_start:card_end].strip()

        result = result.replace('10', 'T')
        result = result.replace('1', 'T')
        return result, len(result)

    def load_board(self, board_number: int = 0):
        """
        This method loads the board data for the given board number.
        """
        if board_number != 0:
            self.set_active_board(board_number)

        hands = []
        for span_name in ("tabB_nCards0", "tabB_eCards0", "tabB_sCards0", "tabB_wCards0"):
            hands.append(self.get_cards(span_name))

        # pylint: disable=E1120
        board = BoardData(self.active_board_number, *hands)
        self.board_data[self.active_board_number] = board
        print(f"Loaded board #{self.active_board_number}:")
        print(str(board))

    # pylint: disable=E0202
    def board_numbers(self):
        """
        This method returns an iterator for the board numbers.
        """
        for m in self.board_numbers:
            yield m


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scrape bridge hands from TC Results')
    parser.add_argument('-n', '--number', type=int, help='Number of boards to process')
    parser.add_argument('-d', '--url', type=str,
                        default="https://mzbs.pl/files/2021/wyniki/zs/240925/",
                        help='Base URL of the results page')
    parser.add_argument('-b', '--board', type=int, help='Specific board number to process')

    args = parser.parse_args()

    driver = TCResultsDriver(args.url)

    if args.board is not None and args.number is not None:
        print("Error: Please provide either -n or -b, not both.")
        exit()

    if args.board is not None:
        # If a specific board is provided, load only that one
        if args.board in driver.board_numbers:
            driver.load_board(args.board)
        else:
            print(f"Error: Board {args.board} not found.")
    else:
        # If -n is provided, process only the first n boards
        num_boards = min(args.number, len(driver.board_numbers)) \
            if args.number else len(driver.board_numbers)
        for n in driver.board_numbers[:num_boards]:
            driver.load_board(n)

    # Generate the LaTeX file
    build_analysis_template(driver.board_data.values(), "test_python.tex", verbose=True)