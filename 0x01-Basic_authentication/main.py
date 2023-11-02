#!/usr/bin/env python3
""" Main 3
"""
# from api.v1.auth.basic_auth import BasicAuth

# a = BasicAuth()

# print(a.decode_base64_authorization_header(None))
# print(a.decode_base64_authorization_header(89))
# print(a.decode_base64_authorization_header("Holberton School"))
# print(a.decode_base64_authorization_header("SG9sYmVydG9u"))
# print(a.decode_base64_authorization_header("SG9sYmVydG9uIFNjaG9vbA=="))
# print(a.decode_base64_authorization_header(a.extract_base64_authorization_header("Basic SG9sYmVydG9uIFNjaG9vbA==")))

import base64
from api.v1.auth.basic_auth import BasicAuth
from models.user import User

""" Create a user test """
user_email = "bob100@hbtn.io"
user_clear_pwd = "H0lberton:School:98!"

user = User()
user.email = user_email
user.password = user_clear_pwd
print("New user: {}".format(user.id))
user.save()

basic_clear = "{}:{}".format(user_email, user_clear_pwd)
print("Basic Base64: {}".format(base64.b64encode(basic_clear.encode('utf-8')).decode("utf-8")))
#Ym9iMTAwQGhidG4uaW86SDBsYmVydG9uOlNjaG9vbDo5OCE=