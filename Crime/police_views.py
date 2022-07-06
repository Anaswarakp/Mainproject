from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from Crime.models import Criminals, PoliceReg, UserReg, Fir, Blockchain_ledger, Complaint, evidence


class IndexView(LoginRequiredMixin,TemplateView):
    template_name = 'police_staff/police_index.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(IndexView,self).get_context_data(**kwargs)

        criminal = Criminals.objects.filter(police__login=self.request.user.id).count()
        m = Complaint.objects.filter(status='approved',police__login=self.request.user.id).count()
        context['m'] =  m
        context['criminal'] =  criminal

        return context

class AddCriminals(LoginRequiredMixin,TemplateView):
    template_name = 'police_staff/add_criminals.html'
    login_url = '/'

    def post(self, request, *args, **kwargs):
        name = request.POST['name']
        addre = request.POST['addre']
        con = request.POST['con']
        age = request.POST['age']
        image = request.FILES['image']

        ps = PoliceReg.objects.get(login_id=self.request.user.id)

        s = Criminals()
        s.address = addre
        s.name = name
        s.contact = con
        s.age = age
        s.image = image
        s.police = ps
        s.save()

        messages = "Added Successfully"
        return render(request,'police_staff/add_criminals.html',{'message':messages})

class ViewCriminals(LoginRequiredMixin,TemplateView):
    template_name = 'police_staff/view_criminals.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(ViewCriminals,self).get_context_data(**kwargs)
        cri = Criminals.objects.all()

        context['cri'] = cri

        return context


class DeleteCriminals(View):
    def dispatch(self, request, *args, **kwargs):
        id = request.GET['c_id']
        user = Criminals.objects.get(pk=id).delete()
        return render(request,'police_staff/view_criminals.html',{'message':"Criminals Removed"})


# class ProfileView(LoginRequiredMixin,TemplateView):
#     template_name = 'police_staff/profile.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(ProfileView,self).get_context_data(**kwargs)
#         pl = PoliceReg.objects.get(login_id=self.request.user.id)
#
#         context['pl'] = pl
#
#         return context


class ApproveFIR(LoginRequiredMixin,TemplateView):
    template_name = 'police_staff/approve.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(ApproveFIR, self).get_context_data(**kwargs)
        m = Complaint.objects.filter(police__login=self.request.user.id,status='pending')

        context['m'] = m
        return context

class ApprFIR(View):
    def dispatch(self, request, *args, **kwargs):
        id = request.GET['id']
        user = Complaint.objects.get(pk=id)
        user.status='approved'

        user.save()
        return render(request,'police_staff/police_index.html',{'message':"Complaint Approved"})


class Fir_details(LoginRequiredMixin,TemplateView):
    template_name = 'police_staff/fir.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        id = self.request.GET['id']
        context = super(Fir_details,self).get_context_data(**kwargs)
        com = Complaint.objects.get(id=id)

        context['com'] = com

        return context



    def post(self, request, *args, **kwargs):
        user = User.objects.get(id=self.request.user.id)

        reporttime = request.POST['reporttime']

        informer = request.POST['informer']
        casedescription = request.POST['casedescription']
        place = request.POST['place']
        criminal = request.POST['criminal']
        explanation = request.POST['explanation']
        complaint_id=request.POST['complaint_id']
        com = Complaint.objects.get(id=complaint_id)

        se = Fir()
        se.complaint_id_id=complaint_id
        se.user=user
        se.reporttime = reporttime
        se.informer = informer
        se.casedescription = casedescription
        se.place = place
        se.criminal = criminal
        se.explanation=explanation
        se.status = 'null'
        com.status1="fir_registerd"
        com.save()
        se.save()

        return render(request,'police_staff/police_index.html',{'message':"FIR Registered"})

class RejectFIR(View):
    def dispatch(self, request, *args, **kwargs):
        id = request.GET['id']
        user = Complaint.objects.get(pk=id)
        user.status='declined'

        user.save()
        return render(request,'police_staff/police_index.html',{'message':"Complaint Declined"})


class ViewFIR(LoginRequiredMixin,TemplateView):
    template_name = 'police_staff/view_complaint.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(ViewFIR, self).get_context_data(**kwargs)
        m = Complaint.objects.filter(police__login=self.request.user.id,status='approved',status1='not_register')

        context['m'] = m
        return context

    def post(self, request, *args, **kwargs):
        charge = request.FILES['charge']
        fir = request.POST['fir']



        s = Complaint.objects.get(pk=fir)
        s.charge = charge
        s.save()

        messages = "Added Successfully"
        return render(request,'police_staff/police_index.html',{'message':messages})


class ViewUser(LoginRequiredMixin,TemplateView):
    template_name = 'police_staff/view_user.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(ViewUser, self).get_context_data(**kwargs)
        id = self.request.GET['id']
        m = UserReg.objects.filter(pk=id)

        context['m'] = m
        return context


class viewFir(LoginRequiredMixin,TemplateView):
    template_name = 'police_staff/view_fir.html'
    def get_context_data(self, **kwargs):
        context = super(viewFir, self).get_context_data(**kwargs)
        m = Complaint.objects.filter(police__login=self.request.user.id,status='approved',status1='fir_registerd')
        context['m'] = m
        return context


class fir_file_view(TemplateView):
    template_name = 'police_staff/fir_file_view.html'
    def get_context_data(self, **kwargs):
        context = super(fir_file_view, self).get_context_data(**kwargs)
        id=self.request.GET['id']
        m= m = Fir.objects.get(complaint_id=id)
        print(m)
        context['m'] = m
        return context

        # m = Fir.objects.filter(blockchain_status='active')
        # print(m)
        # context['m'] = m
        # return context

class view_evidence(TemplateView):
    template_name ='police_staff/view_evidence.html'
    def get_context_data(self, **kwargs):
        context = super(view_evidence, self).get_context_data(**kwargs)

        m = Complaint.objects.filter(police__login=self.request.user.id,status='approved',status1='fir_registerd')
        context['m'] = m

        return context

class evidence_details_view(TemplateView):
    template_name = 'police_staff/evidence_details_view.html'
    def get_context_data(self, **kwargs):
        context = super(evidence_details_view, self).get_context_data(**kwargs)
        try:
            id=self.request.GET['id']
            m = evidence.objects.get(police_id=self.request.user.id,ledger_id=id)
            print("qqqqqqqqqqqq",m)
            context['m'] = m
            return context
        except:
            pass

class add_evidence(TemplateView):
    template_name = 'police_staff/add_evidence.html'

    def get_context_data(self, **kwargs):
        context = super(add_evidence, self).get_context_data(**kwargs)
        id=self.request.GET['c_id']
        c=Complaint.objects.get(id=id)
        context['id'] = c.id
        return context

    def post(self, request, *args, **kwargs):

        id=request.POST['id']
        c=Complaint.objects.get(id=id)

        d =request.POST['date111']
        location =request.POST['location']
        filenumber =request.POST['filenumber']
        filename =request.POST['filename']


        location1 =request.POST['location1']
        time1 =request.POST['time1']
        date1 =request.POST['date1']
        evidence1 =request.POST['evidence1']

        location2 =request.POST['location2']
        time2 =request.POST['time2']
        date2 =request.POST['date2']
        evidence2 =request.POST['evidence2']

        location3 =request.POST['location3']
        time3 =request.POST['time3']
        date3 =request.POST['date3']
        evidence3 =request.POST['evidence3']

        location4 =request.POST['location4']
        time4 =request.POST['time4']
        date4 =request.POST['date4']
        evidence4 =request.POST['evidence4']

        location5 =request.POST['location5']
        time5 =request.POST['time5']
        date5 =request.POST['date5']
        evidence5 =request.POST['evidence5']

        location6 =request.POST['location6']
        time6 =request.POST['time6']
        date6 =request.POST['date6']
        evidence6 =request.POST['evidence6']


        evidence_db =evidence()

        evidence_db.police_id_id=self.request.user.id
        evidence_db.ledger_id_id=c.id

        evidence_db.date=d
        evidence_db.location=location
        evidence_db.filenumber=filenumber
        evidence_db.filename=filename


        evidence_db.location1 =location1
        evidence_db.time1 =time1
        evidence_db.date1 =date1
        evidence_db.evidence1 =evidence1

        evidence_db.location2 =location2
        evidence_db.time2 =time2
        evidence_db.date2 =date2
        evidence_db.evidence2 =evidence2

        evidence_db.location3 =location3
        evidence_db.time3 =time3
        evidence_db.date3 =date3
        evidence_db.evidence3 =evidence3

        evidence_db.location4 =location4
        evidence_db.time4 =time4
        evidence_db.date4 =date4
        evidence_db.evidence4 =evidence4

        evidence_db.location5 =location5
        evidence_db.time5 =time5
        evidence_db.date5 =date5
        evidence_db.evidence5 =evidence5

        evidence_db.location6 =location6
        evidence_db.time6 =time6
        evidence_db.date6 =date6
        evidence_db.evidence6 =evidence6
        evidence_db.save()

        return render(request,'police_staff/police_index.html',{'message':"evidence added"})

class fir_Approved(TemplateView):
    template_name = 'police_staff/approved_fir.html'
    def get_context_data(self, **kwargs):
        context = super(fir_Approved, self).get_context_data(**kwargs)
        m = Fir.objects.filter(blockchain_status='active')
        print(m)
        context['m'] = m
        return context

class update_evidence(TemplateView):
    template_name = 'police_staff/update_evidence.html'
    def get_context_data(self, **kwargs):
        context = super(update_evidence, self).get_context_data(**kwargs)
        try:
            id=self.request.GET['c_id']
            m = evidence.objects.get(police_id=self.request.user.id,ledger_id=id)
            print("2222222222222222222222222222222",m)
            print("qqqqqqqqqqqq",m)
            context['m'] = m
            return context
        except:
            pass

    def post(self, request, *args, **kwargs):

        id=request.POST['id']
        ev =evidence.objects.get(id=id)
        c=Complaint.objects.get(id=ev.ledger_id_id)

        d =request.POST['date111']
        location =request.POST['location']
        filenumber =request.POST['filenumber']
        filename =request.POST['filename']


        location1 =request.POST['location1']
        time1 =request.POST['time1']
        date1 =request.POST['date1']
        evidence1 =request.POST['evidence1']

        location2 =request.POST['location2']
        time2 =request.POST['time2']
        date2 =request.POST['date2']
        evidence2 =request.POST['evidence2']

        location3 =request.POST['location3']
        time3 =request.POST['time3']
        date3 =request.POST['date3']
        evidence3 =request.POST['evidence3']

        location4 =request.POST['location4']
        time4 =request.POST['time4']
        date4 =request.POST['date4']
        evidence4 =request.POST['evidence4']

        location5 =request.POST['location5']
        time5 =request.POST['time5']
        date5 =request.POST['date5']
        evidence5 =request.POST['evidence5']

        location6 =request.POST['location6']
        time6 =request.POST['time6']
        date6 =request.POST['date6']
        evidence6 =request.POST['evidence6']


        evidence_db =evidence.objects.get(id=id)

        evidence_db.police_id_id=self.request.user.id
        evidence_db.ledger_id_id=c.id

        evidence_db.date=d
        evidence_db.location=location
        evidence_db.filenumber=filenumber
        evidence_db.filename=filename


        evidence_db.location1 =location1
        evidence_db.time1 =time1
        evidence_db.date1 =date1
        evidence_db.evidence1 =evidence1

        evidence_db.location2 =location2
        evidence_db.time2 =time2
        evidence_db.date2 =date2
        evidence_db.evidence2 =evidence2

        evidence_db.location3 =location3
        evidence_db.time3 =time3
        evidence_db.date3 =date3
        evidence_db.evidence3 =evidence3

        evidence_db.location4 =location4
        evidence_db.time4 =time4
        evidence_db.date4 =date4
        evidence_db.evidence4 =evidence4

        evidence_db.location5 =location5
        evidence_db.time5 =time5
        evidence_db.date5 =date5
        evidence_db.evidence5 =evidence5

        evidence_db.location6 =location6
        evidence_db.time6 =time6
        evidence_db.date6 =date6
        evidence_db.evidence6 =evidence6
        evidence_db.save()

        return render(request,'police_staff/police_index.html',{'message':"evidence added"})

