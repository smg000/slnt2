import datetime
from django.shortcuts import render
from django.template import loader
from .models import Issue, Article
from .forms import ContactForm, SignUpForm
from django.core.mail import send_mail, BadHeaderError
import sendgrid
import os

def index(request):
    issues = Issue.objects.filter(display=True).order_by('order')
    articles = Article.objects.filter(display=True, issue__in=issues)
    context = {
        'issues': issues,
        'articles': articles,
        'date': datetime.date.today(),
        'form': SignUpForm,
        'prettyDate': datetime.date.today().strftime("%B %d, %Y"),
    }
    # Subscription form
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                data = [
                    {
                        "email": email,
                    }
                ]
                response = sg.client.contactdb.recipients.post(request_body=data)
                print(response.status_code)
                print(response.body)
                print(response.headers)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            # TODO Add Ajax to send without page reload
            return render(request, 'index.html', context)
    # else:
    #     form = SignUpForm
    return render(request, 'index.html', context)

def issue(request):
    issues = Issue.objects.filter(display=True).order_by('order')
    articles = Article.objects.filter(display=True, issue__in=issues)
    context = {
        'issues': issues,
        'articles': articles,
        'date': datetime.date.today(),
        'url_issue': request.GET.get('issue'),
        'url_date': request.GET.get('date'),
        'issue': Issue.objects.filter(display=True).filter(issue=request.GET.get('issue')),
    }
    return render(request, 'issue.html', context)

def about(request):
    return render(request, 'about.html')

def why(request):
    return render(request, 'why.html')

def contact_form(request):
  to_email = 'hi@theskeww.com'
  if request.method == 'POST':
    form = ContactForm(request.POST)
    if form.is_valid():
      name = form.cleaned_data['name']
      from_email = form.cleaned_data['email']
      message = form.cleaned_data['message']
      try:
        send_mail(
            'Contact Form Email',
            message,
			from_email,
            [to_email,],
            fail_silently = False,
            )
      except BadHeaderError:
        return HttpResponse('Invalid header found.')
      return render(request, 'thank-you.html')
  else:
    form = ContactForm
  return render(request, 'contact.html', {'form': form})

def contact_form_thank_you(request):
  return HttpResponse('Thank you!')
  return render(request, 'thank-you.html')

def thankyou(request):
    return render(request, 'thank-you.html')

def privacy_policy(request):
    return render(request, 'privacy-policy.html')

def terms_of_service(request):
    return render(request, 'terms-of-service.html')

""" UNUSED AND/OR FUTURE VIEWS """

def index_test(request):
    issues = Issue.objects.filter(display=True)
    articles = Article.objects.filter(display=True, issue__in=issues)
    context = {
        'issues': issues,
        'articles': articles,
    }
    return render(request, 'index_test.html', context)

def daily_email(request):
    issues = Issue.objects.filter(display=True).order_by('order')
    articles = Article.objects.filter(display=True, issue__in=issues)
    context = {
        'issues': issues,
        'articles': articles,
        'date': datetime.date.today(),
    }
    return render(request, 'daily-email.html', context)

def rate(request):
    issues = Issue.objects.filter(display=True)
    articles = Article.objects.filter(display=True, issue__in=issues)
    context = {
        'issues': issues,
        'articles': articles,
    }
    return render(request, 'rate.html', context)