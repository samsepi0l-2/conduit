from selenium import webdriver
import time


def navbar_in(browser):
    navbar_all_item_logged_in = browser.find_elements_by_xpath("//li[@class= 'nav-item']")
    return navbar_all_item_logged_in


def navbar_out(browser):
    navbar_all_item_logged_out = browser.find_elements_by_xpath("//li[@class= 'nav-item']")
    return navbar_all_item_logged_out


def login(driver):
    nav_out = navbar_out(driver)
    nav_out[1].click()
    email_sign_in_field = driver.find_element_by_xpath("//input[@placeholder='Email']")
    password_sign_in_field = driver.find_element_by_xpath("//input[@placeholder='Password']")
    sign_in_send_btn = driver.find_element_by_xpath("//button[@class= 'btn btn-lg btn-primary pull-xs-right']")
    email_sign_in_field.send_keys("jozsefteszt@jozsefteszt.hu")
    password_sign_in_field.send_keys("asdfASDF123")
    sign_in_send_btn.click()
    time.sleep(1)


def new_article(driver):
    nav_in = navbar_in(driver)
    nav_in[1].click()
    time.sleep(1)
    article_title_field = driver.find_element_by_xpath("//input[@placeholder='Article Title']")
    article_about_field = driver.find_element_by_xpath("//input[contains(@placeholder,'this article about')]")
    article_body_field = driver.find_element_by_xpath("//textarea[@placeholder='Write your article (in markdown)']")
    article_tag_field = driver.find_element_by_xpath("//input[@placeholder='Enter tags']")
    article_publish_btn = driver.find_element_by_xpath("//button[@class= 'btn btn-lg pull-xs-right btn-primary']")
    article_title_field.send_keys("titleteszt3")
    article_about_field.send_keys("aboutteszt")
    article_body_field.send_keys("bodyteszt")
    article_tag_field.send_keys("tagteszt")
    article_publish_btn.click()
    time.sleep(2)


def delete_current_article(driver):
    delete_btn = driver.find_element_by_xpath("//button[@class='btn btn-outline-danger btn-sm']")
    delete_btn.click()
