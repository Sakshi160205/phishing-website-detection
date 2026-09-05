from django.urls import path
from . import views

app_name = 'detector'

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('detector/', views.detector, name='detector'),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('analytics/', views.analytics, name='analytics'),
    
    # Prediction endpoints
    path('predict', views.predict, name='predict'),
    
    # API endpoints
    path('api/predict', views.api_predict, name='api_predict'),
    path('api/statistics', views.api_statistics, name='api_statistics'),
    path('api/history', views.api_history, name='api_history'),
    path('api/clear-history', views.api_clear_history, name='api_clear_history'),
    path('api/performance-trends', views.api_performance_trends, name='api_performance_trends'),
    path('api/performance-metrics', views.api_performance_metrics, name='api_performance_metrics'),
    path('api/analytics-data', views.api_analytics_data, name='api_analytics_data'),
    path('test', views.test_endpoint, name='test_endpoint'),
]
