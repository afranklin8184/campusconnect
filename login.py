import webapp2
import jinja2
import os

from google.appengine.api import users
from google.appengine.ext import ndb

the_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class CssiUser(ndb.Model):
  first_name = ndb.StringProperty()
  last_name = ndb.StringProperty()
  email = ndb.StringProperty()

class MainHandler(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    # If the user is logged in...
    if user:
      signout_link_html = '<a href="%s">sign out</a>' % (
          users.create_logout_url('/login'))
      email_address = user.nickname()
      cssi_user = CssiUser.query().filter(CssiUser.email == email_address).get()
      # If the user is registered...
      if cssi_user:
        # Greet them with their personal information
        self.response.write('''
            Welcome %s %s (%s)! <br> %s <br>''' % (
              cssi_user.first_name,
              cssi_user.last_name,
              email_address,
              signout_link_html))
      # If the user isn't registered...
      else:
        # Offer a registration form for a first-time visitor:
        signup_template = the_jinja_env.get_template('templates/sign_up.html')
        self.response.write(signup_template)

            # # Welcome to Campus Connect, %s!  Please sign up! <br>
            # # <form method="post" action="/Home">
            # # <input type="text" name="first_name" value="First Name">
            # # <input type="text" name="last_name" value="Last Name">
            # # <input type="text" name="phone_num" value="Phone Number">
            # # <input type="checkbox" name="skills_needed" value="Cosmetology"
            # #     <select name="college"
            # #         <option value="">College/University</option>
            # #         <option value="mit">MIT</option>
            # #         <option value="auburn">Auburn University</option>
            # #         <option value="harvard">Harvard</option>
            # #         <option value="ud">University of Delware</option>
            # #         <option value="stanford">Stanford</option>
            # #     </select>
            # #     <select class="select" multiple name="skills_needed">
            # #         <option value="">Skills Needed</option>
            # #         <option value="cosmo">Cosmetology</option>
            # #         <option value="cooking">Cooking</option>
            # #         <option value="tutoring">Tutoring</option>
            # #         <option value="selfD">Self Defense</option>
            # #     </select>
            # #     <select class="select" multiple="" name="Teachable Skills">
            # #         <option value="">Teachable Skills</option>
            # #         <option value="cosmo">Cosmetology</option>
            # #         <option value="cooking">Cooking</option>
            # #         <option value="tutoring">Tutoring</option>
            # #         <option value="selfD">Self Defense</option>
            # #     </select>
            # # <input encode="multipart/form-data" accept="image/png, image/jpeg" type="file" multiple="false" name="pic">
            # # <input type="submit">
            # </form><br> %s <br>
            # ''' % (email_address, signout_link_html))
    else:
      # If the user isn't logged in...
      login_url = users.create_login_url('/home')
      login_html_element = '<a href="%s">Sign in</a>' % login_url
      # Prompt the user to sign in.
      self.response.write('Please log in.<br>' + login_html_element)

  def post(self):
    # Code to handle a first-time registration from the form:
    user = users.get_current_user()
    student_profile = CssiUser(
        first_name=self.request.get('first_name'),
        last_name=self.request.get('last_name'),
        phone_num=self.request.get('phone_num'),
        college=self.request.get('college'),
        skills_needed=self.request.get('skills_needed'),
        teachable_skills=self.request.get('teachable_skills'),
        pic=self.request.Post.get('pic'),
        email=user.nickname()),
    cssi_user.put()
    self.response.write('Thanks for signing up, %s! <br><a href="/">Home</a>' %
        cssi_user.first_name)
