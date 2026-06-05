from django.urls import path
from .views import *

Error_404 = 'CropRecommendationApp.views.Error_404'
Error_500 = 'CropRecommendationApp.views.Error_500'

urlpatterns = [    
    path('',Index,name='home'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),

    path('Crop/',Crop,name='crop'),
    path('Crop/<str:crop_name>/',Crop_details),    

    path('Recommend/',Crop_recommend,name='crop_recommend'),
    path('Fertilizer/',Fertilizer_suggest,name='fertilizer_suggest'),
    path('Disease/',Disease_detect,name='disease_detect'),
    path('Dashboard/', Dashboard_view, name='dashboard'),
    path('api/predict_dashboard/', api_predict_dashboard, name='api_predict_dashboard'),
]
