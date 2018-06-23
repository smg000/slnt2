import datetime
from urllib.parse import unquote
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.template import loader
from django.utils.text import slugify
from .models import Issue, Article
from .forms import ContactForm, SignUpForm
from django.core.mail import send_mail, BadHeaderError
import sendgrid
import os

#TODO Encapsulate subscription form; kwargs = page to render, e.g., index.html

def index(request):
    navbar_issues = Issue.objects.filter(display=True).order_by('order')
    def issues():
        date = datetime.date.today()
        if date.weekday() < 5:
            issues = Issue.objects.filter(display=True).order_by('order')
        else:
            issues = Issue.objects.filter(display=True).order_by('weekend_order')
        return issues
    articles = Article.objects.filter(display=True, issue__in=issues())
    def pretty_date():
        date = datetime.date.today()
        if date.weekday() < 5:
            return datetime.date.today().strftime("%A, %B %d, %Y")
        else:
            return "Week in Review:"
    def weekend_dates():
        date = datetime.date.today()
        if date.weekday() < 5:
            pass
        elif date.weekday() == 5:
            monday = date - datetime.timedelta(days=5)
            friday = date - datetime.timedelta(days=1)
            return monday.strftime("%A, %B %d, %Y") + " to " + friday.strftime("%A, %B %d, %Y")
        else:  # Weekday == 6
            monday = date - datetime.timedelta(days=6)
            friday = date - datetime.timedelta(days=2)
            return monday.strftime("%A, %B %d, %Y") + " to " + friday.strftime("%A, %B %d, %Y")
    context = {
        'navbar_issues': navbar_issues,
        'issues': issues(),
        'articles': articles,
        'date': datetime.date.today(),
        'form': SignUpForm,
        'prettyDate': pretty_date(),
        'weekendDates': weekend_dates(),
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

#TODO Figure out a better way to do this without violating DRY; only change is stage=True
def stage(request):
    navbar_issues = Issue.objects.filter(stage=True).order_by('order')
    issues = Issue.objects.filter(stage=True).order_by('order')
    articles = Article.objects.filter(display=True, issue__in=issues)
    context = {
        'navbar_issues': navbar_issues,
        'issues': issues,
        'articles': articles,
        'date': datetime.date.today(),
        'form': SignUpForm,
        'prettyDate': datetime.date.today().strftime("%A, %B %d, %Y"),
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

def issue(request, issue, year, month, day):
    navbar_issues = Issue.objects.filter(display=True).order_by('order')
    issues = Issue.objects.order_by('order')

    def get_issue():
        for iss in Issue.objects.order_by('order'):
            if slugify(iss.issue) == issue and iss.date == datetime.date(year, month, day):
                return iss
                break
        else:
            raise Http404("No MyModel matches the given query.")



    articles = Article.objects.filter(display=True, issue__in=issues)
    context = {
        'navbar_issues': navbar_issues,
        'issues': issues, # All issues objects
        'issue': get_issue(),  # The specific issue that matches name and date; unique
        'articles': articles,
        'year': year,
        'month': month,
        'day': day,
    }
    return render(request, 'issue.html', context)

def archive(request):
    navbar_issues = Issue.objects.filter(display=True).order_by('order')
    issues = Issue.objects.order_by('order')
    def create_date_list():
        date_list = []
        dates = [datetime.date.today() + datetime.timedelta(days=i) for i in range(-11, 0)] # Last 7 days will always include last 5 weekdays
        for date in dates:
            if date.weekday() < 5: # Limit to weekdays; Saturday = 5, Sunday = 6
                date_list.append(date)
        date_list.sort(reverse=True)
        #TODO Increase daily until archive list is built
        return date_list[:10] # Display last 10 weekdays
    def create_date_issue_dictionary():
        date_issue_dictionary = {}
        date_list = create_date_list()
        for date in date_list:
            date_issue_dictionary[date] = Issue.objects.filter(date=date).order_by('order')
        return date_issue_dictionary
    context = {
        'navbar_issues': navbar_issues,
        'articles': Article.objects.filter(display=True, issue__in=issues),
        'date_issue_dictionary': create_date_issue_dictionary(),
        'archive_dates': create_date_list(),
    }
    return render(request, 'archive.html', context)

def archive_result(request, year, month, day):
    navbar_issues = Issue.objects.filter(display=True).order_by('order')
    issues = Issue.objects.filter(date=datetime.date(year, month, day)).order_by('order')
    articles = Article.objects.filter(display=True, issue__in=issues)
    context = {
        'navbar_issues': navbar_issues,
        'issues': issues,
        'articles': articles,
        'date': datetime.date.today(),
        'form': SignUpForm,
        'prettyDate': datetime.date(year, month, day).strftime("%A, %B %d, %Y"),
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
            return render(request, 'archive_result.html', context)
    # else:
    #     form = SignUpForm
    return render(request, 'archive_result.html', context)

def about(request):
    navbar_issues = Issue.objects.filter(display=True).order_by('order')
    context ={
        'navbar_issues': navbar_issues,
    }
    return render(request, 'about.html', context)

def contact_form(request):
    navbar_issues = Issue.objects.filter(display=True).order_by('order')
    to_email = 'hi@theskeww.com'
    context = {
        'navbar_issues': navbar_issues,
    }
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
                    [to_email, ],
                    fail_silently=False,
                )
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return render(request, 'thank-you.html', context)
    else:
        form = ContactForm
        context = {
            'navbar_issues': navbar_issues,
            'form': form,
        }
    return render(request, 'contact.html', context)

def contact_form_thank_you(request):
    navbar_issues = Issue.objects.filter(display=True).order_by('order')
    context = {
      'navbar_issues': navbar_issues,
    }
    return HttpResponse('Thank you!')
    return render(request, 'thank-you.html', context)

def thankyou(request):
    navbar_issues = Issue.objects.filter(display=True).order_by('order')
    context = {
        'navbar_issues': navbar_issues,
    }
    return render(request, 'thank-you.html', context)

def privacy_policy(request):
    navbar_issues = Issue.objects.filter(display=True).order_by('order')
    context = {
        'navbar_issues': navbar_issues,
    }
    return render(request, 'privacy-policy.html', context)

def terms_of_service(request):
    navbar_issues = Issue.objects.filter(display=True).order_by('order')
    context = {
        'navbar_issues': navbar_issues,
    }
    return render(request, 'terms-of-service.html', context)

""" FUTURE VIEWS """

def daily_email(request):
    issues = Issue.objects.filter(display=True).order_by('order')
    articles = Article.objects.filter(display=True, issue__in=issues)
    context = {
        'issues': issues,
        'articles': articles,
        'date': datetime.date.today(),
    }
    return render(request, 'daily-email.html', context)