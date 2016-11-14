#!/usr/bin/env python


from handlers.handler import Handler
from handlers.mainpage import MainPage
from handlers.newpost import NewPost
from handlers.showpost import ShowPost
from handlers.registration import Registration
from handlers.welcome import Welcome
from handlers.login import Login
from handlers.logout import Logout
from handlers.editpost import EditPost
from handlers.like import Like
from handlers.unlike import Unlike
import webapp2
import security
import models


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/newpost', NewPost),
    (r'/post/(\d+)', ShowPost),
    ('/signup', Registration),
    ('/welcome', Welcome),
    ('/login', Login),
    ('/logout', Logout),
    (r'/editpost/(\d+)', EditPost),
    (r'/post/(\d+)/like', Like),
    (r'/post/(\d+)/unlike', Unlike)

], debug=True)
