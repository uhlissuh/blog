from handler import Handler
import models


class Like(Handler):
    def post(self, id):
        author_id = models.BlogPost.by_id(int(id)).author_id
        user_id = self.read_secure_cookie("id")

        if user_id:
            if user_id != author_id:
                like = models.Like(user_id = int(user_id), blog_id = int(id))
                like.put()
                self.redirect('/post/'+ id)
            else:
                self.redirect('/post/'+ id)
        else:
            self.response.set_status(404, message="not permitted")
            self.render('404_error.html')
