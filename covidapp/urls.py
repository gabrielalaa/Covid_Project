from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('switch-language/<str:lang_code>/', views.switch_language, name='switch_language'),
    path('create-account/', views.create_account, name='create_account'),
    path('decrypt-message/', views.decrypt_message, name='decrypt_message'),
    path('generate-plots/', views.generate_plots, name='generate_plots'),
    path('predictions/', views.predictions, name='predictions'),
]
