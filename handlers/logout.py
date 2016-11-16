from handler import Handler

#allows a logged in user to log out
class Logout(Handler):
    def get(self):
        if self.read_secure_cookie("id"):
            self.logout()
            self.redirect('/login')
        else:
            self.response.set_status(404, message="not permitted")
            self.render('404_error.html')
