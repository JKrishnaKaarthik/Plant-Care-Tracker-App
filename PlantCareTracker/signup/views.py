from django.shortcuts import redirect, render
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
        cursor.execute("SELECT userID FROM users ORDER BY userID DESC LIMIT 1;")
        userId = cursor.fetchone()[0]
        userId = userId + 1
        cursor.execute("insert into users values({}, '{}', '{}', '{}', '{}')".format(userId, fName, lName, email, password))
        query2 = "CREATE TABLE `{}` (linkedUserID INT, plantName varchar(100), species varchar(100), carelevel varchar(50), waterschedule varchar(50), FOREIGN KEY (linkedUserID) REFERENCES users(userID))".format("user"+str(userId))
        cursor.execute(query2)
        mydb.commit()
        return redirect('/')
    else : 
        return render(request, 'signup.html')