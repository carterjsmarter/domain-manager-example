from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from user_management.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.views.generic import RedirectView
from django.views import View
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse, response
from django.conf import settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.contrib.auth.views import (
    PasswordResetConfirmView as DjangoPasswordResetConfirmView,
)


class Login(View):
    def get(self, request, *args, **kwargs):
        return render(request, "login.html")

    def post(self, request):
        data = request.POST
        context = {}
        if data.get("email") and data.get("password"):
            user = self._attempt_login(data)
            
            if user:
                login(self.request, user)
                # change this url w.r.t what you want to redirect after successful login
                url = reverse('domains:dashboard')
                return HttpResponseRedirect(url)
            context["login_failed_message"] = "Incorrect Email or Password."
        else:
            context["login_failed_message"] = "Please Enter Email Address"

        return render(request, "login.html", context)

    def _attempt_login(self, data):
        authentication_form = AuthenticationForm(data)
        if authentication_form.is_valid():
            user = authenticate(**authentication_form.cleaned_data)
            if user is not None and user.is_active:
                return user

        return False


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(settings.LOGIN_URL)


class ForgotPassword(View):
    def post(self, request):
        print("=== working ===")
        email = request.POST.get("email")
        User = get_user_model()
        associated_user = User.objects.filter(email=email).first()
        
        print("email: ", email)
        print("user: ", User)
        print("associated user: ", associated_user)
        
        if not associated_user:
            return JsonResponse({
                "status": False,
                "message": "Email address does not exist."
            })
        else:
            uid = urlsafe_base64_encode(force_bytes(associated_user.pk))
            token = default_token_generator.make_token(associated_user)
            reset_password_url = reverse(
                "user_management:reset",
                kwargs={"uidb64": uid, "token": token, "email": associated_user.email},
            )
            reset_password_url = self.request.build_absolute_uri(reset_password_url)

            context = {
                "user": associated_user,
                "reset_password_url": reset_password_url,
            }

            body = render_to_string("emails/reset_password.html", context)
            subject = render_to_string("emails/reset_password_subject.txt")
            to_email = associated_user.email
            from_email = settings.EMAIL_HOST_USER

            message = EmailMessage(subject, body, from_email, [to_email,])
            message.content_subtype = "html"
            message.send()

            return JsonResponse({
                "status": True,
                "message": "If you have an account associated with this email address, you will receive a password reset email. Please check your inbox."
            })


class PasswordResetConfirmView(DjangoPasswordResetConfirmView):
    success_url = reverse_lazy("user_management:login")
    template_name = "confirm_reset_password.html"

    def post(self, request, *args, **kwargs):
        User = get_user_model()
        user = User.objects.filter(email = kwargs.get('email')).first()
        if user:
            user.set_password(request.POST.get('password'))
            user.save()
            return JsonResponse({"status":200,"message":"Password has been changed successfully"})
        else:
            return JsonResponse({"status":400,"message":"User doesn't exist"})