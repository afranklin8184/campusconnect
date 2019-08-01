import webapp2
import jinja2
import os

from google.appengine.api import users
from google.appengine.ext import ndb

from models import Student_Profile

the_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def get_user_login_data():
    user = users.get_current_user()
    if user:
        print("{} logged in!".format(user.nickname()))
        return {
            "login_link": users.create_logout_url('/'),
            "users_url": "Logout",
        }
    else:
        print("User is not logged in")
        return {
            "login_link": users.create_login_url('/signup'),
            "users_url": "Login",
        }

class SignUpPage(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    # If the user is logged in...
    if user:
      email_address = user.nickname()
      student_profile = Student_Profile.query().filter(Student_Profile.email == email_address).get()
      # If the user is registered...
      if student_profile:
        # Greet them with their personal information
        self.redirect('/profile')
        # self.response.write('''
        #     Welcome %s %s (%s)! <br> %s <br>''' % (
        #       student_profile.first_name,
        #       student_profile.last_name,
        #       email_address,
        #       signout_link_html))
      # If the user isn't registered...
      else:
        # Offer a registration form for a first-time visitor:
        signup_template = the_jinja_env.get_template('templates/sign_up.html')
        # self.response.write(signup_template)
        self.response.write(signup_template.render())
    else:
      # If the user isn't logged in...
      self.redirect('/')
      return

  def post(self):
    # Code to handle a first-time registration from the form:
    print('Creating a profile from login.SignUpPage.')
    user = users.get_current_user()
    if not user:
        # Make sure we actually have a user object to get an email address.
        self.redirect('/')
    student_profile = Student_Profile(
        first_name=self.request.get('first_name'),
        last_name=self.request.get('last_name'),
        phone_num=self.request.get('phone_num'),
        college=self.request.get('college'),
        skills_needed=self.request.get_all('skills_needed'),
        teachable_skills=self.request.get_all('teachable_skills'),
        # pic=self.request.Post.get('pic'),
        email=user.nickname())
    student_key = student_profile.put()
    student_record = student_key.get()
    print('Added user {}'.format(student_record))
    self.redirect('/profile')
    #
    # self.response.write('Thanks for signing up, %s! <br><a href="/">Home</a>' %
    #     cp_user.first_name)
