from handler import Handler
import models

#allows creator of blogpost to edit it
class EditPost(Handler):
    def get(self, id):
        blog = models.BlogPost.by_id(int(id))
        if blog:
            author_id = blog.author_id
            cookie_id = self.read_secure_cookie("id")
            if cookie_id == author_id:
                subject = blog.subject
                content = blog.content
                blog_id = id
                self.render("/editpost.html", subject = subject, content = content, blog_id = blog_id)
            else:
                self.redirect('/login')
        else:
            self.render_404()

    def post(self, id):
        blog = models.BlogPost.by_id(int(id))
        author_id = blog.author_id

        subject = self.request.get("subject")
        content = self.request.get("content")

        if author_id == str(self.read_secure_cookie("id")):
            blog.subject = subject
            blog.content = content

            blog.put()
            self.redirect('/post/' + id)
        else:
            self.render_404()
