from google.appengine.ext import ndb

class Student_Profile(ndb.Model):
    first_name=ndb.StringProperty(required = True)
    last_name=ndb.StringProperty(required = True)
    phone_num=ndb.StringProperty(required = True)
    skills_needed=ndb.StringProperty(repeated = True)
    teachable_skills=ndb.StringProperty(repeated = True)
    email=ndb.StringProperty(required = True)
    college=ndb.StringProperty(required = True)
    pic=ndb.BlobProperty(required=False)
