from handler import Handler
import models


#allows logged in user to create a new post
class NewPost(Handler):
    def render_form(self, subject="", content="", error=""):
        self.render("newpost.html", subject = subject, content = content, error = error)

    def get(self):
        cookie_id = self.read_secure_cookie('id')
        if cookie_id:
            self.render_form()
        else:
            self.redirect('/login')

    def post(self):
        cookie_id = self.read_secure_cookie('id')
        if cookie_id:
            subject = self.request.get("subject")
            content = self.request.get("content")
            author_id = str(self.read_secure_cookie("id"))

            if subject and content and author_id:
                p = models.BlogPost(subject = subject, content = content, author_id = author_id)
                p.put()

                post_id = str(p.key().id())

                self.redirect("/post/" + post_id)

            else:
                error = "we need both a title and some content!"
                self.render_form(subject, content, error)
        else:
            self.render_404()
