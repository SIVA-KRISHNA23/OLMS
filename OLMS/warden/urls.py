from django.urls import path
from . import views
urlpatterns=[
    path("show-all-leaves/",views.showAllLeaves,name="show-all-leaves"),
    path("show-all-outings/",views.showAllOutings,name="show-all-outings"),
    path('update-leave/', views.updateLeave, name='update-leave'),
    path('update-outing/', views.updateOuting, name='update-outing'),
]