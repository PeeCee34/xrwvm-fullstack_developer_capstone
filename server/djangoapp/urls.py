# Uncomment the imports before you add the code
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
     path('get_dealers/', views.get_dealerships, name='get_dealers'),
    path('get_dealers/<str:state>/', views.get_dealerships, name='get_dealers_by_state'),
    path(route='login', view=views.login_user, name='login'),
    path('register/', views.registration_view, name='register'),
    path(route='dealer/<int:dealer_id>', view=views.get_dealer_details, name='dealer_details'),
    path(route='reviews/dealer/<int:dealer_id>', view=views.get_dealer_reviews, name='dealer_details'),
    path(route='add_review', view=views.add_review, name='add_review'),
    # # path for registration

    # path for login
    # path(route='login', view=views.login_user, name='login'),

    # path for dealer reviews view

    # path for add a review view

    # path for get_cars 
    path(route='get_cars', view=views.get_cars, name ='getcars'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
