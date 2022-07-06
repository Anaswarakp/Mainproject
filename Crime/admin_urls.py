from django.urls import path

from Crime.admin_views import IndexView, AddStation, ViewStation, DeletePolice, NewStation, RejectView, ApproveView, \
    ApprovedStation, ViewCriminals, ViewFeed, ViewUser, ViewFIR, Officer_approve, view_officer,Profile_details
from django.contrib.auth import views as auth_views
urlpatterns = [

    path('',IndexView.as_view()),

    path('AddStation',AddStation.as_view()),
    path('ViewStation',ViewStation.as_view()),
    path('DeletePolice',DeletePolice.as_view()),

    path('ViewCriminals',ViewCriminals.as_view()),
    path('Officer_approve',Officer_approve.as_view()),
    path('view_officer',view_officer.as_view()),
    path('single_view',Profile_details.as_view()),

    path('ViewFeed',ViewFeed.as_view()),
    path('ViewUser',ViewUser.as_view()),
    path('ViewFIR',ViewFIR.as_view()),

    path('NewStation',NewStation.as_view()),
    path('RejectView', RejectView.as_view()),
    path('ApproveView', ApproveView.as_view()),
    path('ApprovedStation', ApprovedStation.as_view()),
    path('logout/', auth_views.LogoutView.as_view(
        next_page='/'
        ),
        name='logout'
    ),

]
def urls():
      return urlpatterns,'admin','admin'