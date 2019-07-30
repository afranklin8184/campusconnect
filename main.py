import webapp2
import jinja2
import os


from login import MainHandler
from login import CssiUser
from models import Student_Profile


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
    def post(self): #for a get request
        home_template = the_jinja_env.get_template('templates/home.html')
        # first_name=ndb.StringProperty(required = True)
        # last_name=ndb.StringProperty(required = True)
        # phone_num=ndb.StringProperty(required = True)
        # skills_needed=ndb.StringProperty(required = True)
        # teachable_skills=ndb.StringProperty(required = True)
        # email=ndb.StringProperty(required = True)
        # college=ndb.StringProperty(required = True)
        #
        # student=Student_Profile(first_name=first_name,last_name=last_name,phone_num=phone_num,skills_needed=skills_needed,teachable_skills=teachable_skills,email=email,college=college)
        student_profile={
            "first_name":self.request.get('first_name'),
            "last_name":self.request.get('last_name'),
            "phone_num":self.request.get('phone_num'),
            "skills_needed":self.request.get('skills_needed'),
            "college":self.request.get('college'),
            "teachable_skills":self.request.get('teachable_skills'),
            "email":self.request.get('email'),
        }
        print
        # student.put()
        self.response.write(home_template.render(student_profile))
class MatchPage(webapp2.RequestHandler):
    def get(self): #for a get request
        match_template = the_jinja_env.get_template('templates/match.html')
        self.response.write(match_template.render())
class HomePage(webapp2.RequestHandler):
    def get(self): #for a get request
        home_template = the_jinja_env.get_template('templates/home.html')
        self.response.write(home_template.render())
    def post(self): #for a get request
        home_template = the_jinja_env.get_template('templates/home.html')
        student=Student_Profile(
            first_name=self.request.get('first_name'),
            last_name=self.request.get('last_name'),
            phone_num=self.request.get('phone_num'),
            skills_needed=self.request.get('skills_needed'),
            teachable_skills=self.request.get('teachable_skills'),
            email=self.request.get('email'),
            college=self.request.get('college'),
            id=self.request.get('id'),
            # pic=self.request.get('pic'))
            pic=None)
        student_key= student.put()
        id = student_key.id()

        student_profile={
            "first_name":self.request.get('first_name'),
            "last_name":self.request.get('last_name'),
            "phone_num":self.request.get('phone_num'),
            "skills_needed":self.request.get('skills_needed'),
            "college":self.request.get('college'),
            "teachable_skills":self.request.get('teachable_skills'),
            "email":self.request.get('email'),
            "pic":self.request.get('pic')
        }
        self.response.write(home_template.render(student_profile))


app = webapp2.WSGIApplication([
    ('/', WelcomePage), #this maps the root url to the Main Page Handler
    ('/signup', SignupPage),
    ('/profile', ProfilePage),
    ('/match', MatchPage),
    ('/Home', HomePage),
    ('/login', MainHandler)

], debug=True)
