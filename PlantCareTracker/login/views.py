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
            # return render(request, 'welcome.html')
            return render(request, 'index.html')
        
    return render(request, 'login.html')
         
        # Import this decorator

# ... (existing code)

@csrf_exempt  # Apply the decorator to disable CSRF protection for simplicity (handle CSRF properly in production)
def add_plant(request):
    if request.method == 'POST':
        mydb = sql.connect(host='localhost', user='root', passwd='Krishna@511', database='plantdatabase')
        cursor = mydb.cursor()

        # Get JSON data from the request body
        data = json.loads(request.body)
        print(data)
        # Extract plant details
        plant_name = data['name']
        plant_species = data['species']
        plant_care_level = data['careLevel']
        plant_water_schedule = data['waterSchedule']

        # Insert data into the MySQL database
        c = "INSERT INTO plants (name, species, care_level, water_schedule) VALUES (%s, %s, %s, %s)"
        cursor.execute(c, (plant_name, plant_species, plant_care_level, plant_water_schedule))
        mydb.commit()

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
