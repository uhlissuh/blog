import jinja2
import security
import webapp2
import os


template_dir = os.path.join(os.path.dirname(__file__), '../templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

#main handler that others inherit from
class Handler(webapp2.RequestHandler):
    def render(self, template, **kw):
        t = jinja_env.get_template(template)
        self.response.out.write(t.render(**kw))

    def set_secure_cookie(self, name, val):
        cookie_id = security.make_secure_val(val)
        self.response.headers.add_header('Set-Cookie','%s=%s; Path=/' % (name, cookie_id))

    def read_secure_cookie(self, name):
        cookie_id = self.request.cookies.get(name)
        return cookie_id and security.check_secure_val(cookie_id)

    def logout(self):
        self.response.headers.add_header('Set-Cookie','id=; Path=/')
