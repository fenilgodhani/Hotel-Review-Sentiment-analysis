from selenium import webdriver
import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import selenium.webdriver.support.ui as ui
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class reviewscrapping:
    def __init__(self,hotel_name):
        self.hotel_name = hotel_name
        self.chrome_path = "chromedriver.exe"
        self.driver = webdriver.Chrome(self.chrome_path)
        self.final_review_list = []
        
    def take_review(self):
        review_list = self.driver.find_element_by_class_name('review_list');
        elementList = review_list.find_elements_by_tag_name("li")
        print(len(elementList))
        for i in range(len(elementList)):
            review_div = elementList[i].find_elements_by_class_name('c-review__body')
            for j in range(len(review_div)):
                print(review_div[j].text);
                self.final_review_list.append(review_div[j].text)
        
    def scarapping(self):
        self.driver.get("https://www.booking.com")
        bet_fa = self.driver.find_element_by_id("ss")
        bet_fa.clear()
        bet_fa.send_keys(self.hotel_name)
        self.driver.find_element_by_xpath("""//*[@id="frm"]/div[1]/div[4]/div[2]/button""").click()
        self.driver.find_element_by_xpath("""//*[@id="hotellist_inner"]/div[2]/div[2]/div[1]/div[1]/div[1]/h3/a""").click()
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.find_element_by_xpath("""//*[@id="show_reviews_tab"]""").click()
        var = 0
        try:
            while var==0:
                self.take_review()
                self.driver.find_element_by_xpath("""//*[@id="review_list_page_container"]/div[4]/div/div[1]/div/div[3]/a""").click()
                wait = ui.WebDriverWait(self.driver,10)
                element = wait.until(EC.visibility_of_element_located((By.XPATH, """//*[@id="review_list_page_container"]/div[4]/div/div[1]/div/div[3]/a""")))
        except:
            print("close")
        return self.final_review_list
