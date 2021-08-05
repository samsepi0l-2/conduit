import secrets
import time

from selenium import webdriver
import os.path
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

browser = webdriver.Chrome()

browser.get("http://conduitapp.progmasters.hu:1667")

# registration test
sign_up_nav_btn = browser.find_element_by_xpath("//li/a[@href='#/register']")
sign_up_nav_btn.click()
register_site = "http://conduitapp.progmasters.hu:1667/#/register"
assert browser.current_url == register_site

username_reg_field = browser.find_element_by_xpath("//input[@placeholder='Username']")
email_reg_field = browser.find_element_by_xpath("//input[@placeholder='Email']")
password_reg_field = browser.find_element_by_xpath("//input[@placeholder='Password']")
sign_up_send_btn = browser.find_element_by_xpath("//button[@class= 'btn btn-lg btn-primary pull-xs-right']")

random_email_token = secrets.token_hex(6)
username_good_format = "Tesztjozsef"
email_good_format = f"{random_email_token}@jozsef.hu"
email_bad_format = "jozsef"
password_good_format = "ASDFasdf123"
password_bad_format = "asdf"

username_reg_field.send_keys(username_good_format)
email_reg_field.send_keys(email_bad_format)
password_reg_field.send_keys(password_good_format)
sign_up_send_btn.click()

time.sleep(2)
swal_text = browser.find_element_by_xpath("//div[@class= 'swal-text']")

wrong_email_msg = "Email must be a valid email."
taken_email_msg = "Email already taken. "
wrong_password_msg = "Password must be 8 characters long and include 1 number, 1 uppercase letter, and 1 lowercase letter. "
assert swal_text.text == wrong_email_msg

## cookie test
swal_ok_btn = browser.find_element_by_xpath("//button[@class = 'swal-button swal-button--confirm']")
swal_ok_btn.click()

decline_btn = browser.find_element_by_xpath(
    "//button[@class= 'cookie__bar__buttons__button cookie__bar__buttons__button--decline']")

decline_btn.click()
cookie_decline = browser.get_cookie("vue-cookie-accept-decline-cookie-policy-panel")

assert cookie_decline["value"] == "decline"

browser.delete_cookie("vue-cookie-accept-decline-cookie-policy-panel")
browser.refresh()

time.sleep(2)
accept_btn = browser.find_element_by_xpath(
    "//button[@class= 'cookie__bar__buttons__button cookie__bar__buttons__button--accept']")
accept_btn.click()
cookie_accept = browser.get_cookie("vue-cookie-accept-decline-cookie-policy-panel")

assert cookie_accept["value"] == "accept"

time.sleep(2)


#real registration
username_reg_field = browser.find_element_by_xpath("//input[@placeholder='Username']")
email_reg_field = browser.find_element_by_xpath("//input[@placeholder='Email']")
password_reg_field = browser.find_element_by_xpath("//input[@placeholder='Password']")
sign_up_send_btn = browser.find_element_by_xpath("//button[@class= 'btn btn-lg btn-primary pull-xs-right']")

username_reg_field.send_keys(username_good_format)
email_reg_field.send_keys(email_good_format)
password_reg_field.send_keys(password_good_format)
sign_up_send_btn.click()

time.sleep(2)

success_reg_msg = browser.find_element_by_xpath("//div[@class='swal-text']")
assert success_reg_msg.text == "Your registration was successful!"

reg_success_ok_btn = browser.find_element_by_xpath("//div/button[@class='swal-button swal-button--confirm']")
reg_success_ok_btn.click()

# username test
navbar_all_item_logged_in = browser.find_elements_by_xpath("//li[@class= 'nav-item']")
assert navbar_all_item_logged_in[3].text == username_good_format

# logout test
navbar_all_item_logged_in[4].click()
session_cookie = browser.get_cookie("drash_sess")
assert session_cookie["value"] == "null"

#login
navbar_all_item_logged_out = browser.find_elements_by_xpath("//li[@class= 'nav-item']")
navbar_all_item_logged_out[1].click()

login_site = "http://conduitapp.progmasters.hu:1667/#/login"
assert browser.current_url == login_site

assert browser.get_cookie("drash_sess")["value"] == "null"

email_sign_in_field = browser.find_element_by_xpath("//input[@placeholder='Email']")
password_sign_in_field = browser.find_element_by_xpath("//input[@placeholder='Password']")
sign_in_send_btn = browser.find_element_by_xpath("//button[@class= 'btn btn-lg btn-primary pull-xs-right']")

# random felhasználó bejelentkezés
# email_sign_in_field.send_keys(email_good_format)
# password_sign_in_field.send_keys(password_good_format)
# sign_in_send_btn.click()

# átmeneti égetett adatok postoláshoz és post törléséhez
email_sign_in_field.send_keys("jozsefteszt@jozsefteszt.hu")
password_sign_in_field.send_keys("asdfASDF123")
sign_in_send_btn.click()

time.sleep(1)
assert browser.get_cookie("drash_sess")["value"] != "null"

navbar_all_item_logged_in = browser.find_elements_by_xpath("//li[@class= 'nav-item']")
# usernam ellenérzés a random adatoknál
# assert navbar_all_item_logged_in[3].text == username_good_format

# username ellenőrzés az átmeneti égetett adatokkal
assert navbar_all_item_logged_in[3].text == "jozsefteszt"

# new post
navbar_all_item_logged_in[1].click()
time.sleep(1)

article_title_field = browser.find_element_by_xpath("//input[@placeholder='Article Title']")
article_about_field = browser.find_element_by_xpath("//input[contains(@placeholder,'this article about')]")
article_body_field = browser.find_element_by_xpath("//textarea[@placeholder='Write your article (in markdown)']")
article_tag_field = browser.find_element_by_xpath("//input[@placeholder='Enter tags']")
article_publish_btn = browser.find_element_by_xpath("//button[@class= 'btn btn-lg pull-xs-right btn-primary']")

article_title_field.send_keys("titleteszt3")
article_about_field.send_keys("aboutteszt")
article_body_field.send_keys("bodyteszt")
article_tag_field.send_keys("tagteszt")
article_publish_btn.click()

time.sleep(2)
article_url = browser.current_url
assert article_url == "http://conduitapp.progmasters.hu:1667/#/articles/titleteszt3"

# delete article
navbar_all_item_logged_in = browser.find_elements_by_xpath("//li[@class= 'nav-item']")
navbar_all_item_logged_in[0].click()
time.sleep(1)
titles_before_delete = browser.find_elements_by_xpath("//a[@class='preview-link']/h1")
before_delete_list = []
for i in titles_before_delete:
    before_delete_list.append(i.text)

browser.back()
time.sleep(1)

delete_btn = browser.find_element_by_xpath("//button[@class='btn btn-outline-danger btn-sm']")
delete_btn.click()

delete_msg = browser.find_element_by_xpath("//div[@class='swal-overlay']/div/div")
print(delete_msg.text)
time.sleep(2)
titles_after_delete = browser.find_elements_by_xpath("//a[@class='preview-link']/h1")
after_delete_list = []
for i in titles_after_delete:
    after_delete_list.append(i.text)

difference = []
deleted_title = ""
for i in before_delete_list:
  if i not in after_delete_list:
    deleted_title = deleted_title + i

assert  deleted_title == "titleteszt3"
time.sleep(5)
browser.quit()
