from handler import Handler
import models


class EditPost(Handler):
    def get(self, id):
        blog = models.BlogPost.by_id(int(id))
        subject = blog.subject
        content = blog.content

        self.render("/editpost.html", subject = subject, content = content)

    def post(self, id):
        blog = models.BlogPost.by_id(int(id))
        author_id = blog.author_id

        subject = self.request.get("subject")
        content = self.request.get("content")

        if author_id == str(self.read_secure_cookie("id")):
            blog.subject = subject
            blog.content = content

            blog.put()
            self.redirect('/')
        else:
            self.response.set_status(404)
            self.render('/404_error.html')
