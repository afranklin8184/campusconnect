from google.appengine.ext import ndb

class Student_Proffile(ndb.Model):
    email=ndb.StringProperty(required = True)
