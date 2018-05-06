import datetime
from django.shortcuts import render
from django.template import loader
from .models import Issue, Article
from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError

def index(request):
    issues = Issue.objects.filter(display=True).order_by('order')
    articles = Article.objects.filter(display=True, issue__in=issues)
    context = {
        'issues': issues,
        'articles': articles,
    }
    return render(request, 'index.html', context)

def index_test(request):
    issues = Issue.objects.filter(display=True)
    articles = Article.objects.filter(display=True, issue__in=issues)
    context = {
        'issues': issues,
        'articles': articles,
    }
    return render(request, 'index_test.html', context)

def why(request):
    return render(request, 'why.html')

def contact_form(request):
  to_email = 'sean.graber@gmail.com'
  if request.method == 'POST':
    form = ContactForm(request.POST)
    if form.is_valid():
      name = form.cleaned_data['name']
      from_email = form.cleaned_data['email']
      message = form.cleaned_data['message']
      try:
        send_mail(
            'Email from THE SLNT',
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