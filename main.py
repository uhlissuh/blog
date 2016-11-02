#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import os
import jinja2
import re
from google.appengine.ext import db

#project files import
import security
import models


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)


class Handler(webapp2.RequestHandler):
    def render(self, template, **kw):
        t = jinja_env.get_template(template)
        self.response.out.write(t.render(**kw))

    def set_secure_cookie(self, name, val):
        cookie_id = security.make_secure_val(val)
        self.response.headers.add_header('Set-Cookie','%s=%s, Path=/' % (name, cookie_id))

    def read_secure_cookie(self, name):
        cookie_id = self.request.cookies.get(name)
        return cookie_id and security.check_secure_val(cookie_id)

class MainPage(Handler):
    def get(self):
        posts = db.GqlQuery("SELECT * FROM BlogPost ORDER BY created DESC")
        self.render("front.html", posts=posts)


class NewPost(Handler):
    def render_form(self, subject="", content="", error=""):
        self.render("newpost.html", subject = subject, content = content, error = error)

    def get(self):
        self.render_form()

    def post(self):
        subject = self.request.get("subject")
        content = self.request.get("content")

        if subject and content:
            p = models.BlogPost(subject = subject, content = content)
            p.put()

            post_id = str(p.key().id())

            self.redirect("/post/" + post_id)

        else:
            error = "we need both a title and some content!"
            self.render_form(subject, content, error)

class ShowPost(Handler):
    def get(self, id):
        subject = models.BlogPost.get_by_id(int(id)).subject
        content = models.BlogPost.get_by_id(int(id)).content
        created = models.BlogPost.get_by_id(int(id)).created

        self.render("post.html", subject=subject, content=content, created=created)

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
            self.write_form(username_error, password_error, verify_error, email_error, username, email)

class Welcome(Handler):
    def get(self):
        username = ""
        user_id = int(self.read_secure_cookie("id"))
        username = models.User.by_id(user_id).username
        self.render('welcome.html', username = username)

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
            
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/newpost', NewPost),
    (r'/post/(\d+)', ShowPost),
    ('/signup', Registration),
    ('/welcome', Welcome),
    ('/login', Login)
], debug=True)
