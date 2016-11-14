from handler import Handler
import models



class Login(Handler):
    def write_form(self, no_user_error="", incorrect_password_error="", username=""):
        self.render("loginform.html",
                    no_user_error = no_user_error,
                    incorrect_password_error = incorrect_password_error,
                    username = username)

    def get(self):
        self.write_form()

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        no_user_error = ""
        incorrect_password_error = ""

        user = models.User.by_name(username)

        if user:
            if security.valid_pw(username, password, user.password_hash):
                self.set_secure_cookie("id", str(user.key().id()))
                self.redirect('/welcome')
            else:
                incorrect_password_error = "You have not entered the correct password for this user"
                self.write_form(no_user_error, incorrect_password_error, username)
        else:
            no_user_error = "this user does not exist"
            self.write_form(no_user_error, incorrect_password_error, username)
