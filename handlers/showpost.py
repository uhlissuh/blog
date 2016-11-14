from handler import Handler
import models



class ShowPost(Handler):
    def get(self, id):
        post = models.BlogPost.by_id(int(id))
        subject = post.subject
        content = post.content
        created = post.created
        author_id = post.author_id
        belongs_to_current_user = False
        cookie_id = self.read_secure_cookie("id")

        liked_by_current_user =  models.Like.all() \
            .filter("blog_id =", int(id)) \
            .filter("user_id =", int(cookie_id)).get()

        if author_id == str(cookie_id):
            belongs_to_current_user = True


        self.render("post.html",
                    subject=subject,
                    content=content,
                    created=created,
                    id = id,
                    belongs_to_current_user = belongs_to_current_user,
                    liked_by_current_user = liked_by_current_user)

    def post(self, id):
        blog = models.BlogPost.by_id(int(id))
        blog_user_id = str(blog.author_id)
        cookie_id = str(self.read_secure_cookie("id"))
        if blog_user_id == cookie_id:
            models.BlogPost.by_id(int(id)).delete()
            self.redirect('/')
        else:
            self.response.set_status(404, message="not permitted")
