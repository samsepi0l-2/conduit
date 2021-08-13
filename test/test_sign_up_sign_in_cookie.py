from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from datas import *
from common_steps import *

class TestConduitakarmi(object):
    def setup(self):
        browser_options = Options()
        browser_options.headless = True
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=browser_options)
        # self.driver = webdriver.Chrome()
        self.driver.get("http://conduitapp.progmasters.hu:1667")

    def teardown(self):
        self.driver.quit()

    # A_TC_001
    # Registration with bad e-mail format
    def test_bad_mail_registration(self):
        nav_out = navbar_out(self.driver)
        nav_out[2].click()

        username_reg_field = self.driver.find_element_by_xpath("//input[@placeholder='Username']")
        email_reg_field = self.driver.find_element_by_xpath("//input[@placeholder='Email']")
        password_reg_field = self.driver.find_element_by_xpath("//input[@placeholder='Password']")
        sign_up_send_btn = self.driver.find_element_by_xpath("//button[@class= 'btn btn-lg btn-primary pull-xs-right']")

        username_reg_field.send_keys(username_good_format)
        email_reg_field.send_keys(email_bad_format)
        password_reg_field.send_keys(password_good_format)
        sign_up_send_btn.click()

        time.sleep(2)
        swal_text = self.driver.find_element_by_xpath("//div[@class= 'swal-text']")

        assert swal_text.text == wrong_email_msg

    # A_TC_002
    # Cookie statement with accept and decline options
    def test_cookies(self):
        self.driver.maximize_window()

        decline_btn = self.driver.find_element_by_xpath(
            "//button[@class= 'cookie__bar__buttons__button cookie__bar__buttons__button--decline']")

        decline_btn.click()
        cookie_decline = self.driver.get_cookie("vue-cookie-accept-decline-cookie-policy-panel")

        assert cookie_decline["value"] == "decline"

        self.driver.delete_cookie("vue-cookie-accept-decline-cookie-policy-panel")
        self.driver.refresh()
        time.sleep(2)

        accept_btn = self.driver.find_element_by_xpath(
            "//button[@class= 'cookie__bar__buttons__button cookie__bar__buttons__button--accept']")
        accept_btn.click()
        cookie_accept = self.driver.get_cookie("vue-cookie-accept-decline-cookie-policy-panel")

        assert cookie_accept["value"] == "accept"
        time.sleep(2)

    # A_TC_003
    # Registration with valid data
    def test_good_registration(self):
        nav_out = navbar_out(self.driver)
        nav_out[2].click()

        username_reg_field = self.driver.find_element_by_xpath("//input[@placeholder='Username']")
        email_reg_field = self.driver.find_element_by_xpath("//input[@placeholder='Email']")
        password_reg_field = self.driver.find_element_by_xpath("//input[@placeholder='Password']")
        sign_up_send_btn = self.driver.find_element_by_xpath("//button[@class= 'btn btn-lg btn-primary pull-xs-right']")

        username_reg_field.send_keys(username_good_format)
        email_reg_field.send_keys(email_good_format)
        password_reg_field.send_keys(password_good_format)
        sign_up_send_btn.click()

        time.sleep(2)

        success_reg_msg = self.driver.find_element_by_xpath("//div[@class='swal-text']")

        # sweet alert window test
        assert success_reg_msg.text == "Your registration was successful!"

        reg_success_ok_btn = self.driver.find_element_by_xpath(
            "//div/button[@class='swal-button swal-button--confirm']")
        reg_success_ok_btn.click()

        # username test
        nav_in = navbar_in(self.driver)
        assert nav_in[3].text == username_good_format

    # A_TC_004
    # Logout
    def test_logout(self):
        login(self.driver)
        nav_in = navbar_in(self.driver)
        nav_in[4].click()
        session_cookie = self.driver.get_cookie("drash_sess")
        assert session_cookie["value"] == "null"

    # A_TC_005
    # Login with a permanent account
    def test_signin(self):
        nav_out = navbar_out(self.driver)
        nav_out[1].click()

        # site url test
        assert self.driver.current_url == login_site

        # session cookie test before login
        assert self.driver.get_cookie("drash_sess")["value"] == "null"

        email_sign_in_field = self.driver.find_element_by_xpath("//input[@placeholder='Email']")
        password_sign_in_field = self.driver.find_element_by_xpath("//input[@placeholder='Password']")
        sign_in_send_btn = self.driver.find_element_by_xpath("//button[@class= 'btn btn-lg btn-primary pull-xs-right']")

        email_sign_in_field.send_keys(permanent_email)
        password_sign_in_field.send_keys(permanent_password)
        sign_in_send_btn.click()

        time.sleep(1)

        # session cookie test after login
        assert self.driver.get_cookie("drash_sess")["value"] != "null"

        nav_in = navbar_in(self.driver)

        # username test after login
        assert nav_in[3].text == "jozsefteszt"

    # A_TC_006
    # New blogpost
    def test_new_post(self):
        login(self.driver)
        nav_in=navbar_in(self.driver)
        nav_in[1].click()
        time.sleep(1)

        article_title_field = self.driver.find_element_by_xpath("//input[@placeholder='Article Title']")
        article_about_field = self.driver.find_element_by_xpath("//input[contains(@placeholder,'this article about')]")
        article_body_field = self.driver.find_element_by_xpath(
            "//textarea[@placeholder='Write your article (in markdown)']")
        article_tag_field = self.driver.find_element_by_xpath("//input[@placeholder='Enter tags']")
        article_publish_btn = self.driver.find_element_by_xpath("//button[@class= 'btn btn-lg pull-xs-right btn-primary']")

        article_title_field.send_keys("titleteszt3")
        article_about_field.send_keys("aboutteszt")
        article_body_field.send_keys("bodyteszt")
        article_tag_field.send_keys("tagteszt")
        article_publish_btn.click()

        time.sleep(2)
        article_url = self.driver.current_url

        assert article_url == "http://conduitapp.progmasters.hu:1667/#/articles/titleteszt3"

        delete_current_article(self.driver)

    # A_TC_007
    # Edit article
    def test_edit_article(self):
        login(self.driver)
        new_article(self.driver)

        edit_btn = self.driver.find_element_by_xpath("//a[contains(@href,'editor/titleteszt3')]")
        edit_btn.click()
        time.sleep(1)
        article_body_field = self.driver.find_element_by_xpath(
            "//textarea[@placeholder='Write your article (in markdown)']")
        article_body_field.send_keys(" EDITED")
        article_publish_btn = self.driver.find_element_by_xpath("//button[@class= 'btn btn-lg pull-xs-right btn-primary']")
        article_publish_btn.click()
        time.sleep(1)

        edited_contetnt = self.driver.find_element_by_xpath("//div[@class = 'row article-content']/div/div/p")

        assert edited_contetnt.text == "bodyteszt EDITED"

        delete_current_article(self.driver)

    # A_TC_008
    # Delete article
    def test_del_article(self):
        login(self.driver)
        new_article(self.driver)
        article_url = self.driver.current_url

        nav_in = navbar_in(self.driver)
        nav_in[0].click()
        time.sleep(1)

        titles_before_delete = self.driver.find_elements_by_xpath("//a[@class='preview-link']/h1")
        before_delete_list = []
        for i in titles_before_delete:
            before_delete_list.append(i.text)

        self.driver.get(article_url)
        time.sleep(1)

        delete_current_article(self.driver)
        time.sleep(2)

        titles_after_delete = self.driver.find_elements_by_xpath("//a[@class='preview-link']/h1")
        after_delete_list = []
        for i in titles_after_delete:
            after_delete_list.append(i.text)

        deleted_title = ""
        for i in before_delete_list:
            if i not in after_delete_list:
                deleted_title = deleted_title + i

        assert deleted_title == "titleteszt3"

    # data from file
    def test_data_from_file(self):
        login(self.driver)

        # new post
        nav_in= navbar_in(self.driver)
        nav_in[1].click()
        time.sleep(1)
        article_title_field = self.driver.find_element_by_xpath("//input[@placeholder='Article Title']")
        article_about_field = self.driver.find_element_by_xpath("//input[contains(@placeholder,'this article about')]")
        article_body_field = self.driver.find_element_by_xpath("//textarea[@placeholder='Write your article (in markdown)']")
        article_tag_field = self.driver.find_element_by_xpath("//input[@placeholder='Enter tags']")
        article_publish_btn = self.driver.find_element_by_xpath("//button[@class= 'btn btn-lg pull-xs-right btn-primary']")

        article_title_field.send_keys("commentitle")
        article_about_field.send_keys("commentabout")
        article_body_field.send_keys("commnetbody")
        article_tag_field.send_keys("commentag")
        article_publish_btn.click()

        time.sleep(2)
        # comments sending
        comment_field = self.driver.find_element_by_xpath("//textarea[@placeholder='Write a comment...']")
        comment_btn = self.driver.find_element_by_xpath("//div[@class= 'card-footer']/button")

        with open("input_data.txt", "r") as file:
            comment_lines = file.readlines()
            for i in comment_lines:
                comment = i.strip()
                comment_field.send_keys(comment)
                comment_btn.click()
                time.sleep(1)

        # comment assertion
        comment_list = self.driver.find_elements_by_xpath("//p[@class = 'card-text']")
        stripped_list = []
        text_list = []
        for i in range(len(comment_lines) - 1, -1, -1):
            stripped_list.append(comment_lines[i].strip())

        for k in comment_list:
            text_list.append(k.text)

        assert stripped_list == text_list

        delete_current_article(self.driver)
        time.sleep(2)

# data to file
    def test_data_to_file(self):
        login(self.driver)
        time.sleep(2)
        authors = self.driver.find_elements_by_xpath("//a[@class = 'author']")
        titles = self.driver.find_elements_by_xpath("//a[@class = 'preview-link']/h1")
        summaries = self.driver.find_elements_by_xpath("//a[@class = 'preview-link']/p")
        likes = self.driver.find_elements_by_xpath("//span[@class = 'counter']")

        with open('output_data.csv', 'w', encoding='utf-8') as new_csv:
            new_csv.write("author" + "," + "title" + "," + "summary" + "," + "number_of_likes" + "\n")
            for i in range(len(authors) - 1):
                new_csv.write(authors[i].text + "," + titles[i].text + "," + summaries[i].text + "," + likes[i].text + "\n")

        with open('output_data.csv', 'r', encoding="utf-8") as file:
            rows = list(file)

            random_line_index = secrets.randbelow(len(authors) - 1)

            random_article = f"{authors[random_line_index].text},{titles[random_line_index].text},{summaries[random_line_index].text},{likes[random_line_index].text}\n"
            random_file_line = rows[random_line_index + 1]
            assert random_article == random_file_line

    # listig
    def test_listing(self):
        login(self.driver)
        self.driver.get("http://conduitapp.progmasters.hu:1667/#/tag/lorem_tag")
        time.sleep(2)

        tags_in_article = self.driver.find_elements_by_xpath("//a[@class= 'preview-link']/div/a")
        articles_with_current_tag = self.driver.find_elements_by_xpath("//a[@class = 'preview-link']/h1")
        tag_counter = 0
        for i in range(len(tags_in_article)):
            if "lorem_tag" in tags_in_article[i].text:
                tag_counter += 1

        assert len(articles_with_current_tag) == tag_counter

    # pagination
    def test_pagination(self):
        login(self.driver)
        time.sleep(2)
        page_btns = self.driver.find_elements_by_xpath("//ul[@class = 'pagination']/li/a")

        for i in range(len(page_btns)):
            page_btns[i].click()

        time.sleep(1)
        current_page = self.driver.find_element_by_xpath("//li[@class = 'page-item active']/a")

        assert int(current_page.text) == len(page_btns)
