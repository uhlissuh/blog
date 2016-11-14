from google.appengine.ext import db
from handler import Handler


class MainPage(Handler):
    def get(self):
        posts = db.GqlQuery("SELECT * FROM BlogPost ORDER BY created DESC")
        self.render("front.html", posts=posts)
