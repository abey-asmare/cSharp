from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.edge.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import keyboard
import pyperclip

# Dynamic or private ports ranging from 49152 to 65536 are available for anyone to use.

BASE_URL = 'https://100seconds.et/'
# BASE_URL = 'C:/Users/sasma/OneDrive/Desktop/tele/index6.html'
GPT_GO = 'https://gptgo.ai/?hl=en'
# header settings
VIEWPORT = (360, 740)
ua = UserAgent().random
options = Options()
options.add_argument(f"user-agent={ua}")
ELEMENT_POSITION = [179, 245, 311, 377]


class Browser:
    def __init__(self):
        # instansiate browser
        self.__driver = webdriver.Edge(options=options)
        self.__driver.set_window_size(VIEWPORT[0], VIEWPORT[1])
        self.__action = ActionChains(self.__driver)
        self.__file_index = 16
        self.__question_type = None
        self.__ordered_list = []
        self.__driver.get(BASE_URL)
        self.open_new_window(GPT_GO)
        self.__window_hundles = self.__driver.window_handles
        self.__driver.switch_to.window(self.__window_hundles[0])
        answer_element = self.__driver.find_elements(By.CSS_SELECTOR, ".answerContainer")

    #  gets page data
    def scrape_page(self):
        page_source = self.__driver.page_source
        with open(f"index{self.__file_index}.html", 'w', encoding='utf-8') as html:
            soup = BeautifulSoup(page_source, 'lxml')
            html.write(soup.prettify())
            print(f"index{self.__file_index}.html")
            self.__file_index += 1

    def listen_events(self):
        # only for scrapping the whole body of the tele
        keyboard.add_hotkey("`", lambda: self.scrape_page())
        keyboard.add_hotkey('right', lambda: self.switch_to_gpt())
        keyboard.add_hotkey('left', lambda: self.switch_back_to_questions())
        keyboard.add_hotkey('r', lambda: self.refresh())

    # def solve_ordered(self, solved_answers: list):
    #     answer_elements = self.__driver.find_elements(By.CSS_SELECTOR, "div.orderedAnswerContainer.answerContainer")
    #     for i in range(0, 4):
    #         for j in range(0, 4):
    #             if answer_elements[i].text.lower() in solved_answers[j].lower():
    #                 self.__action.drag_and_drop(answer_elements[i], answer_elements[j]).perform()
    #     # new_answer = self.__driver.find_elements(By.CSS_SELECTOR, "div.orderedAnswerContainer.answerContainer")
    #     # print("solved answer now is: ", [answer.text + "," for answer in new_answer])
    #     try:
    #         button = self.__driver.find_element(By.CSS_SELECTOR, "div.text-center button.btn-lg")
    #         if button.text == "አስገባ":
    #             self.__action.click(button).perform()
    #             print("button clicked")
    #     except:
    #         print("button unclickable")

    # waits for the user to close the window manually

    def solve_ordered(self, solved_answers: list):
        answer_elements = self.__driver.find_elements(By.CSS_SELECTOR, "div.orderedAnswerContainer.answerContainer")

        for i in range(0, 4):
            for j in range(0, 4):
                if answer_elements[j].text.lower() in solved_answers[i].lower():
                    self.__action.drag_and_drop(answer_elements[j], answer_elements[i]).perform()
                    answer_elements = self.__driver.find_elements(By.CSS_SELECTOR, "div.orderedAnswerContainer.answerContainer")
        try:
            button = self.__driver.find_element(By.CSS_SELECTOR, "div.text-center button.btn-lg")
            if button.text == "አስገባ":
                self.__action.click(button).perform()
                # print("button clicked")
        except:
            print("button unclickable")

    def wait_for_key_press(self):
        while True:
            sleep(1)


    # open new window
    def open_new_window(self, webpage: str):
        self.__driver.switch_to.new_window('tab')
        self.__driver.get(webpage)
        self.__action.send_keys(Keys.ENTER).perform()

    def search_on_it(self, search_query: str):
        element = self.__driver.find_element(By.CSS_SELECTOR, "input.search-input#search-input")
        # clear element before typing
        element.send_keys(Keys.CONTROL + 'a')
        element.send_keys(Keys.BACKSPACE)
        element.send_keys(Keys.CONTROL, 'v')
        element.send_keys(Keys.ENTER)
        self.__driver.find_element(By.CSS_SELECTOR, 'button.btn-ask').click()

    def refresh(self):
        self.__driver.refresh()

    def switch_to_gpt(self):
        question_element = self.__driver.find_element(By.CSS_SELECTOR, ".questionContainer.animated")
        self.__question_type = None
        # try:
        #     answer_element = self.__driver.find_elements(By.CSS_SELECTOR, "span.pl-4")
        #     answers = [answers.text for answers in answer_element]
        #     query = f"based on this question,: {question_element.text} give me only the answer without description. if the question directs you to provide mulitple answers, provide the answers with a newline separator instead of comma between them without any description and angle brackets in it. {answers} "
        #     self.__question_type = "ordered"
        # except NoSuchElementException:
        #     answer_element = self.__driver.find_elements(By.CSS_SELECTOR, "div.answerContainer")
        #     answers = [answers.text for answers in answer_element]
        #     query = f"pick only the answer in the choice list for the question : {question_element.text} {answers}"
        answer_elements = self.__driver.find_elements(By.CSS_SELECTOR, "div.answerContainer")
        answers = [answers.text for answers in answer_elements]
        css_properties = answer_elements[0].get_attribute('class')
        if 'orderedAnswerContainer' in css_properties:
            self.__question_type = "ordered"
            query = f"provide only the answer separated by a newline not a comma without a description for the question : {question_element.text}? {answers[0]}, {answers[1]}, {answers[2]}, {answers[3]}"
        else:
            self.__question_type = "simple"
            query = f"give me only the answer without a description: {question_element.text}? {answers[0]}, {answers[1]}, {answers[2]}, {answers[3]}"

        # self.__driver.implicitly_wait(1)
        pyperclip.copy(query)
        self.__driver.switch_to.window(self.__window_hundles[1])
        self.search_on_it(search_query=query)

    def switch_back_to_questions(self):
        answers = self.__driver.find_element(By.CSS_SELECTOR, "div#home-result").text
        # self.__driver.implicitly_wait(3)
        self.__driver.switch_to.window(self.__window_hundles[0])
        if self.__question_type == "ordered":
            print(f"{self.__question_type}: {answers}")
            self.__ordered_list = answers.split('\n')
            print(self.__ordered_list)
            if (len(self.__ordered_list) <= 3):
                self.__ordered_list = answers.split(',')
            try:
                self.solve_ordered(self.__ordered_list)
            except:
                print("exception happened")
        else:
            print(f"{self.__question_type}: {answers}")
        question_element = self.__driver.find_element(By.CSS_SELECTOR, ".questionContainer.animated")
        print(question_element.text)
