import webapp2
import jinja2
import os

from google.appengine.api import users
from google.appengine.ext import ndb

the_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

# class CssiUser(ndb.Model):
#   first_name = ndb.StringProperty()
#   last_name = ndb.StringProperty()
#   email = ndb.StringProperty()
class Student_Profile(ndb.Model):
    first_name=ndb.StringProperty(required = True)
    last_name=ndb.StringProperty(required = True)
    phone_num=ndb.StringProperty(required = True)
    skills_needed=ndb.StringProperty(required = True)
    teachable_skills=ndb.StringProperty(required = True)
    email=ndb.StringProperty(required = True)
    college=ndb.StringProperty(required = True)
    pic=ndb.BlobProperty(required=False)


class MainHandler(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    # If the user is logged in...
    if user:
      signout_link_html = '<a href="%s">sign out</a>' % (
          users.create_logout_url('/login'))
      email_address = user.nickname()
      cc_user = Student_Profile.query().filter(Student_Profile.email == email_address).get()
      # If the user is registered...
      if cc_user:
        # Greet them with their personal information
        self.response.write('''
            Welcome %s %s (%s)! <br> %s <br>''' % (
              cc_user.first_name,
              cc_user.last_name,
              email_address,
              signout_link_html))
      # If the user isn't registered...
      else:
        # Offer a registration form for a first-time visitor:
        signup_template = the_jinja_env.get_template('templates/sign_up.html')
        # self.response.write(signup_template)
        self.response.write(signup_template.render())
    else:
      # If the user isn't logged in...
      login_url = users.create_login_url('/home')
      login_html_element = '<a href="%s">Sign in</a>' % login_url
      # Prompt the user to sign in.
      self.response.write('Please log in.<br>' + login_html_element)

  def post(self):
    # Code to handle a first-time registration from the form:
    user = users.get_current_user()
    cc_user = Student_Profile(
        first_name=self.request.get('first_name'),
        last_name=self.request.get('last_name'),
        phone_num=self.request.get('phone_num'),
        college=self.request.get('college'),
        skills_needed=(self.request.get_all('skills_needed')),
        teachable_skills=self.request.get('teachable_skills'),
        pic=self.request.Post.get('pic'),
        email=user.nickname()),
    cc_user.put()
    self.response.write('Thanks for signing up, %s! <br><a href="/">Home</a>' %
        cp_user.first_name)
