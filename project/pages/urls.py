from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('signup/process/', views.signup_process, name='signup_process'),
    path('login/auth/', views.login_authentication, name='login_authentication'),
    path('logout/', views.logout_view, name='logout'),


    # User Views
    path('home/', views.home, name='home'),
    # path('home/<int:user_id>/', views.home, name='home_with_id'),
    path('challenge/', views.challenge, name='challenge'),
    path('scoreboard/', views.scoreboard, name='scoreboard'),
    path('scoreboards/', views.all_challenges_scoreboard, name='all_challenges_scoreboard'),
    path('submit-prediction/<int:challenge_id>/', views.submit_prediction, name='submit_prediction'),

    # Admin Views
    path('admin/home/', views.home_admin, name='home_admin'),
    # path('admin/home/<int:user_id>/', views.home_admin, name='home_admin_with_id'),
    path('admin/insights/', views.insights_admin, name='insights_admin'),
    path('admin/predict/', views.predict_admin, name='predict'),
    path('admin/new-challenge/', views.new_challenge, name='new_challenge'),
    path('admin/demand/', views.demand_admin, name='demand'),
    path('end_challenge/', views.end_challenge_page, name='end_challenge_page'),
    path('end_challenge/<int:challenge_id>/', views.end_challenge, name='end_challenge'),
]