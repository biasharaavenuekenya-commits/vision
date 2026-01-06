# main/views.py
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib import messages
from .forms import RegistrationForm
from .models import Subscriber

def home(request):
    form = RegistrationForm()
    total_subscribers = Subscriber.objects.count()
    
    # Show spots remaining as informational, not as a hard limit
    # If you want to show "Limited to first 25" as a marketing message, 
    # but still allow more registrations, keep the calculation
    spots_display = max(0, 25 - total_subscribers)
    
    context = {
        'form': form,
        'spots_remaining': spots_display,  # This is now just for display
        'total_subscribers': total_subscribers,
        'total_spots': 25  # For display purposes only
    }
    return render(request, 'main/home.html', context)

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            subscriber = form.save()
            
            total_subscribers = Subscriber.objects.count()
            
            # Send email to user
            user_subject = "Welcome to VISION 2026 – Designed, Not Default"
            user_message = render_to_string('main/emails/welcome_user.html', {
                'name': subscriber.name,
            })
            
            send_mail(
                user_subject,
                "strip_tags(user_message)",  # Plain text version
                settings.DEFAULT_FROM_EMAIL,
                [subscriber.email],
                html_message=user_message,
                fail_silently=False,
            )
            
            # Send notification to admin
            admin_subject = f"🎯 New VISION 2026 Registration: {subscriber.name}"
            admin_message = render_to_string('main/emails/notification_admin.html', {
                'subscriber': subscriber,
                'total_count': total_subscribers,
            })
            
            send_mail(
                admin_subject,
                "strip_tags(admin_message)",  # Plain text version
                settings.DEFAULT_FROM_EMAIL,
                [settings.ADMIN_EMAIL],
                html_message=admin_message,
                fail_silently=False,
            )
            
            messages.success(request, f'Registration successful! Check your email ({subscriber.email}) for confirmation.')
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    
    return render(request, 'main/home.html', {'form': form})