#!/usr/bin/env python

import cgi
import os
from google.appengine.api import users
from google.appengine.ext import db

import webapp2
import jinja2


jinja_enviroment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__name__)))


from adGrabber.cacoa_grabber import CacoaGrabber
from adGrabber.property_grabber import PropertyGrabber



class Amount(db.Model):
    sitename = db.StringProperty()
    size = db.IntegerProperty()


class MainHandler(webapp2.RequestHandler):

    def get(self):
        template_values = {}
        template = jinja_enviroment.get_template('templates/page/index.html')
        self.response.out.write(template.render(template_values))

class CacoaHandler(webapp2.RequestHandler):

    def get(self):
            # It 's happens only if user come from outside
        html = ''

        mls = ''
        another_page_name = 'propertyinsantacruz.com'
        title = 'cacoastalhome.com'
        template_values = {
            'another_page_name': another_page_name,
            'title': title,

            'mls': mls,
            'amount': 100000,
            'html': html,
            }
        template = jinja_enviroment.get_template('templates/page/work_cacoa.html')
        self.response.out.write(template.render(template_values))



    def post(self):
        html = ''
        go = cgi.escape(self.request.get('go'))
        # If it was the first time
        if go:
            html = ''

        new_amount = cgi.escape(self.request.get('amount'))
        if not new_amount:
            new_amount = 100000

        #template = cgi.escape(self.request.get('templates')).rstrip().strip()

        mls = cgi.escape(self.request.get('mls')).rstrip().strip()
        if mls:
            mls = mls.encode('utf-8')
            html = CacoaGrabber(mls, new_amount)


        another_page_name = 'propertyinsantacruz.com'
        title = 'cacoastalhome.com'
        template_values = {
            'another_page_name': another_page_name,
            'title': title,

            'mls': mls,
            'amount': new_amount,
            'html': html,
        }
        template = jinja_enviroment.get_template('templates/page/work_cacoa.html')
        self.response.out.write(template.render(template_values))



class PropertyHandler(webapp2.RequestHandler):

    def get(self):
    # It 's happens only if user come from outside
        html = ''

        mls = ''

        another_page_name = 'cacoastalhome.com'
        title = 'propertyinsantacruz.com'
        template_values = {
            'another_page_name': another_page_name,
            'title': title,

            'mls': mls,

            'amount': 100000,

            'html': html,
            }
        template = jinja_enviroment.get_template('templates/page/work_property.html')
        self.response.out.write(template.render(template_values))


    def post(self):
        html = ''
        go = cgi.escape(self.request.get('go'))
        # If it was the first time
        if go:
            html = ''


        #template = cgi.escape(self.request.get('templates')).rstrip().strip()

        new_amount = cgi.escape(self.request.get('amount'))
        if not new_amount:
            new_amount = 100000


        mls = cgi.escape(self.request.get('mls')).rstrip().strip()
        if mls:
            mls = mls.encode('utf-8')
            html = PropertyGrabber(mls, new_amount)


        another_page_name = 'cacoastalhome.com'
        title = 'propertyinsantacruz.com'
        template_values = {
            'another_page_name': another_page_name,
            'title': title,
            'mls': mls,
            'amount': new_amount,
            'html': html,

            }
        template = jinja_enviroment.get_template('templates/page/work_property.html')
        self.response.out.write(template.render(template_values))



class PiscImageHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'image/jpeg'
        self.response.out.write("""<img src = '/static/images/PISC.jpg' />""")


app = webapp2.WSGIApplication(
    [('/', MainHandler),
    ('/cacoa', CacoaHandler),
    ('/property', PropertyHandler),
    ('/images/PISC.jpg', PiscImageHandler),], debug=True)



# # Parse the HTML
# tree = etree.HTML(url.content)
#
# # Converts the DOM into a string
# result = etree.tostring(tree, pretty_print=True, method='html')
