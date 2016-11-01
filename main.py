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
import hashlib
import random
import hmac
from string import letters

from google.appengine.ext import db

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")

secret = "fdfdf434@!^&*AAAA"

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

#secure cookie stuff
def make_secure_val(val):
    return '%s|%s' % (val, hmac.new(secret, val).hexdigest())

def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val

#user encryption stuff
def make_salt(length = 5):
    return ''.join(random.choice(letters) for x in xrange(length))

def make_password_hash(name, pw, salt = None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s|%s' % (h, salt)

def valid_pw(name, pw, h):
    salt = h.split('|')[0]
    return h == make_password_hash(name, pw, salt)


class Handler(webapp2.RequestHandler):
    def render(self, template, **kw):
        t = jinja_env.get_template(template)
        self.response.out.write(t.render(**kw))

    def set_secure_cookie(self, name, val):
        cookie_id = make_secure_val(val)
        self.response.headers.add_header('Set-Cookie','%=%, Path=/' % (name, cookie_id))

    def read_secure_cookie(self, name):
        cookie_id = self.request.cookies.get(name)
        return cookie_id and check_secure_val(cookie_val)

class BlogPost(db.Model):
    subject = db.StringProperty(required = True)
    content = db.StringProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class User(db.Model):
     username = db.StringProperty(required = True)
     email = db.StringProperty()
     password_hash = db.StringProperty(required = True)

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
            p = BlogPost(subject = subject, content = content)
            p.put()

            post_id = str(p.key().id())

            self.redirect("/post/" + post_id)

        else:
            error = "we need both a title and some content!"
            self.render_form(subject, content, error)

class ShowPost(Handler):
    def get(self, id):
        subject = BlogPost.get_by_id(int(id)).subject
        content = BlogPost.get_by_id(int(id)).content
        created = BlogPost.get_by_id(int(id)).created

        self.render("post.html", subject=subject, content=content, created=created)

class Registration(Handler):

    def valid_username(username):
        return USER_RE.match(username)

    def valid_password(password):
        return PASSWORD_RE.match(password)

    def valid_email(email):
        return EMAIL_RE.match(email)

    def write_form(self, username_error="", password_error="", verify_error="", email_error="", username="", email=""):
        self.render("usersignupform.html", username_error = username_error, password_error = password_error, verify_error = verify_error, email_error = email_error, username = username, email = email)

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

        if valid_username(username) == None:
            username_error = "this is not a valid username"

        if valid_password(password) == None:
            password_error = "this is not a valid password"

        if password != verify:
            verify_error = "passwords do not match"

        if email and valid_email(email) == None:
            email_error = "this is not a valid email"


        if username_error == "" and password_error == "" and verify_error == "" and email_error=="":
            #u = User.all().filter('name' = name).get()

            password_hash = make_password_hash(username, password)
            user = User(username = username, email = email, password_hash = password_hash)
            user.put()
            self.redirect("/")
        else:
            self.write_form(username_error, password_error, verify_error, email_error, username, email)



app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/newpost', NewPost),
    (r'/post/(\d+)', ShowPost),
    ('/signup', Registration)
], debug=True)
