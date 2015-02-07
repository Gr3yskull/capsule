from capsule.models import *

# -------------------
#  Flushing Database
# -------------------
for h in Highlight.objects.all():
    h.delete()

for u in URLReference.objects.all():
    u.delete()

# ----------------
#  Inserting data
# ----------------
# Getting the user: 'mitthu'
user = User.objects.filter(username__exact=u'mitthu')[0]

ref = URLReference(user=user, url="https://docs.djangoproject.com/en/1.3/topics/db/models/")
ref.save()
Highlight(url_ref=ref, title="Day", content="Day and night we were out for jobs.").save()
Highlight(url_ref=ref, title="Student", content="Students need to study and work hard.").save()

# Testing toJSON serializer
Highlight.objects.all()[1].toJSON()

# Tesing TagControl
from capsule.query import *
tc = TagContol(user)

tc.tagIncrement('News')
tc.tagDecrement('News')

# Insertion is static
# Colours inserted using colour whell from w3schools on 27-Mar-2013 (10:06 AM) -
# http://www.w3schools.com/tags/ref_colorpicker.asp
Colour(name="Red", hexcode="CC0000").save()
Colour(name="Gray", hexcode="C3C3C3").save()
Colour(name="Green", hexcode="33CC33").save()
Colour(name="Purple", hexcode="CC0099").save()
Colour(name="Yellow", hexcode="FFCC00").save()
Colour(name="Blue", hexcode="3366FF").save()

# Getting json serialized list of all colours
import json
c = json.dumps(list(Colour.objects.all().values()))

# Checking SighnupForm
signup = {
    "username": "aditya",
    "password": "abc",
    "email": "abc@gmail.com"
}

# Invalid username
signup = {
    "username": "adityabasuadityabasuadityabasuadityabasu",
    "password": "abc",
    "email": "abc@gmail.com"
}

# Invalid email
signup = {
    "username": "aditya",
    "password": "abc",
    "email": "abc@gmail"
}

signup = {
    "username": "aditya",
    "password": "abc",
    "email": ""
}

signup = {
    "username": "aditya",
    "password": "abc",
}

signup = {
    "username": "",
    "password": "abc",
}

# Checking SighnupForm
from authentication.forms import *

s = SignupForm(signup)
s.is_bound
s.is_valid()

# Checking Signup
from django.test.client import Client
import json
c = Client()
signup = {
    "username": "aditya",
    "password": "abc",
}
r = c.post('/api/user/signup/', data=json.dumps(signup), content_type='application/json', follow=True, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
r.content

# Checking login
from django.test.client import Client
c = Client()
r = c.post('/login/', {'username':'mitthu', 'password':'pass'})
r.status_code

# ModifyUserForm
from authentication.forms import *
dat = {'username':'mitthu', 'password':'pass'}
m = ModifyUserForm(dat)
