from django.shortcuts import render, redirect
from django.db import connection

# # Create your views here.
# def index(request):
#     """Shows the main page"""

#     ## Delete customer
#     if request.POST:
#         if request.POST['action'] == 'delete':
#             with connection.cursor() as cursor:
#                 cursor.execute("DELETE FROM customers WHERE customerid = %s", [request.POST['id']])

#     ## Use raw query to get all objects
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT * FROM customers ORDER BY customerid")
#         customers = cursor.fetchall()

#     result_dict = {'records': customers}

#     return render(request,'app/index.html',result_dict)

# # Create your views here.
# def view(request, id):
#     """Shows the main page"""
    
#     ## Use raw query to get a customer
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT * FROM customers WHERE customerid = %s", [id])
#         customer = cursor.fetchone()
#     result_dict = {'cust': customer}

#     return render(request,'app/view.html',result_dict)

# # Create your views here.
# def add(request):
#     """Shows the main page"""
#     context = {}
#     status = ''

#     if request.POST:
#         ## Check if customerid is already in the table
#         with connection.cursor() as cursor:

#             cursor.execute("SELECT * FROM customers WHERE customerid = %s", [request.POST['customerid']])
#             customer = cursor.fetchone()
#             ## No customer with same id
#             if customer == None:
#                 ##TODO: date validation
#                 cursor.execute("INSERT INTO customers VALUES (%s, %s, %s, %s, %s, %s, %s)"
#                         , [request.POST['first_name'], request.POST['last_name'], request.POST['email'],
#                            request.POST['dob'] , request.POST['since'], request.POST['customerid'], request.POST['country'] ])
#                 return redirect('index')    
#             else:
#                 status = 'Customer with ID %s already exists' % (request.POST['customerid'])


#     context['status'] = status
 
#     return render(request, "app/add.html", context)

# # Create your views here.
# def edit(request, id):
#     """Shows the main page"""

#     # dictionary for initial data with
#     # field names as keys
#     context ={}

#     # fetch the object related to passed id
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT * FROM customers WHERE customerid = %s", [id])
#         obj = cursor.fetchone()

#     status = ''
#     # save the data from the form

#     if request.POST:
#         ##TODO: date validation
#         with connection.cursor() as cursor:
#             cursor.execute("UPDATE customers SET first_name = %s, last_name = %s, email = %s, dob = %s, since = %s, country = %s WHERE customerid = %s"
#                     , [request.POST['first_name'], request.POST['last_name'], request.POST['email'],
#                         request.POST['dob'] , request.POST['since'], request.POST['country'], id ])
#             status = 'Customer edited successfully!'
#             cursor.execute("SELECT * FROM customers WHERE customerid = %s", [id])
#             obj = cursor.fetchone()


#     context["obj"] = obj
#     context["status"] = status
 
#     return render(request, "app/edit.html", context)
def home(request):
    return render(request,"home/home.html")

def register_view(request):
    return render(request, 'registration/register.html', {})

def register_request(request):
    context = {}
    status = ''

    if request.POST:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * \
                            FROM login l \
                            WHERE l.email = %s \
                            AND l.type = %s", 
                            [request.POST['email'], request.POST['type']])

            user = cursor.fetchone()
            type = request.POST['type']
            if user == None:
                cursor.execute("INSERT INTO login VALUES (%s, %s, %s)", [request.POST['email'], request.POST['password'], type])
                if (type == 'member'):
                    cursor.execute("INSERT INTO member VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                        , [request.POST['email'], request.POST['first_name'], request.POST['last_name'], 
                            request.POST['gender'], request.POST['level'], request.POST['preferred_gym_location'],
                            request.POST['budget'], request.POST['focus1'], request.POST['focus2'], request.POST['focus3'] ])
                elif (type == 'trainer'):
                    cursor.execute("INSERT INTO trainer VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                        , [request.POST['email'], request.POST['first_name'], request.POST['last_name'],
                            request.POST['gender'], request.POST['upper_price_range'], request.POST['lower_price_range'],
                            request.POST['experience'], request.POST['focus1'], request.POST['focus2'], request.POST['focus3'],
                            request.POST['level']])
                elif (type == 'gym'):
                    cursor.execute("INSERT INTO gym VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                        , [request.POST['name'], request.POST['email'], request.POST['address'],
                            request.POST['upper_price_range'], request.POST['lower_price_range'], request.POST['capacity'],
                            request.POST['level'], request.POST['region']])
                return render(request,"registration/reg_submit.html", context)
            else:
                status = '%s with email %s already exists' % (type, request.POST['email'])
                context['status'] = status
                return render(request,'registration/register.html', context)


def search_view(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT name, email \
                        FROM gym \
                        WHERE name LIKE %%%s%% \
                        UNION \
                        SELECT name, email \
                        FROM trainer \
                        WHERE name LIKE %%%s%%", request.POST['search'], request.POST['search'])
        rows = cursor.fetchall()
        result = {}
        for r in rows:
            result[r] = r
        return render(request, 'searches/search.html', result)

def login(request):
    """Shows the login page"""
    context = {}
    status = ''
 
    if request.POST:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * \
                            FROM login l \
                            WHERE l.email = %s \
                            AND l.type = %s \
                            AND l.password = %s",
                            [request.POST['email'],request.POST['type'],request.POST['password']])
            user = cursor.fetchone()
            if user == None:
                status = 'You do not have an account!'
            else:
                status = 'Welcome back!'
                context['status'] = status
                return redirect('home',context)

    #context["status"] = status 
    # m = Login.objects.get(username=request.POST['email'])
    # if m.check_password(request.POST['password']):
    #    request.session['member_id'] = m.id
    #    return HttpResponse("You're logged in.")
    # else:
    #     return HttpResponse("Your username and password didn't match.")
    context['status'] = status

    return render(request, "registration/login.html", context)