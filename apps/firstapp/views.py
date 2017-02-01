from django.shortcuts import render, redirect
from django.contrib import messages

import bcrypt
import re
from .models import *

def index(request):
    print "hit index"
    if 'name' in request.session:
        return redirect ('/quotes')
    return render (request, 'firstapp/index.html')


def register(request):
    if request.method == "POST":
        errors = False
        emailvalid = re.search(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$', request.POST['email'])
        if len(request.POST['name']) < 2:
            messages.error(request, "your name must be more than 1 character long")
            errors = True
        if len(request.POST['alias']) < 3:
            messages.error(request, "please pick an alias that is longer than 2 characters")
            errors = True
        if emailvalid == None:
            messages.error(request, "that appears to be an invalid email")
            errors = True
        if len(request.POST['password']) < 8:
            messages.error(request, "your password must be at least 8 characters long")
            errors = True
        if request.POST['password'] != request.POST['password2']:
            messages.error(request, "those passwords do not match")
            errors = True
        if errors == True:
            return redirect('/')

        if errors == False:
            hashpw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        try:
            User.objects.create(name=request.POST['name'], alias=request.POST['alias'], email=request.POST['email'], password=hashpw)
        except:
            messages.error(request, "that email address is already registered, please try logging in instead")

        user = User.objects.get(email=request.POST['email'])
        request.session['id']=user.id
        request.session['name'] = request.POST['alias']
        print "request session id value is ", request.session['id']

    return redirect('/quotes')


def login(request):
    if request.method == "POST":
        user = User.objects.filter(email=request.POST['email'])
        if user.count() == 0:
            messages.error(request, 'email not in database, please register')
            return redirect ('/')
        for info in user:
            if bcrypt.checkpw(request.POST["password"].encode(), info.password.encode()):
                request.session['name'] = info.name
                request.session['id'] = info.id
                return redirect('/quotes')
            else:
                messages.error(request, 'your password is incorrect, please try again')
    return redirect ('/')


def quotes(request):

    favequotes = Favorite.objects.filter(user=request.session['id'])

    allquotes = Quote.objects.all()
    for a in allquotes:
        print "a.text", a.text
        print "a.favorite_quote", a.favorite_quote

    context = {
        'allquotes': allquotes,
        'favequotes': favequotes
    }
    return render (request, 'firstapp/quotes.html', context)


def addquote(request):
    if request.method == "POST":
        errors = False
        if len(request.POST['author']) < 3:
            messages.error(request, 'author name must be at least 3 characters long')
            errors = True
        if len(request.POST['quote']) < 10:
            messages.error(request, 'quote must be at least 10 characters long')
            errors = True
        if errors == True:
            return redirect('/quotes')
        if errors == False:
            Quote.objects.create(text=request.POST['quote'], author=request.POST['author'], user_id=request.session['id'])

    return redirect('/quotes')

def addfave(request, id):
    quote = Quote.objects.get(id=id)
    print "quote id value = ", quote.id
    print "current sessions user id = ", request.session['id']
    try:
        Favorite.objects.create(user_id=request.session['id'], quote_id=quote.id)
    except:
        messages.error(request, "that quote is already in your favorites!")
        return redirect ('/quotes')

    return redirect('/quotes')


def deletefave(request, id):
    Favorite.objects.filter(id=id).delete()
    return redirect('/quotes')


def showuser(request, id):
    user = User.objects.filter(id=id)
    posts = Quote.objects.filter(user=id)
    postcount = Quote.objects.filter(user=id).count()
    context = {'user': user, 'posts':posts, 'postcount': postcount}

    return render (request, 'firstapp/showuser.html', context)








def logout(request):
    request.session.clear()
    return redirect('/')
