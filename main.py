import webapp2
import jinja2
import os


from login import MainHandler
from login import CssiUser


the_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class WelcomePage(webapp2.RequestHandler):
    def get(self): #for a get request
        welcome_template = the_jinja_env.get_template('templates/welcome.html')
        self.response.write(welcome_template.render())
class SignupPage(webapp2.RequestHandler):
    def get(self): #for a get request
        aboutme_template = the_jinja_env.get_template('templates/sign_up.html')
        self.response.write(sign_up_template.render())
class ProfilePage(webapp2.RequestHandler):
    def get(self): #for a get request
        profile_template = the_jinja_env.get_template('templates/profile.html')
        self.response.write(profile_template.render())
class MatchPage(webapp2.RequestHandler):
    def get(self): #for a get request
        match_template = the_jinja_env.get_template('templates/match.html')
        self.response.write(match_template.render())
class HomePage(webapp2.RequestHandler):
    def post(self): #for a get request
        home_template = the_jinja_env.get_template('templates/home.html')
        self.response.write(home_template.render())

app = webapp2.WSGIApplication([
    ('/', WelcomePage), #this maps the root url to the Main Page Handler
    ('/signup', SignupPage),
    ('/profile', ProfilePage),
    ('/match', MatchPage),
    ('/Home', HomePage),
    ('/login', MainHandler)

], debug=True)
