from django.urls import path
from . import views
urlpatterns =[
    path('leave-form/',views.leaveForm,name="leave"),
    path('leaves/',views.showLeaves,name="show-leaves"),
    path('outings/',views.showOutings,name="show-outings"),
    path('outing-form/',views.OutingForm,name="outing")
]