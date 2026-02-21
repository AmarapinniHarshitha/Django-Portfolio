from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import ContactMessage

def contact_view(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message')

        # Save to database
        contact = ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        
        print(f"✅ Contact message saved: ID={contact.id}")

        # Email to admin
        send_mail(
            subject=f'New Contact Message: {subject}' if subject else 'New Contact Message from Portfolio',
            message=f'From: {name} ({email})\n\nMessage:\n{message}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=False,
        )
        print("✅ Email sent to admin")

        # Confirmation email to user
        send_mail(
            subject='Thank you for contacting Harshitha',
            message=f'Hi {name},\n\nThank you for reaching out! I have received your message and will get back to you soon.\n\nYour message: {message}\n\nBest regards,\nHarshitha Amarapinni',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )
        print("✅ Confirmation email sent to user")
        
        # Redirect to success page (not back to contact)
        return redirect('contact-success')  # This will go to the new success page
    
    return render(request, 'contact.html')

# Add this new view
def contact_success(request):
    return render(request, 'contact_success.html')