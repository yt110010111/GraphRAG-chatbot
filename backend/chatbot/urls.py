from django.urls import path
from .views import ChatbotView,CreateGraphView
from . import views

urlpatterns = [
     path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('verify-token/', views.verify_token, name='verify_token'),
    path('chat/', ChatbotView.as_view(), name='chatbot'),
    path('graphrag/create/', CreateGraphView.as_view(), name='create_graph'),
    #path('graphrag/query/', QueryGraphView.as_view(), name='query_graph'),
   
]
