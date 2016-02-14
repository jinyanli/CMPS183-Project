# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.logo = A(B('Slug Hero'),XML('&trade;&nbsp;'),
                  _class="navbar-brand",_href="http://www.web2py.com/",
                  _id="web2py-logo")
response.title = request.application.replace('_',' ').title()
response.subtitle = ''

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Your Name <you@example.com>'
response.meta.description = 'a cool new app'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    (T('Home'), False, URL('default', 'index'), []),
    (T('Department'), False, URL('SlugHero', 'default', 'showDepartment')),
    (T('Professor'), False, URL('SlugHero', 'professor', 'showProfessor')),
    (T('Textbook Exchange'), False, URL('SlugHero', 'forum', 'bookExchange')),
    (T('Forum'), False, URL('SlugHero', 'forum', 'generalForum'))
]

if auth.user:
   response.menu+=[(T('my Profile'), False, URL('SlugHero', 'userProfile', 'showProfile',args=auth.user.id, vars=dict(fromMenu=True)))]

#DEVEOPMENT_MENU = True

#########################################################################
## provide shortcuts for development. remove in production
#########################################################################
"""
def _():
    # shortcuts
    app = request.application
    ctr = request.controller
    # useful links to internal and external resources
    response.menu += [

        ]
if DEVELOPMENT_MENU: _()

if "auth" in locals(): auth.wikimenu()
"""
