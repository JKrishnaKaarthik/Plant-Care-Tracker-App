from django.shortcuts import render
import mysql.connector as sql

fName=''
lName=''
email=''
password=''

# Create your views here.
def signup(request):
    global fName, lName, email, password
    if(request.method == 'POST'):
        mydb = sql.connect(host='localhost', user='root', passwd='Krishna@511', database='plantdatabase')
        cursor = mydb.cursor()
        data = request.POST
        for key, val in data.items():
            if key == 'firstName':
                fName = val
            if key == 'lastName':
                lName = val
            if key == 'email':
                email = val
            if key == 'password':
                password = val
        userId = 0
        query ='SELECT userID FROM users ORDER BY userID DESC LIMIT 1;'
        userId = cursor.execute(query)
        userId = userId + 1
        cursor.execute("insert into users values('{}', '{}', '{}', '{}', '{}')".format(userId, fName, lName, email, password))
        mydb.commit()
    return render(request, 'signup.html')