import webapp2
import jinja2
import os


from google.appengine.ext import ndb

class Student_Profile(ndb.Model):
    first_name=ndb.StringProperty(required = True)
    last_name=ndb.StringProperty(required = True)
    phone_num=ndb.StringProperty(required = True)
    skills_needed=ndb.StringProperty(required = True)
    teachable_skills=ndb.StringProperty(required = True)
    email=ndb.StringProperty(required = True)
    college=ndb.StringProperty(required = True)
    pic=ndb.BlobProperty(required=False)
    # def post(self):
    #     home_template = the_jinja_env.get_template('templates/home.html')
