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
    return render(request, 'search/search.html')

def search_request(request):
    if request.POST['search']:
        string = request.POST['search']
        type = request.POST.get('type',False)
        if type == "gym":
            location = request.POST.get('loc',False)
        if type == "trainer":
            gender = request.POST.get('gend',False)
        level = request.POST.get('lvl',False)
        focus1 = request.POST.get('foc1',False)
        focus2 = request.POST.get('foc2',False)
        focus3 = request.POST.get('foc3',False)
        gymaction = "SELECT DISTINCT g.name, g.email \
            FROM gym g, gymfocus f \
            WHERE name LIKE '%%" + string + "%%'"
        traineraction = "SELECT DISTINCT t.first_name, t.last_name, t.email \
                FROM trainer t, focus f \
                WHERE first_name LIKE '%%" + string + "%%' \
                    OR last_name LIKE '%%" + string + "%%'"
        if type == "gym":
            with connection.cursor() as cursor:
                if location != "":
                    gymaction += " AND g.region = '" + location + "'"
                if level != "":
                    gymaction += " AND g.level = '" + level + "'"
                if focus1 != "":
                    gymaction += " AND f.focus = '" + focus1 + "'"
                if focus2 != "":
                    gymaction += " AND f.focus = '" + focus2 + "'"
                if focus3 != "":
                    gymaction += " AND f.focus = '" + focus3 + "'"
                gymaction += " AND 1=1"
                cursor.execute(gymaction)
                gym_rows = cursor.fetchall()
                return render(request, 'search/search.html', 
                                {'gym': gym_rows,
                                'trainer': [],
                                'num_gyms': len(gym_rows),
                                'num_trainers': 0})
        elif type == "trainer":
            with connection.cursor() as cursor:
                if gender != "":
                    traineraction += "AND t.gender = '" + gender + "'"
                if level != "":
                    traineraction += "AND t.level = '" + level + "'"
                if focus1 != "":
                    traineraction += "AND f.focus = '" + focus1 + "'"
                if focus2 != "":
                    traineraction += "AND f.focus = '" + focus2 + "'"
                if focus3 != "":
                    traineraction += "AND f.focus = '" + focus3 + "'"
                traineraction += " AND 1=1'"
                cursor.execute(traineraction)
                trainer_rows = cursor.fetchall()
                return render(request, 'search/search.html', 
                                {'gym': [],
                                'trainer': trainer_rows,
                                'num_gyms': 0,
                                'num_trainers': len(trainer_rows)})
    else:
        return render(request, 'search/search.html',{})

def login_view(request):
    return render(request,'registration/login.html',{})

def login_request(request):
    """Shows the login page"""
    context = {}
 
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
                context['status'] = status
                return render(request,"registration/login.html",context)
            else:
                type = request.POST['type']
                cursor.execute("SELECT first_name FROM " + type + " WHERE email = %s", [request.POST['email']])
                fnmatch = cursor.fetchone()
                #email = request.POST['email']
                return redirect('loggedhome', fname = fname, permanent = True )
    return render(request, "registration/login.html", context)


def get(email,type):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id FROM " + type + " WHERE email = %s", [email])
        curid = cursor.fetchone()

    return curid

## CANNOT FIND ID SMH AND NEED REVERSE URL

    # context["status"] = status 
    # m = Login.objects.get(username=request.POST['email'])
    # if m.check_password(request.POST['password']):
    #    request.session['member_id'] = m.id
    #    return HttpResponse("You're logged in.")
    # else:
    #     return HttpResponse("Your username and password didn't match.")

    return render(request, "registration/login.html", context)

def recommends_view(request, member_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM member WHERE id = " + member_id)
    member = cursor.fetchone()
    email = member[1]
    level = member[5]
    region = member[6]
    budget = member[7]
    focus = [member[8:11]]
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM member_trainer WHERE member_email = %s" , email)  
    trainers = cursor.fetchall()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM member_gym WHERE member_email = %s", email)
    gyms = cursor.fetchall()
        # tuple contains:
        # id, email, first_name, last_name, gender, level, preferred_gym_location, budget, focus1, focus2, focus3
        # look up gyms and trainers with above info
    with connection.cursor() as cursor:
        cursor.execute("SELECT * \
                        FROM gym g\
                        WHERE g.region = " + region +
                        "AND " + budget + " BETWEEN g.lower_price_range AND g.upper_price_range \
                            AND ( '" + focus[0] + "' IN (SELECT focus \
                                                FROM gymfocus gf \
                                                WHERE gf.gym_email = g.email) \
                            OR '" + focus[1] + "' IN (SELECT focus \
                                                FROM gymfocus gf1 \
                                                WHERE gf1.gym_email = g.email)  \
                            OR '" + focus[2] + "' IN (SELECT focus \
                                                FROM gymfocus gf2 \
                                                WHERE gf2.gym_email = g.email))")
        reco_gyms = cursor.fetchall()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * \
                        FROM trainer t \
                        WHERE " + budget + " BETWEEN t.lower_price_range AND t.upper_price_range \
                            AND '" + level + "' = t.level \
                                AND ('" + focus[0] + "' =ANY(t.focus1, t.focus2, t.focus3) \
                                    OR '" + focus[1] + "' =ANY(t.focus1, t.focus2, t.focus3) \
                                    OR '" + focus[2] + "' =ANY(t.focus1, t.focus2, t.focus3))")
        reco_trainers = cursor.fetchall()
    with connection.cursor() as cursor:
        cursor.execute("SELECT m.first_name, m.last_name \
                        FROM member m \
                        WHERE m.preferred_gym_location = " + region + 
                        "AND m.email in (SELECT mt.member_email \
                                            FROM member_trainer mt \
                                            WHERE mt.member_email = '" + email +  
                                            "' AND mt.trainer_email in (SELECT mt1.trainer_email \
                                                                        FROM member_trainer mt1 \
                                                                        WHERE m.email = mt1.member_email) \
                                        UNION \
                                        SELECT mg.member_email \
                                            FROM member_gym mg \
                                            WHERE mg.member_email = '" + email + 
                                            "' AND mg.gym_email in (SELECT mg1.trainer_email \
                                                                        FROM member_gym mg1 \
                                                                        WHERE m.email = mg1.member_email)")
        reco_members = cursor.fetchall()
        
                            

    pass

def logged_home(request, member_id):
    pass
