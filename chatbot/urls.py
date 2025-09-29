from django.contrib import admin
from django.urls import path, include
from chatbot_app.views import home


urlpatterns = [
    path('admin/', admin.site.urls),
    #path('api/', include('chatbot_app.urls')),
    path('', include('chatbot_app.urls')), 
    path('', home),
]
