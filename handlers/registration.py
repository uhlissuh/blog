from handler import Handler
import re
import models

#allows a new user to register to use platform
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")

class Registration(Handler):

    def valid_username(self, username):
        return USER_RE.match(username)

    def valid_password(self, password):
        return PASSWORD_RE.match(password)

    def valid_email(self, email):
        return EMAIL_RE.match(email)

    def write_form(self, username_error="", password_error="", verify_error="", email_error="", user_exists_error="", username="", email=""):
        self.render("usersignupform.html",
                    username_error = username_error,
                    password_error = password_error,
                    verify_error = verify_error,
                    email_error = email_error,
                    user_exists_error = user_exists_error,
                    username = username,
                    email = email)

    def get(self):
        self.write_form()

    def post(self):

        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        print("username is", username)

        username_error = ""
        password_error = ""
        verify_error = ""
        email_error = ""
        user_exists_error = ""

        if self.valid_username(username) == None:
            username_error = "this is not a valid username"

        if self.valid_password(password) == None:
            password_error = "this is not a valid password"

        if password != verify:
            verify_error = "passwords do not match"

        if email and self.valid_email(email) == None:
            email_error = "this is not a valid email"


        if username_error == "" and password_error == "" and verify_error == "" and email_error=="":
            if not models.User.by_name(username):
                user = models.User.register(username, password, email)
                user.put()
                user_id = str(user.key().id())
                self.set_secure_cookie("id", user_id)
                self.redirect("/welcome")
            else:
                user_exists_error = "this user already exists"
                self.write_form(user_exists_error = user_exists_error)
        else:
            self.write_form(username_error, password_error, verify_error, user_exists_error, email_error, username, email)
