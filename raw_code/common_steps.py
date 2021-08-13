def navbar_in(browser):
    navbar_all_item_logged_in = browser.find_elements_by_xpath("//li[@class= 'nav-item']")
    return navbar_all_item_logged_in
