
from django.shortcuts import render
from django.views.generic import TemplateView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from Crime.models import Criminals, Feedback, UserReg, PoliceReg, Complaint


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'user/user_index.html'
    login_url = '/'

class ViewCriminals(LoginRequiredMixin,TemplateView):
    template_name = 'user/view_criminals.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(ViewCriminals,self).get_context_data(**kwargs)
        cri = Criminals.objects.all()
        context['cri'] = cri
        return context

class AddFeedback(LoginRequiredMixin,TemplateView):
    template_name = 'user/feedback.html'
    login_url = '/'

    def post(self, request, *args, **kwargs):
        f = request.POST['feed']

        ps = UserReg.objects.get(login_id=self.request.user.id)

        s = Feedback()
        s.feedback = f
        s.user = ps
        s.save()

        messages = "Added Successfully"
        return render(request,'user/feedback.html',{'message':messages})

class SelectStation(LoginRequiredMixin,TemplateView):
    template_name = 'user/select_sation.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(SelectStation, self).get_context_data(**kwargs)
        staff = PoliceReg.objects.filter(login__last_name='1', login__is_staff='0')
        context['staff'] = staff
        return context

class Complaint_reg(LoginRequiredMixin,TemplateView):
    template_name = 'user/complaint.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(Complaint_reg, self).get_context_data(**kwargs)
        st = self.request.GET['st']
        ps = UserReg.objects.get(login_id=self.request.user.id)

        context['st'] = st
        context['ps'] = ps
        return context

    def post(self, request, *args, **kwargs):
        st = request.POST['st']
        timee = request.POST['timee']
        date = request.POST['date']
        complaint = request.POST['complaint']
        location=request.POST['location']

        ps = UserReg.objects.get(login_id=self.request.user.id)
        pl = PoliceReg.objects.get(pk=st)

        com =Complaint()
        com.police = pl
        com.user = ps
        com.complaint = complaint
        com.location=location
        com.timee = timee
        com.c_date = date
        com.status = 'pending'
        com.status1='not_register'
        com.save()

        messages = "Registered Successfully"
        return render(request,'user/user_index.html',{'message':messages})


class View_complaint(LoginRequiredMixin,TemplateView):
    template_name = 'user/view_fir.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(View_complaint, self).get_context_data(**kwargs)
        m = Complaint.objects.filter(user__login=self.request.user.id)

        context['m'] = m
        return context