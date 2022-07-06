from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import TemplateView

#from Crime.models import
from Crime.models import UserType, PoliceStation, UserReg, PoliceReg, Officer_Reg


class IndexView(TemplateView):
    template_name = 'index.html'

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password= request.POST['password']
        user = authenticate(username=username,password=password)

        if user is not None:
            login(request,user)
            if user.last_name == '1':
                if user.is_superuser:
                    return redirect('/admin')
                elif UserType.objects.get(user_id=user.id).type == "user":
                    return redirect('/user')
                elif UserType.objects.get(user_id=user.id).type == "officer":
                    return redirect('/officer')
                else:
                    return redirect('/police')

            else:
                return render(request,'index.html',{'message':" User Account Not Authenticated"})
        else:
            return render(request,'index.html',{'message':"Invalid Username or Password"})


class PoliceRegs(TemplateView):
    template_name = 'police_reg.html'

    def get_context_data(self, **kwargs):
        context = super(PoliceRegs,self).get_context_data(**kwargs)
        pl = PoliceStation.objects.all()

        context['pl'] = pl

        return context

    def post(self, request,*args,**kwargs):
        sid = request.POST['name']
        print(sid)

        contact = request.POST['phone']
        print(contact)
        email = request.POST['email']
        print(email)
        location = request.POST['location']
        print(location)
        password = request.POST['password']
        print(password)
        s = PoliceStation.objects.get(pk=sid)
        fl = s.station_name
        print(fl)

        r = PoliceReg.objects.filter(station=s).count()
        if r>0:
            messages = "Staff Already Added"
            return render(request, 'police_reg.html', {'message': messages})
        else:

            try:
                 user = User.objects.create_user(username=email,password=password,first_name=fl,email=email,last_name=0)
                 user.save()
                 reg = PoliceReg()
                 reg.login = user
                 reg.contact = contact
                 reg.p_location = location
                 reg.station = s
                 reg.save()
                 usertype = UserType()
                 usertype.user = user
                 usertype.type = "police"
                 usertype.save()
                 messages = "Register Successfully."

                 return render(request, 'police_reg.html', {'message': messages})
            except:
                 messages = "not valid details"
                 return render(request,'police_reg.html',{'message':messages})


class UserRegister(TemplateView):
    template_name = 'user_reg.html'

    def post(self, request,*args,**kwargs):
        gender = request.POST['gender']
        fullname = request.POST['name']
        address = request.POST['address']
        email = request.POST['email']
        phone = request.POST['phone']
        dob = request.POST['dob']
        password = request.POST['password']

        try:
             user = User.objects.create_user(username=email,password=password,first_name=fullname,email=email,last_name=1)
             user.save()
             reg = UserReg()
             reg.login = user
             reg.gender =gender
             reg.address = address
             reg.dob = dob
             reg.contact = phone
             reg.save()
             usertype = UserType()
             usertype.user = user
             usertype.type = 'user'
             usertype.save()
             messages = "Register Successfully."

             return render(request, 'user_reg.html', {'message': messages})
        except:
             messages = "Username already used!.."
             return render(request,'user_reg.html',{'message':messages})





class Police_officer_reg(TemplateView):
    template_name = 'police_officer_reg.html'

    def post(self, request, *args, **kwargs):
        name = request.POST['name']
        email = request.POST['email']
        designation = request.POST['designation']
        password = request.POST['password']
        range=request.POST['range']

        try:
            user = User.objects.create_user(username=email, password=password, first_name=name, email=email,
                                            last_name=0)
            user.save()
            reg = Officer_Reg()
            reg.user = user
            reg.range = range
            reg.designation = designation
            reg.save()
            usertype = UserType()
            usertype.user = user
            usertype.type = 'officer'
            usertype.save()
            messages = "Register Successfully."

            return render(request, 'police_officer_reg.html', {'message': messages})
        except:
            messages = "Username already used!.."
            return render(request, 'police_officer_reg.html', {'message': messages})