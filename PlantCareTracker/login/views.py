import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
import mysql.connector as sql
from django.views.decorators.csrf import csrf_exempt 
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
            get_plant_list(request)
            return render(request, 'index.html')
        
    return render(request, 'login.html')

def get_plant_list(request):
    try:
        mydb = sql.connect(host='localhost', user='root', passwd='Krishna@511', database='plantdatabase')
        cursor = mydb.cursor()
        query1 = "select * from users where email='{}' and password='{}'".format(email, password)
        cursor.execute(query1)
        user_result = cursor.fetchone()

        if user_result is not None:
            userId = user_result[0]
            print(userId)

            cursor.execute("select * from {}".format("user"+str(userId)))
            data = cursor.fetchall()
            print(data)
            plant_list = [{'id' : plant[1], 'name': plant[2], 'species': plant[3], 'careLevel': plant[4], 'waterSchedule': plant[5]} for plant in data]

            return JsonResponse({'plants': plant_list})
        else:
            print("NO DATA")
            return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        print("exception occurred:", str(e))
        return JsonResponse({'error': 'Internal Server Error'}, status=500)
@csrf_exempt  # Apply the decorator to disable CSRF protection for simplicity (handle CSRF properly in production)
def add_plant(request):
    if request.method == 'POST':
        mydb = sql.connect(host='localhost', user='root', passwd='Krishna@511', database='plantdatabase')
        cursor = mydb.cursor()
        query1 = "select * from users where email='{}' and password='{}'".format(email, password)
        cursor.execute(query1)
        userId = cursor.fetchone()[0]
        print(userId)
        # Get JSON data from the request body
        data = json.loads(request.body)
        print()
        print(data)
        # Extract plant details
        plantId = data['id']
        plantName = data['name']
        plantSpecies = data['species']
        plantCareLevel = data['careLevel']
        plantWaterSchedule = data['waterSchedule']
        sql_query = "INSERT INTO {} VALUES (%s, %s, %s, %s, %s, %s)".format("user" + str(userId))
        # Tuple of values to insert
        values = (userId, plantId, plantName, plantSpecies, plantCareLevel, plantWaterSchedule)
        # Execute the query with the tuple of values
        cursor.execute(sql_query, values)
        mydb.commit()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
@csrf_exempt # Apply the decorator to disable CSRF protection for simplicity (handle CSRF properly in production)
def remove_plant(request):
    try:
        if request.method == 'POST':
            mydb = sql.connect(host='localhost', user='root', passwd='Krishna@511', database='plantdatabase')
            cursor = mydb.cursor()
            query1 = "select * from users where email='{}' and password='{}'".format(email, password)
            cursor.execute(query1)
            userId = cursor.fetchone()[0]
            print(userId)
            # Get JSON data from the request body
            data = json.loads(request.body)
            print("Received POST request to remove plant")
            print(f"Data: {data}")
            removeQuery = f"DELETE FROM user{userId} WHERE plantId = %s"
            cursor.execute(removeQuery, (data['id'],))
            mydb.commit()
            return JsonResponse({'status': 'success'})
    except Exception as e:
        # Log the exception for further analysis
        print(f"Error: {str(e)}")
        return JsonResponse({'status': 'error', 'message': 'Internal Server Error'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})