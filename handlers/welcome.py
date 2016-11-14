from handler import Handler
import models


class Welcome(Handler):
    def get(self):
        if self.read_secure_cookie("id"):
            user_id = int(self.read_secure_cookie("id"))
            username = models.User.by_id(user_id).username
            self.render('welcome.html', username = username)
        else:
            self.redirect('/login')
