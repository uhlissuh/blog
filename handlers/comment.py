from handler import Handler
import models

class Comment(Handler):
    def render_page(self, id, error =""):
        cookie_id = self.read_secure_cookie("id")
        post = models.BlogPost.by_id(int(id))
        subject = post.subject
        content = post.content
        created = post.created
        author_id = post.author_id
        belongs_to_current_user = False


        liked_by_current_user =  models.Like.all() \
            .filter("blog_id =", int(id)) \
            .filter("user_id =", int(author_id)).get()

        if author_id == str(cookie_id):
            belongs_to_current_user = True

        number_of_likes = models.Like.all().filter("blog_id =", int(id)).count()

        self.render("commentonpost.html",
                    subject=subject,
                    content=content,
                    created=created,
                    id = id,
                    belongs_to_current_user = belongs_to_current_user,
                    liked_by_current_user = liked_by_current_user,
                    number_of_likes = number_of_likes,
                    error = error
                    )


    def get(self, id):
        if self.read_secure_cookie("id"):
            self.render_page(id)

        else:
            self.response.set_status(404, message="not permitted")
            self.render('404_error.html')

    def post(self, id):
        cookie_id = self.read_secure_cookie("id")
        if cookie_id:
            content = self.request.get("content")
            if content:
                comment = models.Comment(commenter_id = int(cookie_id),
                                         blog_id = int(id),
                                         content = content
                                         )
                comment.put()
                print(comment)
                self.redirect('/post/'+ id)
            else:
                content_error = "your comment must have some content"
                self.render_page(id, error = content_error)
        else:
            self.response.set_status(404, message="not permitted")
            self.render('404_error.html')
