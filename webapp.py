# -*- coding: utf-8 -*-

import wsgiref.handlers, cgi, os, time, zipfile
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import template

class Greeting(db.Model):
  author = db.UserProperty()
  content = db.StringProperty(multiline=True)
  date = db.DateTimeProperty(auto_now_add=True)

class MainPage(webapp.RequestHandler):
  def get(self):
    greetings_query = Greeting.all().order('-date')
    greetings = greetings_query.fetch(10)

    if users.get_current_user():
      url = users.create_logout_url(self.request.uri)
      url_linktext = 'Logout'
    else:
      url = users.create_login_url(self.request.uri)
      url_linktext = 'Login'

    template_values = {
      'greetings': greetings,
      'url': url,
      'url_linktext': url_linktext,
      }

    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, template_values))

class Search(webapp.RequestHandler):
  def post(self):
    word=self.request.get('word')
    exist=0
    type=['noun','verb','adj','adv']
    self.response.out.write('<table><td><a href="/">Back</a></td>')
    self.response.out.write('<td>&nbsp;&nbsp;&nbsp;</td><form action="/search" method="post">')
    self.response.out.write('<td><div><input type="text" name="word"></div></td>')
    self.response.out.write('<td><div><input type="submit" value="search"></div></td>')
    self.response.out.write('</form></table>')
    self.response.out.write('<hr>')
    d=[1,2,3,4,5,6]
    for num in d:
        f=zipfile.ZipFile('library%d.zip' % num,'r')
        files=f.namelist()
#        listFile=open('/static/list.txt','r')
#        files=[ a for a in listFile.readlines()]
        for name in files:
          for t in type:
            found=name.find(word+'_'+t+'.htm') 
            if found!=-1:
              exist+=1
              if exist>=2 and exist<=4:
                self.response.out.write('<hr>')
              wordinfo=f.read(name)
              self.response.out.write(template.render('result.html',{'wordinfo':wordinfo}))
    if exist==0:
      self.response.out.write('<h3>Sorry, no such Word!<h3>')
	#self.response.out.write('<img src="http://code.google.com/appengine/images/appengine-silver-120x30.gif" alt="Google App Engine 支持" />')
    self.response.out.write('<hr>')
    self.response.out.write('<a style="font-weight:normal;font-size:16;" href="/">Back</a>')
	#self.response.out.write('<img></img>')
	#self.response.out.write('<img src="http://code.google.com/appengine/images/appengine-silver-120x30.gif" alt="Google App Engine 支持" />')
#    self.response.out.write('</body>')
#    self.response.out.write('</html>')

class Guestbook(webapp.RequestHandler):
  def post(self):
    greeting = Greeting()

    if users.get_current_user():
      greeting.author = users.get_current_user()

    greeting.content = self.request.get('content')
    greeting.put()
    self.redirect('/')

def main():
  application = webapp.WSGIApplication(
                                       [('/', MainPage),
                                        ('/sign', Guestbook),
                                        ('/search', Search)])
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
  main()
