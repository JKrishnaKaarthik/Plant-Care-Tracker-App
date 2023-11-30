from django.http import HttpResponse
from django.shortcuts import render
import mysql.connector as sql
email =''
password = ''

# Create your views here.
def login(request):
    global email, password
    if request.method == 'POST':
        mydb = sql.connect(host='localhost', user='root', passwd='Krishna@511', database='plantdatabase')
        cursor = mydb.cursor()
        data = request.POST
        for key, val in data.items():
            if key == 'email':
                email = val
            if key == 'password':
                password = val
        c = "select * from users where email='{}' and password='{}'".format(email, password)
        cursor.execute(c)
        fetch = tuple(cursor.fetchall())       
        if(fetch == ()):
            return HttpResponse("invalid user data")
        else :
            # return render(request, 'welcome.html')
            return HttpResponse("welcome to the Plant Care Tracker App")
        
    return render(request, 'login.html')
        