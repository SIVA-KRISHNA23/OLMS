from django.shortcuts import render, redirect
from django.http import JsonResponse
from student.models import Leave, Outing
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage
from .utils import generate_qr_code
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Count,Q
from django.db.models.functions import TruncMonth

from django.utils.dateparse import parse_date

@login_required
def showAllLeaves(request):
    user = request.user
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if user.hostel == 'I1':
        leaves = Leave.objects.filter(user__username__startswith='N19').order_by('-id')
    elif user.hostel == 'I2':
        leaves = Leave.objects.exclude(user__username__startswith='N19').order_by('-id')
    else:
        leaves = Leave.objects.none()  # No leaves if hostel is neither I1 nor I2

    if start_date and end_date:
        start_date = parse_date(start_date)
        end_date = parse_date(end_date)
        leaves = leaves.filter(
            Q(first_scan_time__date__range=[start_date, end_date]) |
            Q(last_scan_time__date__range=[start_date, end_date])
        )

    # Calculate leaves per month for each user
    leaves_per_month = Leave.objects.filter(user=user).annotate(
        month=TruncMonth('last_scan_time')
    ).values('month').annotate(count=Count('id')).order_by('-month')

    paginator = Paginator(leaves, 10)  # Objects per page
    page = request.GET.get('pg')
    leaves = paginator.get_page(page)
    return render(request, 'showAllLeaves.html', {"leaves": leaves, "leaves_per_month": leaves_per_month})

@login_required
def showAllOutings(request):
    user = request.user
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    outings = Outing.objects.none()  # Initialize with empty queryset

    if user.hostel == 'I1':
        queryset = Outing.objects.filter(user__username__startswith='N19')
    elif user.hostel == 'I2':
        queryset = Outing.objects.exclude(user__username__startswith='N19')
    else:
        queryset = Outing.objects.none()

    if start_date and end_date:
        queryset = queryset.filter(out_date__range=[start_date, end_date])
    outings = queryset.order_by('-id')

    # Calculate outings per month for each user
    outings_per_month = Outing.objects.filter(user=user).annotate(
        month=TruncMonth('last_scan_time')
    ).values('month').annotate(count=Count('id')).order_by('-month')

    paginator = Paginator(outings, 10)  # Objects per page
    page = request.GET.get('pg')
    outings = paginator.get_page(page)

    return render(request, 'showAllOutings.html', {"outings": outings, "outings_per_month": outings_per_month})


# @csrf_exempt
# def updateLeave(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         leave_id = data.get('leave_id')
#         action = data.get('action')
#         leave = Leave.objects.get(pk=leave_id)

#         if action == 'approve':
#             qr_img = generate_qr_code(leave.user)
#             email = EmailMessage(
#                 subject='Leave Approval Notification',
#                 body='Your Leave application is done! Use the below QR code at the entrance gate.',
#                 from_email=settings.EMAIL_HOST_USER,
#                 to=[leave.user.email]
#             )
#             email.attach('leave_qr.png', qr_img.read(), 'image/png')
#             email.send()
#             leave.status = 'Approved'
#         elif action == 'disapprove':
#             email = EmailMessage(
#                 subject='Leave Rejected Notification',
#                 body='Your Leave application is Rejected!',
#                 from_email=settings.EMAIL_HOST_USER,
#                 # to=[leave.user.email]
#                 to=['sivakrishna197791@gmail.com']
#             )
#             print("[DEBUG] Sending rejection email for Leave...")
#             email.send()
#             print("[DEBUG] Leave rejection email sent.")
#             leave.status = 'Declined'

#         leave.save()

#         return JsonResponse({'status': leave.status})
#     else:
#         return JsonResponse({'error': 'Invalid request method'})

@csrf_exempt
def updateLeave(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        leave_id = data.get('leave_id')
        action = data.get('action')
        leave = Leave.objects.get(pk=leave_id)

        if action == 'approve':
            print("[DEBUG] Approving leave. Generating QR code...")
            try:
                qr_img = generate_qr_code(leave.user)
                qr_img.seek(0)  # Reset stream position
                email = EmailMessage(
                    subject='Leave Approval Notification',
                    body='Your Leave application is approved! Use the attached QR code at the entrance gate.',
                    from_email=settings.EMAIL_HOST_USER,
                    to=[leave.user.email]
                )
                print("[DEBUG] Attaching QR code and sending to:", leave.user.email)
                email.attach('leave_qr.png', qr_img.read(), 'image/png')
                email.send()
                print("[DEBUG] Approval email sent successfully.")
                leave.status = 'Approved'
            except Exception as e:
                print("[ERROR] Failed to send approval email:", e)
                return JsonResponse({'error': 'Email send failed', 'details': str(e)})

        elif action == 'disapprove':
            try:
                email = EmailMessage(
                    subject='Leave Rejected Notification',
                    body='Your Leave application is Rejected!',
                    from_email=settings.EMAIL_HOST_USER,
                    # You can put the student's actual email back here
                    to=[leave.user.email]
                    # or for debug: to=['sivakrishna197791@gmail.com']
                )
                print("[DEBUG] Sending rejection email...")
                email.send()
                print("[DEBUG] Rejection email sent.")
                leave.status = 'Declined'
            except Exception as e:
                print("[ERROR] Failed to send rejection email:", e)
                return JsonResponse({'error': 'Email send failed', 'details': str(e)})

        leave.save()
        print(f"[DEBUG] Leave ID {leave_id} status updated to {leave.status}")
        return JsonResponse({'status': leave.status})
    else:
        return JsonResponse({'error': 'Invalid request method'})


@csrf_exempt
def updateOuting(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        outing_id = data.get('outing_id')
        action = data.get('action')
        outing = Outing.objects.get(pk=outing_id)

        if action == 'approve':
            qr_img = generate_qr_code(outing.user)
            email = EmailMessage(
                subject='Outing Approval Notification',
                body='Your Outing application is done! Use the below QR code at the entrance gate.',
                from_email=settings.EMAIL_HOST_USER,
                to=[outing.user.email]
            )
            email.attach('outing_qr.png', qr_img.read(), 'image/png')
            email.send()
            outing.status = 'Approved'
        elif action == 'disapprove':
            email = EmailMessage(
                subject='Outing Rejected Notification',
                body='Your Outing application is Rejected.',
                from_email=settings.EMAIL_HOST_USER,
                to=[outing.user.email]
            )
            
            email.send()
            
            outing.status = 'Declined'

        outing.save()

        return JsonResponse({'status': outing.status})
    else:
        return JsonResponse({'error': 'Invalid request method'})
