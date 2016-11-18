from handler import Handler
import models

#allows creator of comment to delete it
class DeleteComment(Handler):
    def post(self, blog_id, comment_id):
        comment = models.Comment.by_id(int(comment_id))
        if comment:
            commenter_id = comment.commenter_id
            cookie_id = int(self.read_secure_cookie("id"))
            if cookie_id:
                if cookie_id == commenter_id:
                    comment.delete()
                    self.redirect("/post/" + blog_id)
                else:
                    self.response.set_status(404, message="not permitted")
                    self.render('404_error.html')
            else:
                self.redirect('/login')
        else:
            self.render_404()
