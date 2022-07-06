from django.urls import path

from Crime.police_views import IndexView, AddCriminals, ViewCriminals, DeleteCriminals, ApproveFIR, ApprFIR, RejectFIR, \
    ViewFIR, ViewUser, Fir_details, viewFir, fir_file_view, add_evidence, view_evidence, evidence_details_view, \
    update_evidence,fir_Approved
from django.contrib.auth import views as auth_views
urlpatterns = [

    path('',IndexView.as_view()),
    path('AddCriminals',AddCriminals.as_view()),
    path('ViewCriminals',ViewCriminals.as_view()),
    path('DeleteCriminals',DeleteCriminals.as_view()),
    path('ApproveFIR',ApproveFIR.as_view()),
    path('ApprFIR',ApprFIR.as_view()),
    path('RejectFIR',RejectFIR.as_view()),
    path('ViewFIR',ViewFIR.as_view()),
    path('ViewUser',ViewUser.as_view()),
    path('fir',Fir_details.as_view()),
    path('viewFirs',viewFir.as_view()),
    path('fir_file_view',fir_file_view.as_view()),
    path('add_evidence',add_evidence.as_view()),
    path('view_evidence',view_evidence.as_view()),
    path('evidence_details_view',evidence_details_view.as_view()),
    path('fir_Approved', fir_Approved.as_view()),
    path('update_evidence',update_evidence.as_view()),
    path('logout/', auth_views.LogoutView.as_view(
        next_page='/'
        ),
        name='logout'
    ),


]
def urls():
      return urlpatterns,'police','police'