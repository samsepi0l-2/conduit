import secrets
import time
import csv

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

# real registration
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

# login
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
# username ellenérzés a random adatoknál
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

# edit article

edit_btn = browser.find_element_by_xpath("//a[contains(@href,'editor/titleteszt3')]")
edit_btn.click()
time.sleep(1)
article_body_field = browser.find_element_by_xpath("//textarea[@placeholder='Write your article (in markdown)']")
article_body_field.send_keys(" EDITED")
article_publish_btn = browser.find_element_by_xpath("//button[@class= 'btn btn-lg pull-xs-right btn-primary']")
article_publish_btn.click()
time.sleep(1)

edited_contetnt = browser.find_element_by_xpath("//div[@class = 'row article-content']/div/div/p")
assert edited_contetnt.text == "bodyteszt EDITED"
browser.back()

# delete article
navbar_all_item_logged_in = browser.find_elements_by_xpath("//li[@class= 'nav-item']")
navbar_all_item_logged_in[0].click()
time.sleep(1)
titles_before_delete = browser.find_elements_by_xpath("//a[@class='preview-link']/h1")
before_delete_list = []
for i in titles_before_delete:
    before_delete_list.append(i.text)

browser.back()
browser.back()
time.sleep(1)

delete_btn = browser.find_element_by_xpath("//button[@class='btn btn-outline-danger btn-sm']")
delete_btn.click()

# delete_msg = browser.find_element_by_xpath("//div[@class='swal-overlay']/div/div")
# print(delete_msg.text)
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

assert deleted_title == "titleteszt3"

# data from file
#       new post
navbar_all_item_logged_in = browser.find_elements_by_xpath("//li[@class= 'nav-item']")
navbar_all_item_logged_in[1].click()
time.sleep(1)
article_title_field = browser.find_element_by_xpath("//input[@placeholder='Article Title']")
article_about_field = browser.find_element_by_xpath("//input[contains(@placeholder,'this article about')]")
article_body_field = browser.find_element_by_xpath("//textarea[@placeholder='Write your article (in markdown)']")
article_tag_field = browser.find_element_by_xpath("//input[@placeholder='Enter tags']")
article_publish_btn = browser.find_element_by_xpath("//button[@class= 'btn btn-lg pull-xs-right btn-primary']")

article_title_field.send_keys("commentitle")
article_about_field.send_keys("commentabout")
article_body_field.send_keys("commnetbody")
article_tag_field.send_keys("commentag")
article_publish_btn.click()

time.sleep(2)
comment_field = browser.find_element_by_xpath("//textarea[@placeholder='Write a comment...']")
comment_btn = browser.find_element_by_xpath("//div[@class= 'card-footer']/button")

with open("input_data.txt", "r") as file:
    comment_lines = file.readlines()
    for i in comment_lines:
        comment = i.strip()
        comment_field.send_keys(comment)
        comment_btn.click()
        time.sleep(1)

comment_list = browser.find_elements_by_xpath("//p[@class = 'card-text']")
stripped_list = []
text_list = []
for i in range(len(comment_lines) - 1, -1, -1):
    stripped_list.append(comment_lines[i].strip())

for k in comment_list:
    text_list.append(k.text)

# ciklusok nélkül
# assert comment_list[0].text == comment_lines[2].strip() and comment_list[1].text == comment_lines[1].strip() and \
#        comment_list[2].text == comment_lines[0].strip()

assert stripped_list == text_list

delete_btn = browser.find_element_by_xpath("//button[@class='btn btn-outline-danger btn-sm']")
delete_btn.click()
time.sleep(2)

# data to file
authors = browser.find_elements_by_xpath("//a[@class = 'author']")
titles = browser.find_elements_by_xpath("//a[@class = 'preview-link']/h1")
summaries = browser.find_elements_by_xpath("//a[@class = 'preview-link']/p")
likes = browser.find_elements_by_xpath("//span[@class = 'counter']")
# header = ['author', 'title', 'summary', 'number_of_likes']

with open('output_data.csv', 'w', encoding='utf-8') as new_csv:
    # writer = csv.writer(new_csv)
    # writer.writerow(header)
    new_csv.write("author" + "," + "title" + "," + "summary" + "," + "number_of_likes" + "\n")
    for i in range(len(authors) - 1):
        new_csv.write(authors[i].text + "," + titles[i].text + "," + summaries[i].text + "," + likes[i].text + "\n")

with open('output_data.csv', 'r', encoding="utf-8") as file:
    reader = csv.reader(file, delimiter=',')
    rows = list(file)

    random_line_index = secrets.randbelow(len(authors))

    print(rows[8])
    print(titles[7].text)
    print(random_line_index)
time.sleep(15)
browser.quit()
