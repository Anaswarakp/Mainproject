from django.urls import path


from Crime.officer_view import Indexview, blockchain_profile, Blockchain_login, View_Fir, view_ledger_login, \
    view_blockchain_login

urlpatterns = [

    path('',Indexview.as_view()),
    path('blockchain_index',blockchain_profile.as_view()),
    path('login',Blockchain_login.as_view()),
    path('View_Fir',View_Fir.as_view()),
    path('view_ledger_login',view_ledger_login.as_view()),
    path('view_blockchain_login',view_blockchain_login.as_view())



]
def urls():
    return urlpatterns, 'officer','officer'