from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect

def admin_index(request):

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM login")
        users = cursor.fetchall()

    return render(request,'app/index.html',{'users': users})

def admin_delete(request):
    if request.POST:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM login WHERE email = %s AND type = %s", 
                [request.POST['email'], request.POST['type']])
        return render(request, 'app/index.html', {'status': 'User deleted successfully'})
    
    return render(request, 'app/index.html', {'status': 'Please specify user details - login email and user type'})

def admin_edit_req(request):
    if request.POST:
        type = request.POST['type']
        if type == 'gym':
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM gym WHERE email = %s", 
                [request.POST['email']])
                gym = cursor.fetchone()
            return render(request,'app/gym_edit.html', {'gym': gym })
        elif type == 'member':
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM member WHERE email = %s", 
                [request.POST['email']])
                member = cursor.fetchone()

            return render(request, 'app/member_edit.html', {'member': member })
        elif type == 'trainer':
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM trainer WHERE email = %s", 
                [request.POST['email']])
                trainer = cursor.fetchone()

            return render(request, 'app/trainer_edit.html', {'trainer': trainer })
    else:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM login")
            users = cursor.fetchall()
        return render(request, 'app/index.html', {'users': users, 'status': 'Edit request failed'})

def admin_edit_action(request):
        type = request.POST['type']
        if type == 'gym':
            with connection.cursor() as cursor:
                cursor.execute("UPDATE gym SET name = %s, address = %s, upper_price_range = %s, \
                    lower_price_range = %s, capacity = %s, level = %s, region = %s WHERE email = %s", 
                    [request.POST['name'], request.POST['address'], request.POST['upper_price_range'],
                    request.POST['lower_price_range'],request.POST['capacity'],request.POST['lvl'], request.POST['loc'], request.POST['email']])
            
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM login")
                users = cursor.fetchall()
            return render(request, 'app/index.html', {'users': users, 'status': 'Gym details edited successfully'})
        
        elif type == 'member':
            cursor.execute("UPDATE member SET first_name = %s, last_name = %s, gender = %s, preferred_gym_location = %s, \
                budget = %s, focus1 = %s, focus2 = %s, focus3 = %s WHERE email = %s",[request.POST['first_name'],request.POST['last_name'],
                request.POST['gender'], request.POST['level'], request.POST['location'], request.POST['budget'],
                request.POST['focus1'],request.POST['focus2'],request.POST['focus3'],request.POST['email']])

            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM login")
                users = cursor.fetchall()
            return render(request, 'app/index.html', {'users': users, 'status': 'Member details edited successfully'})
            
        elif type == 'trainer':
            cursor.execute("UPDATE trainer SET first_name = %s, last_name = %s, gender = %s, upper_price_range = %s, \
                    lower_price_range = %s, experience = %s, focus1 = %s, focus2 = %s, focus3 = %s, level = %s WHERE email = %s"
                    , [request.POST['first_name'], request.POST['last_name'], request.POST['gender'],
                        request.POST['upper_price_range'] , request.POST['lower_price_range'], request.POST['experience'], 
                        request.POST['focus1'],request.POST['focus2'],request.POST['focus3'],request.POST['level'],request.POST['email']])

            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM login")
                users = cursor.fetchall()
            return render(request, 'app/index.html', {'users': users, 'status': 'Trainer details edited successfully'})
                
          
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
                cursor.execute("INSERT INTO login VALUES \
                    (%s, %s, %s)", [request.POST['email'], request.POST['password'], type])
                if (type == 'member'):
                    cursor.execute("INSERT INTO member (email,first_name,last_name,gender,level,preferred_gym_location,budget,focus1,focus2,focus3) \
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                        , [request.POST['email'], request.POST['first_name'], request.POST['last_name'], 
                            request.POST['gender'], request.POST['level'], request.POST['preferred_gym_location'],
                            request.POST['budget'], request.POST['focus1'], request.POST['focus2'], request.POST['focus3'] ])
                elif (type == 'trainer'):
                    cursor.execute("INSERT INTO trainer (email, first_name, last_name, gender, upper_price_range, lower_price_range,experience,focus1,focus2,focus3,level) \
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                        , [request.POST['email'], request.POST['first_name'], request.POST['last_name'],
                            request.POST['gender'], request.POST['upper_price_range'], request.POST['lower_price_range'],
                            request.POST['experience'], request.POST['focus1'], request.POST['focus2'], request.POST['focus3'],
                            request.POST['level']])
                elif (type == 'gym'):
                    cursor.execute("INSERT INTO gym (name, email, address, upper_price_range, lower_price_range, capacity, level, region) \
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                        , [request.POST['name'], request.POST['email'], request.POST['address'],
                            request.POST['upper_price_range'], request.POST['lower_price_range'], request.POST['capacity'],
                            request.POST['level'], request.POST['region']])
                return render(request, "registration/reg_submit.html", context)
            else:
                status = '%s with email %s already exists' % (type, request.POST['email'])
                context['status'] = status
                return render(request,'registration/register.html', context)



def search_view(request):
    return render(request, 'search/search_base.html')

def search_request(request):
    if request.POST['search']:
        string = request.POST['search']
        type = request.POST['type']
        if type == "gym":
            location = request.POST.get('loc',False)
        if type == "trainer":
            gender = request.POST.get('gend',False)
        level = request.POST.get('lvl',False)
        focus1 = request.POST.get('foc1',False)
        focus2 = request.POST.get('foc2',False)
        focus3 = request.POST.get('foc3',False)
        budget = request.POST.get('budget',False)
        gymaction = "SELECT DISTINCT g.id, g.name, g.email, g.address, g.upper_price_range, g.lower_price_range, g.capacity, g.level, g.region \
            FROM gym g, gymfocus f \
            WHERE name LIKE '%%" + string + "%%'"
        traineraction = "SELECT DISTINCT t.id, t.email, t.first_name, t.last_name, t.gender, t.upper_price_range, t.lower_price_range, t.experience, t.focus1, t.focus2, t.focus3, t.level \
                FROM trainer t, focus f \
                WHERE first_name LIKE '%%" + string + "%%' \
                    OR last_name LIKE '%%" + string + "%%'"
        if type == "gym":
            with connection.cursor() as cursor:
                if location != "":
                    gymaction += " AND g.region = '" + location + "'"
                if level != "":
                    gymaction += " AND g.level = '" + level + "'"
                if budget != "":
                    gymaction += " AND g.lower_price_range <= " + budget
                    gymaction += " AND " + budget + " <= g.upper_price_range"
                if focus1 != "":
                    gymaction += " AND f.focus = '" + focus1 + "'"
                if focus2 != "":
                    gymaction += " AND f.focus = '" + focus2 + "'"
                if focus3 != "":
                    gymaction += " AND f.focus = '" + focus3 + "'"
                if (focus1 != "") or (focus2 != "") or (focus3 != ""):
                    gymaction += " AND g.email = f.gym_email" 
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
                if budget != "":
                    traineraction += " AND t.lower_price_range <= " + budget 
                    traineraction += " AND " + budget + " <= t.upper_price_range"
                if focus1 != "":
                    traineraction += "AND f.focus = '" + focus1 + "'"
                if focus2 != "":
                    traineraction += "AND f.focus = '" + focus2 + "'"
                if focus3 != "":
                    traineraction += "AND f.focus = '" + focus3 + "'"
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
                cursor.execute("SELECT id FROM " + type + " WHERE email = %s", [request.POST['email']])
                myid = str(cursor.fetchone()[0])
                return redirect('loggedhome', type = type, myid = myid, permanent = True)
    return render(request, "registration/login.html", context)

def loggedhome(request, type, myid):
    return redirect('profile_view', type, myid)


    # context["status"] = status 
    # m = Login.objects.get(username=request.POST['email'])
    # if m.check_password(request.POST['password']):
    #    request.session['member_id'] = m.id
    #    return HttpResponse("You're logged in.")
    # else:
    #     return HttpResponse("Your username and password didn't match.")

def recommends_view(request, member_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM member WHERE id = " + member_id)
        member = cursor.fetchone()
    name = member[2]
    email = member[1]
    level = member[5]
    region = member[6]
    budget = str(member[7])
    focus = member[8:11]
        # tuple contains:
        # id, email, first_name, last_name, gender, level, preferred_gym_location, budget, focus1, focus2, focus3
        # look up gyms and trainers with above info
    with connection.cursor() as cursor:
        cursor.execute("SELECT * \
                        FROM gym g\
                        WHERE g.region = '" + region +
                        "' AND " + budget + " BETWEEN g.lower_price_range AND g.upper_price_range \
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
                        FROM trainer \
                        WHERE " + budget + " BETWEEN lower_price_range AND upper_price_range \
                            AND '" + level + "' = level \
                                AND ('" + focus[0] + "' IN (focus1, focus2, focus3) \
                                    OR '" + focus[1] + "' IN (focus1, focus2, focus3) \
                                    OR '" + focus[2] + "' IN (focus1, focus2, focus3))")

        reco_trainers = cursor.fetchall()
    with connection.cursor() as cursor:
        cursor.execute("SELECT m.first_name, m.last_name \
                        FROM member m \
                        WHERE m.preferred_gym_location = '" + region + 
                    "' AND m.id != " + member_id + " \
                        AND m.email in (SELECT mt.member_email \
                                            FROM member_trainer mt \
                                            WHERE mt.member_email = '" + email +  
                                            "' AND mt.trainer_email in (SELECT mt1.trainer_email \
                                                                        FROM member_trainer mt1 \
                                                                        WHERE m.email = mt1.member_email) \
                                        UNION \
                                        SELECT mg.member_email \
                                            FROM member_gym mg \
                                            WHERE mg.member_email = '" + email + 
                                            "' AND mg.gym_email in (SELECT mg1.gym_email \
                                                                        FROM member_gym mg1 \
                                                                        WHERE m.email = mg1.member_email))")
        reco_members = cursor.fetchall()                            
    return render(request, 'recommendations/recos.html', {'name': name,
                                'reco_gyms': reco_gyms,
                                'reco_trainers': reco_trainers,
                                'reco_members': reco_members})

def rating(request, *args):
    #TODO: add case for insert rating for gyms, need to edit rating.html as well
    if request.POST:
        rate = request.POST.get('rating',False)
        member_email = request.POST.get('memberemail',False)
        type = request.POST.get('type',False)
        if type == 'trainer':
            trainer_email = request.POST.get('traineremail',False)
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM trainer_ratings \
                                WHERE trainer_email = '" + trainer_email + "'")
                in_trainer_rating = cursor.fetchone()
            if in_trainer_rating:
                with connection.cursor() as cursor:
                    cursor.execute("UPDATE member_trainer SET trainer_rating = " + rate + " WHERE member_email = '" + member_email + "' AND trainer_email = '" + trainer_email + "'")
                with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM trainer_ratings where trainer_email = '" + trainer_email + "'")
                    rating = cursor.fetchone()
                    return render(request,'ratings/rating.html',{'rating': rating })
            else:
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO member_trainer (member_email,trainer_email,trainer_rating) VALUES ('" + member_email + "','"+trainer_email+"',"+rate+")")
                with connection.cursor() as cursor:
                    cursor.execute("SELECT * from trainer_ratings where trainer_email = '" + trainer_email + "'")
                    rating = cursor.fetchone()
                    return render(request,'ratings/rating.html',{'rating':rating})
        if type == 'gym':
            gym_email = request.POST.get('gymemail',False)
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM gym_ratings \
                            WHERE gym_email = '" + gym_email + "'")
                in_gym_rating = cursor.fetchone()
            if in_gym_rating:
                with connection.cursor() as cursor:
                    cursor.execute("UPDATE member_gym SET gym_rating = " + rate + " WHERE member_email = '" + member_email + "' AND gym_email = '" + gym_email + "'")
                with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM gym_ratings where gym_email = '" + gym_email + "'")
                    rating = cursor.fetchone()
                    return render(request,'ratings/rating.html',{'rating': rating })
            else:
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO member_gym (member_email,gym_email,gym_rating) VALUES ('" + member_email + "','"+gym_email+"',"+rate+")")
                with connection.cursor() as cursor:
                    cursor.execute("SELECT * from gym_ratings where gym_email = '" + gym_email + "'")
                    rating = cursor.fetchone()
                    return render(request,'ratings/rating.html',{'rating':rating})
    elif len(args) != 0:
        type = args[0]
        id = args[1]
        with connection.cursor() as cursor:
            cursor.execute("SELECT email FROM " + type +  " WHERE id = " + str(id))
            email = cursor.fetchone()
        return render(request,'ratings/rating.html', {'type': type,
                                                        'email': email })
    else:
        return render(request,'ratings/rating.html',{})





def profile_view(request, type, id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * \
                        FROM " + type + 
                        " WHERE id = " + id)
        profile_info = cursor.fetchone()
    
    if type == 'member':
        email = profile_info[1]
        with connection.cursor() as cursor:
            cursor.execute("SELECT * \
                            FROM gym g \
                            WHERE g.email IN (SELECT mg.gym_email \
                                                FROM member_gym mg \
                                                WHERE mg.member_email = '" + email + "')") 
            member_gyms = cursor.fetchall()
        return render(request, 'profile/member.html', {'name': profile_info[2] + " " + profile_info[3],
                                'gender': profile_info[4],
                                'level': profile_info[5],
                                'region': profile_info[6],
                                'budget': profile_info[7],
                                'focus1': profile_info[8],
                                'focus2': profile_info[9],
                                'focus3': profile_info[10],
                                'member_gyms': member_gyms,
                                'email': email,
                                'id': profile_info[0]})
    elif type == 'trainer':
        email = profile_info[1]
        with connection.cursor() as cursor:
            cursor.execute("SELECT * \
                            FROM member m \
                            WHERE m.email IN (SELECT mt.member_email \
                                                FROM member_trainer mt \
                                                WHERE mt.trainer_email = '" + email + "')")
            trainer_members = cursor.fetchall()
        with connection.cursor() as cursor:
            cursor.execute("SELECT rating FROM trainer_ratings \
                            WHERE trainer_email = %s", [email])
            rating = str(cursor.fetchone()[0])
        return render(request, 'profile/trainer.html', {'name': profile_info[2] + ' ' + profile_info[3],
                                'gender': profile_info[4],
                                'upper_price_range': profile_info[5],
                                'lower_price_range': profile_info[6],
                                'experience': profile_info[7],
                                'focus1': profile_info[8],
                                'focus2': profile_info[9],
                                'focus3': profile_info[10],
                                'trainer_members': trainer_members,
                                'email': email, 
                                'rating': rating,
                                'id': profile_info[0]})
    elif type == 'gym':
        email = profile_info[2]
        with connection.cursor() as cursor:
            cursor.execute("SELECT * \
                            FROM member m \
                            WHERE m.email IN (SELECT mg.member_email \
                                                FROM member_gym mg \
                                                WHERE mg.gym_email = '" + email + "')")
            gym_members = cursor.fetchall()
        with connection.cursor() as cursor:
            cursor.execute("SELECT rating FROM gym_ratings \
                            WHERE gym_email = %s", [email])
            rating = str(cursor.fetchone()[0])

        context = {'name': profile_info[1],
                                'address': profile_info[3],
                                'upper_price_range': profile_info[4],
                                'lower_price_range': profile_info[5],
                                'capacity': profile_info[6],
                                'level': profile_info[7],
                                'region': profile_info[8],
                                'gym_members': gym_members,
                                'email': email,
                                'rating': rating,
                                'id': profile_info[0]}


        with connection.cursor() as cursor:
            cursor.execute("SELECT focus \
                            FROM gymfocus \
                            WHERE gym_email = '" + email + "'")
            focuses = cursor.fetchall()
            for i in range(len(focuses)):
                context['focus' + str(i)] = focuses[i][0]

        return render(request, 'profile/gym.html', context)
