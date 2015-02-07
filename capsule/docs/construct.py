from capsule.models import *
from capsule.control import *
from capsule.query import *
from capsule.tests import populate_dbms

# -------------------
#  Flushing Database
# -------------------
for d in Datasheet.objects.all():
    d.delete()

for t in Tag.objects.all():
    t.delete()

# ----------------
#  Inserting data
# ----------------
# Getting the user: 'mitthu'
user = User.objects.get(username='aditya')
DatasheetControl.add(user=user, url="http://www.w3schools.com/tags/ref_colorpicker.asp", kind='S', title="Colour Picker", colour='Red', tags=['scraps', 'web'])
DatasheetControl.add(user=user, url="https://docs.djangoproject.com/en/1.3/topics/db/models/", kind='H', title="Day", content="Day and night we were out for jobs.", tags=['scraps', 'blogs'])
DatasheetControl.add(user=user, url="https://docs.djangoproject.com/en/1.3/topics/db/models/", kind='H', title="Student", content="Students need to study and work hard.")
DatasheetControl.add(user=user, url="http://www.w3schools.com/css/default.asp", kind='H', title="CSS", description="CSS", content="At W3Schools you will find complete CSS references of all properties and selectors with syntax, examples, browser support, and more.", tags=['css', 'w3c'])

# By moody
DatasheetControl.add(user=user, url="http://en.wikipedia.org/wiki/Maria_Terwiel", kind='H', title="MariaJi-1", description="Maria is beautiful", content="After her arrest on 17 September 1942, Maria Terwiel was sentenced to death on 26 January 1943 by the Reichskriegsgericht (\"Reich Military Tribunal\"). She was put to death at Plötzensee Prison in Berlin.", tags=['maria', 'yo maria yo'])

DatasheetControl.add(user=user, url="http://www.w3schools.com/css/default.asp", kind='H', title="CSS-hurray", description="2nd CSS", content="Learn from over 150 examples! With our editor, you can edit the CSS, and click on a button to view the result.", tags=['css', 'w3c'])
DatasheetControl.add(user=user, url="http://www.w3schools.com/css/default.asp", kind='H', title="CSS yipee", description="3rd CSS", content="This CSS tutorial contains hundreds of CSS examples.", tags=['css', 'w3c'])
DatasheetControl.add(user=user, url="http://en.wikipedia.org/wiki/Maria_Terwiel", kind='H', title="MariaJi", description="Maria is my darling.", content="The devout Catholic, along with Helmut Himpel, helped Jews in hiding, to whom they furnished identification and ration cards. There arose contacts with the Red Orchestra group about Harro Schulze-Boysen. Terwiel wrote illegal handbills and put up posters against the Nazi propaganda exhibition Soviet Paradise.", tags=['Maria', 'Terwiel'])
DatasheetControl.add(user=user, url="http://en.wikipedia.org/wiki/Maria_Terwiel", kind='H', title="MariaJi-1", description="Maria is beautiful", content="After her arrest on 17 September 1942, Maria Terwiel was sentenced to death on 26 January 1943 by the Reichskriegsgericht (\"Reich Military Tribunal\"). She was put to death at Plötzensee Prison in Berlin.", tags=['maria', 'yo maria yo'])
DatasheetControl.add(user=user, url="http://en.wikipedia.org/wiki/Maria_Terwiel", kind='H', title="MariaJi-2", description="Maria is sexy.", content="Maria Terwiel (7 June 1910 in Boppard – 5 August 1943 in Berlin-Plötzensee, executed) was a German resistance fighter in the Third Reich. She belonged to the Red Orchestra resistance group.", tags=['maria'])
DatasheetControl.add(user=user, url="http://en.wikipedia.org/wiki/Maria_Terwiel", kind='S', title="Maria Terwiel", colour='Blue', tags=['Maria'])
DatasheetControl.add(user=user, url="http://www.gegen-diktatur.de/beispiel.php?beisp_id=448&tafel_id=9&thema=0", kind='S', title="Maria", colour='Red', tags=['darling', 'maria'])
DatasheetControl.add(user=user, url="http://www.gdw-berlin.de/index.php?id=191#", kind='S', title="Colour Picker", colour='Red', tags=['Maria', 'fighter'])

q = DatasheetQuery(user)
q.urlIs("http://www.w3schools.com/tags/ref_colorpicker.asp")
q.result()

# Testing toJSON serializer
Datasheet.objects.all()[1].serialize_to_json()

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
