import os
import sys
from datetime import datetime
from textwrap import dedent

from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.exceptions import UnexpectedModelBehavior
from pydantic_ai.models.openai import OpenAIModel

from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtGui import QDesktopServices, QIcon
from PyQt6.QtWidgets import (QApplication, QWidget, QTextEdit, QPushButton,
                             QLineEdit, QStatusBar, QHBoxLayout, QVBoxLayout, QSystemTrayIcon, QMenu)

class SearchQuery(BaseModel):
    search_query: str = Field(..., description='The search query to be executed.')

def setup_agent() -> Agent:
    agent_google_search = Agent(
        name='Google Search Query Agent',
        model=OpenAIModel('gpt-4o-mini'),
        system_prompt=dedent("""
            You are a Google Search Query Agent. Your task is to take user's input, come up with a crafted Google search query using American English,

            You will be provided with operator table to help you refine the search.

            Steps to follow:
            1. Check for typo or spelling errors in the user's input and correct it.
            2. Check for grammar errors in the user's input and correct it.
            3. Check for punctuation errors in the user's input and correct it.
            4. Check for capitalization errors in the user's input and correct it.
            5. Identify the main topic of the search.
            6. Use the operator table to understand how to refine the search.
            7. Construct a Google search query using the identified topic and operators unless user provide the full URL.

            For for example, if the user input is "search post about laidoff un reddit", you should:
            1. Correct the spelling of "laidoff" to "laid off".
            2. Identify the main topic as "laid off".
            3. Use the operator table to refine the search.
            4. Construct a Google search query using the identified topic and operators.

            If the user input is a website URL, you should:
            1. Check if the URL is valid.
            2. If valid, return the URL as is.
            3. If not valid, correct the URL and return it.

            For example, if the user input is "https://www.example.com", you should navigate to that URL.

            Here's a list of examples giving for the query output giving the user input:
            1. "Find verified customer reviews for the latest smartphones without fake ratings" -> "("iPhone 15 Pro review" OR "Samsung Galaxy S24 review") ("verified purchase" OR "real customer review") -"sponsored post" -"paid review" site:bestbuy.com OR site:amazon.com OR site:trustpilot.com OR site:reddit.com"
            2. "Find hidden travel deals on flights and hotels that aren’t widely advertised" -> "("cheap flights" OR "hotel discounts" OR "hidden travel deals") ("error fare" OR "mistake fare" OR "last-minute deal") site:skyscanner.com OR site:theflightdeal.com OR site:secretflying.com OR site:google.com/travel"
            3. "Find high-quality free online courses on tech skills from top universities" -> "("free online course" OR "MOOC") ("data science" OR "AI" OR "Python") site:edx.org OR site:coursera.org OR site:khanacademy.org OR site:harvard.edu OR site:mit.edu -intext:"paid"
            4. "Find websites related to Tesla that aren't Tesla's official site" -> "related:tesla.com -site:tesla.com"
            5. "Find pages with reviews of the iPhone 15 Pro in the title and URL" -> "allintitle:"iPhone 15 Pro review" allinurl:review"
            6. "Find archived (cached) versions of OpenAI's blog" -> "cache:openai.com/blog"
            7. "Find Apple patent-related articles where "Steve Jobs" is mentioned with an unknown word in between" -> "intitle:patent intext:"Steve * Jobs" site:uspto.gov OR site:patents.google.com"
            
        """),
        result_type=SearchQuery
    )

    @agent_google_search.system_prompt
    def add_today_timestamp() -> str:
        return f'Today is {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}.'

    @agent_google_search.system_prompt
    def add_google_operator_table() -> str:
        operator = """
        | Search Operator    | What it does                                           | Example                  |
        |--------------------|-------------------------------------------------------|--------------------------|
        | " "                | Search for results that mention a word or phrase.     | "steve jobs"             |
        | OR                 | Search for results related to X or Y.                 | jobs OR gates            |
        | |                  | Same as OR:                                           | jobs | gates             |
        | AND                | Search for results related to X and Y.                | jobs AND gates           |
        | -                  | Search for results that don’t mention a word or phrase.| jobs -apple             |
        | *                  | Wildcard matching any word or phrase.                 | steve * apple            |
        | ( )                | Group multiple searches.                              | (ipad OR iphone) apple   |
        | define:            | Search for the definition of a word or phrase.        | define:entrepreneur      |
        | cache:             | Find the most recent cache of a webpage.              | cache:apple.com          |
        | filetype:          | Search for particular types of files (e.g., PDF).     | apple filetype:pdf       |
        | ext:               | Same as filetype:                                     | apple ext:pdf            |
        | site:              | Search for results from a particular website.         | site:apple.com           |
        | related:           | Search for sites related to a given domain.           | related:apple.com        |
        | intitle:           | Search for pages with a particular word in the title tag. | intitle:apple        |
        | allintitle:        | Search for pages with multiple words in the title tag.| allintitle:apple iphone  |
        | inurl:             | Search for pages with a particular word in the URL.   | inurl:apple              |
        | allinurl:          | Search for pages with multiple words in the URL.      | allinurl:apple iphone    |
        | intext:            | Search for pages with a particular word in their content. | intext:apple iphone  |
        | allintext:         | Search for pages with multiple words in their content.| allintext:apple iphone   |
        | weather:           | Search for the weather in a location.                 | weather:san francisco    |
        | stocks:            | Search for stock information for a ticker.            | stocks:aapl              |
        | map:               | Force Google to show map results.                     | map:silicon valley       |
        | movie:             | Search for information about a movie.                 | movie:steve jobs         |
        | in                 | Convert one unit to another.                          | $329 in GBP              |
        | source:            | Search for results from a particular source in Google News. | apple source:the_verge |
        | before:            | Search for results from before a particular date.     | apple before:2007-06-29  |
        | after:             | Search for results from after a particular date.      | apple after:2007-06-29   |
        """
        return operator

    return agent_google_search

def resource_path(relative_path: str) -> str:
    """Function to get the absolute path to the resource file to patch PyInstaller 
    unable to locate the bundled resources when packaging.
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath('.')

    return os.path.join(base_path, relative_path)

class AppWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('AI Google Search Generator')
        self.setWindowIcon(QIcon(resource_path('./browser.ico')))
        self.setStyleSheet('font-family: Arial; font-size: 16px; background-color: #122b3a;')
        self.resize(800, 600)

        self.layout = {}
        self.layout['main'] = QVBoxLayout()
        self.setLayout(self.layout['main'])

        self.init_ui()
        self.init_tray_icon()

        self.message_history = []
        self.agent = setup_agent()

    def init_ui(self):
        self.log_window = QTextEdit()
        self.log_window.setReadOnly(True)
        self.log_window.setStyleSheet('background-color: #f0f0f0; color: #000000;')
        self.layout['main'].addWidget(self.log_window)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText('Enter your search query here...')
        self.input_field.setStyleSheet('background-color: #ffffff; color: #000000;')
        self.input_field.setMinimumHeight(35)
        self.input_field.returnPressed.connect(self.run_search)
        self.layout['main'].addWidget(self.input_field)

        self.layout['button_layout'] = QHBoxLayout()
        self.layout['main'].addLayout(self.layout['button_layout'])

        self.search_button = QPushButton('Search')
        self.search_button.setStyleSheet('background-color: #122b3a; color: #ffffff;')
        self.search_button.setFixedWidth(120)
        self.search_button.clicked.connect(self.run_search)
        self.layout['button_layout'].addWidget(self.search_button)

        self.reset_button = QPushButton('&Reset')
        self.reset_button.setStyleSheet('background-color: #FF5733; color: #ffffff;')
        self.reset_button.clicked.connect(self.reset_search)
        self.layout['button_layout'].addWidget(self.reset_button)

        self.layout['button_layout'].addStretch()

        self.status_bar = QStatusBar()
        self.status_bar.setStyleSheet('background-color: #122b3a; color: #ffffff;')
        self.layout['main'].addWidget(self.status_bar)

    def init_tray_icon(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(resource_path('./browser.ico')))

        tray_menu = QMenu()
        restore_action = tray_menu.addAction('Restore')
        restore_action.triggered.connect(self.show_normal)
        quit_action = tray_menu.addAction('Quit')
        quit_action.triggered.connect(QApplication.instance().quit)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.on_tray_icon_activated)
        self.tray_icon.show()

    def show_normal(self):
        self.show()
        self.setWindowState(self.windowState() & ~Qt.WindowState.WindowMinimized | Qt.WindowState.WindowActive)
        self.activateWindow()

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.show_normal()

    def closeEvent(self, event):
        if self.isVisible():
            event.ignore()
            self.hide()

    def reset_search(self):
        self.input_field.clear()
        self.log_window.clear()
        self.status_bar.clearMessage()
        self.message_history = []

    def run_search(self):
        user_input = self.input_field.text()

        try:
            res = self.agent.run_sync(user_input, message_history=self.message_history)

            if isinstance(res.data, SearchQuery):
                search_query = res.data.search_query
                self.log_window.append(f'Search query: {search_query}')
                self.status_bar.showMessage(f'Opening browser with query: {search_query}...')
                QDesktopServices.openUrl(QUrl(f'https://www.google.com/search?q={search_query}'))
                self.message_history = res.all_messages()

        except UnexpectedModelBehavior as e:
            self.status_bar.showMessage(f'Error: {e}')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    app_window = AppWindow()
    app_window.show()

    sys.exit(app.exec())