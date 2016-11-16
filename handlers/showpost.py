from handler import Handler
import models




class ShowPost(Handler):
    def get(self, id):
        post = models.BlogPost.by_id(int(id))
        subject = post.subject
        content = post.content
        created = post.created
        author_id = post.author_id
        cookie_id = self.read_secure_cookie("id")

        if cookie_id:
            user_id = int(cookie_id)
            logged_in = True
            liked_by_current_user =  models.Like.all() \
                .filter("blog_id =", int(id)) \
                .filter("user_id =", int(cookie_id)).get()
        else:
            liked_by_current_user = False
            logged_in = False
            user_id = None

        if author_id == str(cookie_id):
            belongs_to_current_user = True
        else:
            belongs_to_current_user = False



        number_of_likes = models.Like.all().filter("blog_id =", int(id)).count()

        comments = models.Comment.all().filter("blog_id =", int(id)).order("-created")
        print("this is the comments", comments)

        self.render("post.html",
                    subject=subject,
                    content=content,
                    created=created,
                    id = id,
                    belongs_to_current_user = belongs_to_current_user,
                    liked_by_current_user = liked_by_current_user,
                    number_of_likes = number_of_likes,
                    comments = comments,
                    logged_in = logged_in,
                    user_id = user_id
                    )
