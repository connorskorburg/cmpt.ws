from django.shortcuts import render, redirect
import pymysql
from .models import *
import validators
from django.contrib import messages
import re
# Create your views here.

def validate_form(post_data):
  errors = {}
  
  valid_alias = re.compile(r'^[a-z0-9_\-]+$')
  if not valid_alias.match(post_data['alias']):
    errors['alias'] = "Please Enter a Valid Alias (a-z)(0-9)"
  
  valid_url = validators.url(post_data['url'])
  if not valid_url:
    errors['url'] = "Please Enter a Valid URL"

  mysql = connectToMySQL('compact_url')
  alias_query = 'SELECT * FROM short_url WHERE alias = %(alias)s;'
  alias_data = {
    "alias": post_data['alias']
  }
  available_alias = mysql.query_db(alias_query, alias_data)

  if len(available_alias) > 0:
    errors['available_alias'] = "Alias in use, Please try a different Alias"
  
  return errors
  



# render home page
def index(request):
  return render(request, "index.html")


# post route to create url 
def createURL(request):

  url = request.POST['url']
  alias = request.POST['alias']


  errors = validate_form(request.POST)
  if len(errors) > 0:
    for key, val in errors.items():
      messages.error(request, val)
    return redirect('/')
  else:
    mysql = connectToMySQL('compact_url')
    query = 'INSERT INTO short_url (long_url, alias) VALUES(%(long_url)s, %(alias)s);'
    data = {
      "long_url": url,
      "alias": alias
    }
    new_url_id = mysql.query_db(query, data)
    success = {}
    success['long_url'] = f'Long URL: {url}'
    success['alias'] = f'Alias: {alias}'
    success['short_url'] = f'Short URL: cmpt.ws/{alias}'
    if len(success) > 0:
      for key, val in success.items():
        messages.success(request, val)
      return redirect('/')

    
  return redirect('/')

def findURL(request, alias):
  mysql = connectToMySQL('compact_url')
  query = 'SELECT * FROM short_url WHERE alias = %(alias)s;'
  data = {
    "alias": alias
  }
  info = mysql.query_db(query, data)
  if len(info) > 0 and info[0]['long_url']:
    print(info[0]['long_url'])
    return redirect(info[0]['long_url'])
  else:
    return render(request, 'error.html')