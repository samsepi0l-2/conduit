import secrets

# A_TC_001
# A_TC_003
random_email_token = secrets.token_hex(6)
username_good_format = "Tesztjozsef"
email_good_format = f"{random_email_token}@jozsef.hu"
email_bad_format = "jozsef"
password_good_format = "ASDFasdf123"

# A_TC_001
wrong_email_msg = "Email must be a valid email."
taken_email_msg = "Email already taken. "
wrong_password_msg = "Password must be 8 characters long and include 1 number, 1 uppercase letter, and 1 lowercase letter. "

# A_TC_005
login_site = "http://conduitapp.progmasters.hu:1667/#/login"
permanent_email = "jozsefteszt@jozsefteszt.hu"
permanent_password = "asdfASDF123"

# A_TC_011
tested_tag = "lorem_tag"