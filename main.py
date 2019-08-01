import webapp2
import jinja2
import os

from google.appengine.api import users
from google.appengine.ext import ndb
import login
from models import Student_Profile


the_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class WelcomePage(webapp2.RequestHandler):
    def get(self): #for a get request
        template_data = login.get_user_login_data()
        welcome_template = the_jinja_env.get_template('templates/welcome.html')
        self.response.write(welcome_template.render(template_data))


class ProfilePage(webapp2.RequestHandler):
    def get(self): #for a get request
        profile_template = the_jinja_env.get_template('templates/profile.html')
        student_key=ndb.Key(urlsafe=self.request.get('id'))
        student=users.get_current_user()
        # email_address = student.nickname()+"@gmail.com"
        email_address = student.nickname()
        # print(email_address)
        student_profile = Student_Profile.query().filter(Student_Profile.email == email_address).get()
        print(student_profile)
        match_url="/match?id="+student_key.urlsafe()
        matches=[]
        if student_profile == None:
            print("no matches")
            self.redirect("/signup")
        else:
            cans = Student_Profile.query().filter(Student_Profile.college == student_profile.college).fetch()
            for can in cans:
                if set(student_profile.skills_needed) & set(can.teachable_skills):
                    matches.append(can)
            # ts=student_profile.teachable_skills
            # t=ts.split(',')

            student_profile={
                "first_name":student_profile.first_name,
                "last_name":student_profile.last_name,
                "phone_num":student_profile.phone_num,
                "skills_needed":student_profile.skills_needed,
                "college":student_profile.college,
                "teachable_skills":student_profile.teachable_skills,
                "email":email_address,
                "pic":student_profile.pic,
                "matches":matches,
                "match_url":match_url
            }
            self.response.write(profile_template.render(student_profile))
    def post(self): #for a get request
        print('Adding a user from the ProfilePage handler.')
        profile_template = the_jinja_env.get_template('templates/profile.html')
        student=users.get_current_user()
        email_address = student.nickname()

        student=Student_Profile(
            first_name=self.request.get('first_name'),
            last_name=self.request.get('last_name'),
            phone_num=self.request.get('phone_num'),
            skills_needed=self.request.get_all('skills_needed'),
            teachable_skills=self.request.get_all('teachable_skills'),
            email=email_address,
            college=self.request.get('college'),
            pic=None)
        student_key= student.put()
        print('Added student {}'.format(student_key))
        self.redirect('/profile')

class MatchPage(webapp2.RequestHandler):
    def get(self): #for a get request
        match_template = the_jinja_env.get_template('templates/match.html')
        student_key=ndb.Key(urlsafe=self.request.get('id'))
        student=users.get_current_user()
        email_address = student.nickname()
        student_profile = Student_Profile.query().filter(Student_Profile.email == email_address).get()
        # print(student_profile)
        matches=[]
        if student_profile == None:
            print("no matches")
            self.redirect("/signup")
        else:
            cans = Student_Profile.query().filter(Student_Profile.college == student_profile.college).fetch()
            for can in cans:
                if set(student_profile.skills_needed) & set(can.teachable_skills):
                    matches.append(can)
        print("hello world")
        for match in matches:
            print(can)


        self.response.write(match_template.render())

class HomePage(webapp2.RequestHandler):
    def get(self): #for a get request
        home_template = the_jinja_env.get_template('templates/home.html')

        student=users.get_current_user()
        email_address = student.nickname()+"@gmail.com"
        # print(email_address)
        student_profile = Student_Profile.query().filter(Student_Profile.email == email_address).get()
        print(student_profile)
        matches=[]
        if student_profile== None:
            print("no matches")
            self.redirect("/login")
        else:
            cans = Student_Profile.query().filter(Student_Profile.college == student_profile.college).fetch()
            for can in cans:
                if set(student_profile.skills_needed.split(",")) & set(can.teachable_skills.split(",")):
                    matches.append(can)
            student_profile={
                "first_name":student_profile.first_name,
                "last_name":student_profile.last_name,
                "phone_num":student_profile.phone_num,
                "skills_needed":student_profile.skills_needed,
                "college":student_profile.college,
                "teachable_skills":student_profile.teachable_skills,
                "email":email_address,
                "pic":student_profile.pic,
                "matches":matches
            }
            self.response.write(home_template.render(student_profile))
    def post(self): #for a get request
        home_template = the_jinja_env.get_template('templates/home.html')
        student=Student_Profile(
            first_name=self.request.get('first_name'),
            last_name=self.request.get('last_name'),
            phone_num=self.request.get('phone_num'),
            skills_needed=self.request.get_all('skills_needed'),
            teachable_skills=self.request.get_all('teachable_skills'),
            email=self.request.get('email'),
            college=self.request.get('college'),
            # id=self.request.get('id'),
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
        # print(student_profile.skills_needed())
        self.response.write(home_template.render(student_profile))


app = webapp2.WSGIApplication([
    ('/', WelcomePage), #this maps the root url to the Main Page Handler
    ('/profile', ProfilePage),
    ('/match', MatchPage),
    # ('/home', HomePage),
    ('/signup', login.SignUpPage),

], debug=True)
