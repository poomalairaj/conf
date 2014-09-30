from __future__ import with_statement
from fabric.api import *
import os, sys

GH_PAGES_REPO = 'git@github.com:poomalairaj/poomalairaj.github.com.git'
BITBUCKET_REPO = 'git@bitbucket.org:poomalairaj/blog.git'
PELICAN_DIR = os.path.abspath(os.path.dirname('.'))
BLOG_DIR = os.path.dirname(PELICAN_DIR)
CONTENT_DIR = os.path.join(PELICAN_DIR, 'content')
OUTPUT_DIR = os.path.join(BLOG_DIR, 'output')
GH_PAGES_DIR = os.path.join(os.path.dirname(PELICAN_DIR), 'poomalairaj.github.com')
STATIC_DIR = os.path.join(PELICAN_DIR, 'static')
PELICAN_CONF = os.path.join(PELICAN_DIR, 'pelicanconf.py')
WEBFACTION_BLOG_DIR = '/home/poomalairaj/webapps/blog'

@task
def init():
	if not os.path.exists(OUTPUT_DIR):
		os.makedirs(OUTPUT_DIR)
	if not os.path.exists(GH_PAGES_DIR):
		local('cd %s && git clone %s' % (BLOG_DIR, GH_PAGES_REPO))

@task
def publish():
	genhtml()
	push()
	publish_github()

@task
def publish_github():
	local('cp -r %s/* %s && cd %s && git add --all && git commit' % (OUTPUT_DIR, GH_PAGES_DIR, GH_PAGES_DIR))
	local('cd %s && git push origin master' % GH_PAGES_DIR)

@task
def push():
	print "\nPushing content to bitbucket...\n"
	local('cd %s && git add --all && git commit' % BLOG_DIR)
	local('cd %s && git push origin master' % BLOG_DIR)

@task
def genhtml():
	print "\nGenerating HTML and Adding static content to output directory...\n"
	local('pelican %s -o %s -s %s' % (CONTENT_DIR, OUTPUT_DIR, PELICAN_CONF))
	local('cp -r %s %s' % (STATIC_DIR, OUTPUT_DIR))

@task
def serve():
	local('cd %s && python -m SimpleHTTPServer' % OUTPUT_DIR)

@task
def help():
	print """Dependencies: pelican, fabric, python-pip, python-markdown, ssh client config, ssh keypairs
	fab genhtml: Generates html from markdown content
	fab serve: serves html site on http://localhost:8000
	fab push: commits and pushes all content to bitbucket repo
	fab publish: generates html, commits and pushes to bitbucket, deploys to github
	fab publish_github: commits and pushes changes to github
	"""
