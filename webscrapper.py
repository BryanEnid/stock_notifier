from selenium import webdriver
import os

class Webscrapper:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('headless')
        self.driver = webdriver.Chrome(executable_path='./chromedriver.exe', chrome_options=self.options)
        self.driver.get('https://robinhood.com/crypto/btc')

    def parseHTML(self,html):
        return html.text


    def clear(self):
        return os.system('cls')


    def quit(self):
        self.driver.quit()


    def getPrice(self):
        numbers = []

        while len(numbers) < 9:
            numbers = list(map(self.parseHTML, self.driver.find_elements_by_css_selector(".QzVHcLdwl2CEuEMpTUFaj span")))
            numbers = list(filter(None, numbers))

        if "," in numbers:
            numbers.remove(",")

        numbers.pop(0)
        
        result = ''.join(numbers)
        return float(result)
    


