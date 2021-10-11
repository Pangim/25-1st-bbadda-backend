import re

def validate_email(email):
    email_pattern = '[a-zA-Z0-9\-_]+@[a-zA-Z0-9\-_]+.[a-zA-Z0-9\.\-_]+'
    user_email    = re.match(email_pattern, email)
    if user_email != None:
        return user_email.group()

def validate_password(password):
    password_pattern = '(?=.*[a-zA-Z0-9])(?=.*[0-9!@#\$\%\*\^])(?=.*[a-zA-Z!@#\$\%\*\^]).+'
    user_password    = re.match(password_pattern, password)
    if user_password != None:
        return user_password.group()