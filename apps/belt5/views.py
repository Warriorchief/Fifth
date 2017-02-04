from django.shortcuts import render, redirect
from .models import User, Poke
import bcrypt
from datetime import date
import datetime
import re
from django.contrib import messages
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def index(request):
    # User.objects.all().delete()
    # Poke.objects.all().delete()
    signedup = User.objects.all()
    for s in signedup:
        print s.id
        print s.name
    print date.today()
    return render(request, "belt5/index.html")

def register(request):
    if request.method != 'POST':
        print("You have gotten to this page by invalid means!")
        return redirect('/')
    wrong = False
    name = request.POST['name'].lower()
    alias = request.POST['alias']
    email = request.POST['email']
    password = request.POST['password'].encode()
    date_of_birth = request.POST['date_of_birth']
    confirm_password = request.POST['confirm_password'].encode()
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    if len(name) <3 :
        wrong = True
        messages.warning(request, "Name must be at least 3 characters!")
        if len(name)>3 and not name.isalpha():
            wrong = True
            messages.warning(request, "Name must consist of letters ONLY!")
    if not EMAIL_REGEX.match(email):
        wrong = True
        messages.warning(request, "Email must be in valid form!")
    # if date_of_birth > date.today():
    #     wrong = True
    #     messages.warning(request, "Invalid date of birth!")
    if len(password) < 8:
        wrong = True
        messages.warning(request, "Password must be at least 8 characters!")
    if password != confirm_password:
        wrong = True
        messages.warning(request, "Your passwords must match!")
    if wrong:
        return redirect('/')
    else:
        messages.success(request, "Registration successful! ")
        User.objects.create(name = name, alias=alias, email=email, password= hashed)
        thisperson_list = User.objects.filter(email=email, name=name)
        request.session['user_name']=name
        request.session['user_alias'] = alias
        request.session['user_id'] = thisperson_list[0].id
        request.session['user_email'] = thisperson_list[0].email
        return redirect('/success')

def login(request):
    email = request.POST['email']
    password = request.POST['password']
    email_list = User.objects.filter(email=email)
    if email_list:
        hashed = email_list[0].password
        if bcrypt.hashpw(password.encode(), hashed.encode()) == hashed.encode():
            request.session['user_id'] = email_list[0].id
            request.session['user_name'] = email_list[0].name
            request.session['user_alias'] = email_list[0].alias
            request.session['user_email'] = email_list[0].email
            return redirect('/success')
        else:
            messages.warning(request, "Password does not match email!")
            return redirect('/')
    else:
        messages.warning(request, "Email not recognized!")
        return redirect('/')

def success(request):
    me = User.objects.get(id = request.session['user_id'])
    pokes_to_me = Poke.objects.filter(to = me)
    # for a in pokes_to_me:
    #     print a.id, "was the poke from", a.by.name, "to", a.to.name
    # print "there were this number of pokes to me total:", len(pokes_to_me)

    vals = pokes_to_me.values_list('by').distinct()
    who_poked_me = User.objects.filter(id__in= vals)
    # print "who poked me:", who_poked_me
    # for w in who_poked_me:
    #     print w.id, w.name
    x = len(who_poked_me)
    poked_me_ids = who_poked_me.values_list('id')

    counts=[]

    for w in who_poked_me:
        number_pokes = len(Poke.objects.filter(to=me, by=w))
        # print w.name, "seems to have poked me", number_pokes, "times"
        counts.append(number_pokes)
    # print "counts is:", counts

    thing=[]
    i = 0
    while i< len(counts):
        thing.append([who_poked_me[i],counts[i]])
        i+=1
    print "thing is",thing

    thing.sort(key=lambda elem: elem[1], reverse=True)  #HELL YES BITCH !!!!
    # for elem in thing:
    #     whack = thing.sort(key = lambda x: x[1])
    print "thing is", thing

    # for t in thing:
    #     print t[0].name
    #     print t[1]

    others = User.objects.exclude(id__in = poked_me_ids).exclude(id = me.id)
    otherthing=[]
    othercounts=[]
    for h in others:
        num_pokes = len(Poke.objects.filter(to=h, by=me))
        # print "I seem to have poked",h.name, num_pokes, "times"
        othercounts.append(num_pokes)
    # print "othercounts is:", counts
    j=0
    while j<len(others):
        otherthing.append([others[j],othercounts[j]])
        j+=1
    # print "otherthing is:", otherthing

    context = {
        "x": x,
        "thing": thing,
        "otherthing": otherthing,
        }
    return render (request, "belt5/pokes.html", context)

def addpoke(request,poked_id):
    me = User.objects.get(id = request.session['user_id'])
    person_poked = User.objects.get(id = poked_id)
    # print "it seems that",me.name,"just poked",person_poked.name
    Poke.objects.create(by = me, to = person_poked)
    return redirect('/success')


def logout(request):
    del request.session['user_id']
    return redirect('/')
