from handler import Handler
import models

#allows a user who isn't the blog author to like a blog post if they are signed in
class Like(Handler):
    def post(self, id):
        author_id = int(models.BlogPost.by_id(int(id)).author_id)
        user_id = int(self.read_secure_cookie("id"))
        blog_id = int(id)

        if user_id:
            if user_id != author_id:
                has_already_liked = models.Like.all().filter("blog_id =", blog_id).filter("user_id =", user_id).get()
                if not has_already_liked:
                    like = models.Like(user_id = user_id, blog_id = blog_id)
                    like.put()
                    self.redirect('/post/'+ id)
                else:
                    self.response.set_status(404, message="not permitted")
                    self.render('404_error.html')
            else:
                self.redirect('/post/'+ id)
        else:
            self.redirect('/login')
