from django.shortcuts import HttpResponse
from django.shortcuts import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from models import Users

# Create your views here.
#from models import Users
def index(request):
	#message = "hello1"
	message = '''<html>
                    <head>
                        <style>
                            body {
                                margin: 0;
                                padding: 0;
                            }

                            .container {
                                position: relative;
                                width: 100%;
                            }

                        </style>
                    </head>
                    <body>
                        <div class="container">
                            <form name="submit_form" id="submit_form" action="/career/showdata/" method="post">
                                <table border="1" style="width: 400px; margin-left: auto; margin-right: auto; margin-top: 30px;" cellpadding="8" cellspacin="8">
                                    <tr>
                                    	<td style="width: 30%; text-align: center;">
                                    		First Name
                                    	</td>
                                    	<td>
                                    		<input type="text" name="firstName" value="" placeholder="Please enter firstname." style="width: 100%; height: 30px;" />
                                    	</td>
                                    </tr>
                                    <tr>
                                        <td style="width: 30%; text-align: center;">
                                            Last Name
                                        </td>
                                        <td>
                                            <input type="text" name="lastName" value="" placeholder="Please enter lastname." style="width: 100%; height: 30px;" />
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="width: 30%; text-align: center;">
                                            Middle Name
                                        </td>
                                        <td>
                                            <input type="text" name="midName" value="" placeholder="Please enter middle name." style="width: 100%; height: 30px;" />
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="width: 30%; text-align: center;">
                                            Gender
                                        </td>
                                        <td>
                                            <input type="radio" name="gender" value="m" checked /> Male
                                            <br />
                                            <input type="radio" name="gender" value="f" /> Female
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="width: 30%; text-align: center;">
                                            Date of birth
                                        </td>
                                        <td>
                                            <input type="text" name="dateOfBirth" value="" placeholder="Please enter date of birth." style="width: 100%; height: 30px;" />
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="width: 30%; text-align: center;">
                                            &nbsp;
                                        </td>
                                        <td>
                                            <input type="button" value="Cancel" />
                                            <input type="submit" value="Submit" />
                                        </td>
                                    </tr>
                                </table>
                            </form>
                        </div>
                    </body>
                </html>'''

	return HttpResponse (message)

@csrf_exempt
def showdata (request):
    if request.method == "POST":
        firstName = request.POST.get("firstName", "")
        lastName = request.POST.get("lastName", "")
        midName = request.POST.get("midName", "")
        gender = request.POST.get("gender", "")
        dateOfBirth = request.POST.get("dateOfBirth", "")
        print firstName
        print lastName
        print midName
        print gender
        print dateOfBirth

        a = Users.objects.create(
                firstName=firstName,
                lastName=lastName,
                middleName=midName,
                gender=gender,
                dateOfBirth=dateOfBirth
        )
        a.save()
        #with connection.cursor() as cursor:
            #cursor.execute("INSERT INTO person (firstname, lastname, middlename, gender, dateofB) VALUES (%s, %s, %s, %s, %s)", (firstName, lastName, midName, gender, dateOfBirth))

        # cursor.execute("DELETE FROM login_users where id= %s", user_id)
    
        # row = cursor.fetchone()


    return HttpResponseRedirect('/career/select/')

def select (request):

    user = ''
    for row in Users.objects.all():
        print(row.id)
        print(row.firstName)
        print(row.lastName)
        print(row.middleName)
        print(row.gender)
        print(row.dateOfBirth)
        user += '''
                <tr>
                    <td>'''+str(row.id)+'''</td>
                    <td>'''+row.firstName+'''</td>
                    <td>'''+row.lastName+'''</td>
                    <td>'''+row.middleName+'''</td>
                    <td>'''+row.gender+'''</td>
                    <td>'''+row.dateOfBirth+'''</td>
                    <td><a href="/career/update/?id='''+str(row.id)+'''">Update</a></td>
                    <td><a href="/career/delete/?id='''+str(row.id)+'''">Delete</a></td>
                </tr>
                '''
        
    # print user

    message = """<html>
                    <head>
                        <style>
                            body {
                                margin: 0;
                                padding: 0;
                            }

                            .container {
                                position: relative;
                                width: 100%;
                            }

                        </style>
                    </head>
                    <body>
                        <div class="container">
                            <table border="1" width="800" style="margin-left: auto; margin-right: auto; margin-top: 30px;">
                                """+user+"""
                            </table>
                        </div>
                    </body>
                </html>"""

    # message = 'xxxx'

    return HttpResponse(message)

def update(request):
    _id = request.GET.get('id','')

    row = Users.objects.filter(id=_id)
    person = row[0]
    maleSelected = ''
    if person.gender == 'm':
        maleSelected = 'checked'

    femaleSelected = ''
    if person.gender == 'f':
        femaleSelected = 'checked'

    message = '''<html>
                    <head>
                        <style>
                            body {
                                margin: 0;
                                padding: 0;
                            }

                            .container {
                                position: relative;
                                width: 100%;
                            }

                        </style>
                    </head>
                    <body>
                        <div class="container">
                            <form name="submit_form" id="submit_form" action="/career/doUpdate/" method="post">
                                <input type="hidden" name="id" value="'''+str(person.id)+'''" />
                                <table border="1" style="width: 400px; margin-left: auto; margin-right: auto; margin-top: 30px;" cellpadding="8" cellspacin="8">
                                    <tr>
                                        <td style="width: 30%; text-align: center;">
                                            First Name
                                        </td>
                                        <td>
                                            <input type="text" name="firstName" value="'''+person.firstName+'''" placeholder="Please enter firstname." style="width: 100%; height: 30px;" />
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="width: 30%; text-align: center;">
                                            Last Name
                                        </td>
                                        <td>
                                            <input type="text" name="lastName" value="'''+person.lastName+'''" placeholder="Please enter lastname." style="width: 100%; height: 30px;" />
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="width: 30%; text-align: center;">
                                            Middle Name
                                        </td>
                                        <td>
                                            <input type="text" name="midName" value="'''+person.middleName+'''" placeholder="Please enter middle name." style="width: 100%; height: 30px;" />
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="width: 30%; text-align: center;">
                                            Gender
                                        </td>
                                        <td>
                                            <input type="radio" name="gender" value="m" '''+maleSelected+''' /> Male
                                            <br />
                                            <input type="radio" name="gender" value="f" '''+femaleSelected+''' /> Female
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="width: 30%; text-align: center;">
                                            Date of birth
                                        </td>
                                        <td>
                                            <input type="text" name="dateOfBirth" value="'''+person.dateOfBirth+'''" placeholder="Please enter date of birth." style="width: 100%; height: 30px;" />
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="width: 30%; text-align: center;">
                                            &nbsp;
                                        </td>
                                        <td>
                                            <input type="button" value="Cancel" />
                                            <input type="submit" value="Submit" />
                                        </td>
                                    </tr>
                                </table>
                            </form>
                        </div>
                    </body>
                </html>'''

    return HttpResponse (message)

@csrf_exempt
def doUpdate (request):
    if request.method == "POST":
        _id = request.POST.get("id", "")
        firstName = request.POST.get("firstName", "")
        lastName = request.POST.get("lastName", "")
        middleName = request.POST.get("midName", "")
        gender = request.POST.get("gender", "")
        dateOfBirth = request.POST.get("dateOfBirth", "")
        print firstName
        print lastName
        print middleName
        print gender
        print dateOfBirth

        a = Users.objects(id=_id).first()
        a.firstName = firstName
        a.lastName = lastName
        a.middleName = middleName
        a.gender = gender
        a.dateOfBirth = dateOfBirth
        a.save()

        #with connection.cursor() as cursor:
            #cursor.execute("UPDATE person SET firstname = %s, lastname = %s, middlename = %s, gender = %s, dateofB = %s WHERE id = %s", (firstName, lastName, midName, gender, dateOfBirth, _id))

    return HttpResponseRedirect('/career/select/')

def delete(request):
    _id = request.GET.get('id','')
    a = Users.objects(id=_id)
    if a:
        a.delete()
    #with connection.cursor() as cursor:
         #cursor.execute("DELETE FROM person where id= %s", _id)
         
    return HttpResponseRedirect('/career/select/')

