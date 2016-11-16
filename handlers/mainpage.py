from google.appengine.ext import db
from handler import Handler

#displays from page of blog platform with all blog posts
class MainPage(Handler):
    def get(self):
        is_signed_in = False
        if self.read_secure_cookie("id"):
            is_signed_in = True

        posts = db.GqlQuery("SELECT * FROM BlogPost ORDER BY created DESC")

        self.render("front.html", posts=posts, is_signed_in=is_signed_in)
