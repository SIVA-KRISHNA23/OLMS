from django.shortcuts import render,redirect
from student.models import Leave,Outing
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

customUser=get_user_model()

@login_required
def leaveForm(request):
    if request.method == "POST":
        user = request.user
        start_date = request.POST['outdate']
        end_date = request.POST['indate']
        reason = request.POST['reason']
        obj = Leave.objects.create(user=user,start_date=start_date,end_date=end_date,reason=reason)
        obj.save()
        return redirect('show-leaves')
    return render(request,'leave_application_form.html')

def getUser(id):
    return customUser.objects.get(id=id)

@login_required
def showLeaves(request):
    id= request.user.id
    user =getUser(id)
    leaves = Leave.objects.filter(user=user).order_by('-id')
    return render(request,'showLeaves.html',{'leaves':leaves})

@login_required
def showOutings(request):
    id= request.user.id
    user =getUser(id)
    outings = Outing.objects.filter(user=user).order_by('-id')
    return render(request,'showOutings.html',{'outings':outings})

@login_required
def OutingForm(request):
    if request.method == "POST":
        user = request.user
        out_time= request.POST['outtime']
        in_time = request.POST['intime']
        outdate = request.POST['outdate']
        reason = request.POST['reason']
        obj = Outing.objects.create(user=user,out_date=outdate,in_time=in_time,out_time=out_time,reason=reason)
        obj.save()
        return redirect('show-outings')
    return render(request,'outing_application_form.html')

