import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from models import *
from bridgetex import build_analysis_template


class TCResultsDriver(webdriver.Chrome):
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
        return f"#000000RB0000000000{board_number:02d}000001000001000000000000000000"

    def prepare(self):
        self.get(self.url_base)
        self.board_numbers = self.execute_script("return settings.BoardsNumbers")

    def set_active_board(self, board_number):
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
        try:
            raw_cards = self.find_element(By.ID, span_name).text
            raw_cards = raw_cards.split("\n")
            return Hand(*raw_cards)
        except TimeoutException:
            print(f"Error loading element: {span_name}")

    def load_board(self, board_number: int = 0):
        if board_number != 0:
            self.set_active_board(board_number)

        hands = []
        for span_name in ("tabB_wCards0", "tabB_nCards0", "tabB_eCards0", "tabB_sCards0"):
            hands.append(self.get_cards(span_name))

        board = BoardData(self.active_board_number, *hands)
        self.board_data[self.active_board_number] = board
        print(f"Loaded board #{self.active_board_number}:")
        print(str(board))

    def board_numbers(self):
        for n in self.board_numbers:
            yield n


if __name__ == '__main__':
    driver = TCResultsDriver("https://mzbs.pl/files/2021/wyniki/zs/240925/")

    for n in (1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 24, 25, 26, 27):
        driver.load_board(n)

    build_analysis_template(driver.board_data.values(), "test_python.tex", verbose=True)

