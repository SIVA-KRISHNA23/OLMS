from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
import json
from student.models import Leave, Outing
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

customuser = get_user_model()

@csrf_exempt
def qr_code_scanner(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        scanned_data = data.get('scanned_data')
        action = data.get('action')
        try:
            user = customuser.objects.get(email=scanned_data)
        except customuser.DoesNotExist:
            return JsonResponse({'message': 'Invalid user', 'status': 'error'})
        
        current_time = timezone.now()
        additional_info = ""

        if action == 'Leave':
            leave = Leave.objects.filter(user=user, status='Approved').order_by('-id').first()
            if leave:
                if leave.scanned_count < 2:
                    if leave.scanned_count == 0:
                        leave.first_scan_time = current_time
                        additional_info = "Checked out"
                    elif leave.scanned_count == 1:
                        leave.last_scan_time = current_time
                        additional_info = "Checked in"
                    leave.scanned_count += 1
                    leave.save()
                    return JsonResponse({'message': 'Scan successful', 'status': 'success', 'redirect': True, 'email': user.email, 'additional_info': additional_info})
                else:
                    return JsonResponse({'message': 'Invalid QR code', 'status': 'error'})
            else:
                return JsonResponse({'message': 'Invalid Leave QR code', 'status': 'error'})

        elif action == 'Outing':
            outing = Outing.objects.filter(user=user, status='Approved').order_by('-id').first()
            if outing:
                if outing.scanned_count < 2:
                    if outing.scanned_count == 0:
                        outing.first_scan_time = current_time
                        additional_info = "Checked out"
                    elif outing.scanned_count == 1:
                        outing.last_scan_time = current_time
                        additional_info = "Checked in"
                    outing.scanned_count += 1
                    outing.save()
                    return JsonResponse({'message': 'Scan successful', 'status': 'success', 'redirect': True, 'email': user.email, 'additional_info': additional_info})
                else:
                    return JsonResponse({'message': 'Invalid QR code', 'status': 'error'})
            else:
                return JsonResponse({'message': 'Invalid Outing QR code', 'status': 'error'})

    return render(request, 'qrscanner.html')

@login_required
def user_details(request, email):
    try:
        user = customuser.objects.get(email=email)
    except customuser.DoesNotExist:
        return redirect('qr_code_scanner')
    additional_info = request.GET.get('additional_info', '')  # Fetch additional_info from query parameter
    return render(request, 'user_details.html', {'user': user, 'additional_info': additional_info})

@login_required
def scanned_today(request):
    today = timezone.now().date()
    leaves_today = Leave.objects.filter(
        first_scan_time__date=today
    ) | Leave.objects.filter(
        last_scan_time__date=today
    )
    outings_today = Outing.objects.filter(
        first_scan_time__date=today
    ) | Outing.objects.filter(
        last_scan_time__date=today
    )

    entries_today = []

    for leave in leaves_today:
        if leave.first_scan_time and leave.first_scan_time.date() == today:
            entries_today.append({
                'user': leave.user,
                'scan_time': leave.first_scan_time,
                'status': 'Checked out',
                'type': 'Leave'
            })
        if leave.last_scan_time and leave.last_scan_time.date() == today:
            entries_today.append({
                'user': leave.user,
                'scan_time': leave.last_scan_time,
                'status': 'Checked in',
                'type': 'Leave'
            })

    for outing in outings_today:
        if outing.first_scan_time and outing.first_scan_time.date() == today:
            entries_today.append({
                'user': outing.user,
                'scan_time': outing.first_scan_time,
                'status': 'Checked out',
                'type': 'Outing'
            })
        if outing.last_scan_time and outing.last_scan_time.date() == today:
            entries_today.append({
                'user': outing.user,
                'scan_time': outing.last_scan_time,
                'status': 'Checked in',
                'type': 'Outing'
            })

    entries_today = sorted(entries_today, key=lambda x: x['scan_time'], reverse=True)

    context = {
        'entries_today': entries_today
    }
    return render(request, 'scanned_today.html', context)
