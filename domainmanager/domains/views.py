from multiprocessing import context
from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User, Account, Domain
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.urls import reverse, reverse_lazy
import string
import random
import dns.resolver
import ast


class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        context = {}
        user = User.objects.filter(pk=request.user.id).first()
        associated_domains = Domain.objects.filter(account=user.account).exclude(status='4')
        domains=[]
        for domain in associated_domains:
            domains.append(domain)

        context.update({
            'domains': domains
        })

        return render(request, "dashboard.html", context)


class AddDomainsView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "add_domain.html")

    def post(self, request):
        domain_name = request.POST.get('domain_name')
        user = User.objects.filter(pk=request.user.id).first()
        source_prefix = '_' + id_generator()
        domains_count = Domain.objects.filter(account=user.account).exclude(status='4').count()

        if domains_count >= user.account.domain_cap:
            return JsonResponse({
                "status": False,
                "status_code": 301,
                "message": "Domain cap exceeds! You can't add more domains."
            })

        domain = Domain.objects.create(
            domain_name=domain_name,
            source_prefix=source_prefix.lower(),
            account=user.account
        )
        spf_domain = domain.source_prefix + "." + domain.domain_name
        return JsonResponse({
            "status": True,
            "status_code": 200,
            "message": "Domain added successfully.",
            "domain": spf_domain,
            "domain_name": domain.domain_name,
            "source_prefix": domain.source_prefix,
        })


class VerifyDomainView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, "domain_verify.html")

    def post(self, request, *args, **kwargs):
        is_verify_page = request.POST.get('is_verify_page')
        is_spf = False
        if is_verify_page == 'True':
            domain_to_verify = request.POST.get('domain_to_verify') 
            domain_prefix = domain_to_verify.split('.')[0]
            associated_domain = Domain.objects.filter(source_prefix=domain_prefix).first()
            try:
                result = dns.resolver.resolve(domain_to_verify, 'TXT')
                for val in result:
                    if ast.literal_eval(val.to_text()).startswith("v=spf1"):
                        is_spf = True
                        break

                if is_spf == True:
                    associated_domain.update(status='2') # status=2 is verified
                    return JsonResponse({
                        "status": True,
                        "message": "Domain Verified"
                    })
                else:
                    return JsonResponse({
                        "status": True,
                        "message": "Domain is not verified"
                    })
            except:
                return JsonResponse({
                    "status": False,
                    "message": "The DNS query name does not exist"
                })
        else:
            domain_id = request.POST.get('domain_id')
            domain = Domain.objects.filter(domain_id=domain_id)
            prefix_domain = domain[0].source_prefix + '.' + domain[0].domain_name
            try:
                result = dns.resolver.resolve(prefix_domain, 'TXT')
                for val in result:
                    if ast.literal_eval(val.to_text()).startswith("v=spf1"):
                        is_spf = True
                        break

                if is_spf == True:
                    domain.update(status='2') # status=2 is verified
                    return JsonResponse({
                        "status": True,
                        "message": "Domain Verified"
                    })
                else:
                    return JsonResponse({
                        "status": True,
                        "message": "Domain is not verified"
                    })
            except:
                return JsonResponse({
                    "status": False,
                    "message": "The DNS query name does not exist"
                })


class DeleteDomainsView(LoginRequiredMixin, View):
    def post(self, request):
        is_disable = request.POST.get('is_disable')
        is_enable = request.POST.get('is_enable')
        domain_id = request.POST.get('domain_id')

        if is_disable == 'True':
            try:
                domain = Domain.objects.filter(domain_id=domain_id)
                domain.update(status='3')
                return JsonResponse({
                    "status": True,
                    "message": "Domain disabled!"
                })
            except:
                return JsonResponse({
                    "status": False,
                    "message": "Something went wrong!"
                })
        elif is_enable == 'True':
            try:
                domain = Domain.objects.filter(domain_id=domain_id)
                domain.update(status='5')
                return JsonResponse({
                    "status": True,
                    "message": "Domain Enabled successfully!"
                })
            except:
                return JsonResponse({
                    "status": False,
                    "message": "Something went wrong!"
                })
        else:
            try:
                domain = Domain.objects.filter(domain_id=domain_id)
                domain.update(status='4')
                return JsonResponse({
                    "status": True,
                    "message": "Domain deleted successfully"
                })
            except:
                return JsonResponse({
                    "status": False,
                    "message": "Something went wrong!"
                })



############################################################
#################### PRIVATE FUNCTIONS #####################
############################################################

# Function to generate 7 digits random string
def id_generator(size=7, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))