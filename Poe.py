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
from poe_api_wrapper import PoeApi


TOKEN = '4Ti_eGta1vh34hC5FcJbtg%3D%3D'
client = PoeApi(TOKEN)


BASE_URL = 'https://100seconds.et/'
# BASE_URL = 'C:/Users/sasma/OneDrive/Desktop/tele/index6.html'
# header settings
VIEWPORT = (360, 740)
ua = UserAgent().random
options = Options()
options.add_argument(f"user-agent={ua}")
ELEMENT_POSITION = [179, 245, 311, 377]


class Poe:
    def __init__(self):
        # instansiate browser
        self.__driver = webdriver.Edge(options=options)
        self.__driver.set_window_size(VIEWPORT[0], VIEWPORT[1])
        self.__action = ActionChains(self.__driver)
        self.__file_index = 16
        self.__question_type = None
        self.__ordered_list = []
        self.__driver.get(BASE_URL)
        answer_element = self.__driver.find_elements(By.CSS_SELECTOR, ".answerContainer")


    def listen_events(self):
        # only for scrapping the whole body of the tele
        # keyboard.add_hotkey("`", lambda: self.scrape_page())
        # keyboard.add_hotkey('r', lambda: self.refresh())
        keyboard.add_hotkey('right', lambda: self.solveWithPoe())

    def solve_ordered(self, solved_answers: list):
        answer_elements = self.__driver.find_elements(By.CSS_SELECTOR, "div.orderedAnswerContainer.answerContainer")

        for i in range(0, 4):
            for j in range(0, 4):
                if answer_elements[j].text.lower() in solved_answers[i].lower():
                    try:
                        self.__action.drag_and_drop(answer_elements[j], answer_elements[i]).perform()
                        answer_elements = self.__driver.find_elements(By.CSS_SELECTOR, "div.orderedAnswerContainer.answerContainer")
                    except IndexError as e:
                        print(e)
        try:
            button = self.__driver.find_element(By.CSS_SELECTOR, "div.text-center button.btn-lg")
            if button.text == "አስገባ":
                self.__action.click(button).perform()
                # print("button clicked")
        except:
            print("button unclickable")

    # waits for the user to close the window manually
    def wait_for_key_press(self):
        while True:
            sleep(1)

    def solveWithPoe(self):
        question_element = self.__driver.find_element(By.CSS_SELECTOR, ".questionContainer.animated")
        self.__question_type = None
        answer_elements = self.__driver.find_elements(By.CSS_SELECTOR, "div.answerContainer")
        answers = [answers.text for answers in answer_elements]
        css_properties = answer_elements[0].get_attribute('class')
        if 'orderedAnswerContainer' in css_properties:
            self.__question_type = "ordered"
            query = f"provide only the answer separated by a newline not a comma without a description for the question : {question_element.text}? {answers[0]}, {answers[1]}, {answers[2]}, {answers[3]}"
            pyperclip.copy(query)
            request = client.send_message('BotYULFL821PQ', query)
            solved_answers = request['response'].split('\n')
            if len(solved_answers)< 3:
                solved_answers = request['response'].split(',')
            print(request['response'])
            self.solve_ordered(solved_answers)
        else:
            self.__question_type = "simple"
            query = f"give me only the answer without a description: {question_element.text}? {answers[0]}, {answers[1]}, {answers[2]}, {answers[3]}"
            pyperclip.copy(query)
            request = client.send_message('BotYULFL821PQ', query)
            for answer_element in answer_elements:
                if answer_element.text.lower() in request['response'].lower():
                    print(answer_element.text)
                    self.__action.click(answer_element).perform()