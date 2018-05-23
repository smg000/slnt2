import datetime
import os
from django.core.mail import EmailMessage, BadHeaderError, send_mail
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string
# from slantapp.models import Issue, Article
from mailchimp3 import MailChimp


class Command(BaseCommand):
    help = 'Sends daily email to MailChimp subscribers.'

    # Get email addresses from MailChimp
    mailchimp_user = os.environ.get('MAILCHIMP_USER')
    mailchimp_api = os.environ.get('MAILCHIMP_API')
    client = MailChimp(mc_api=mailchimp_api, mc_user=mailchimp_user)
    email_dictionary = client.lists.members.all('797ef6d1dc', get_all=True, fields="members.email_address")
    email_list = []
    for item in email_dictionary['members']:
        email_list.append(item['email_address'])

    def add_arguments(self, parser):
        # parser.add_argument('--subject', type=str, required=True)
        pass

    def handle(self, *args, **options):
        issues = Issue.objects.filter(display=True).order_by('order')
        articles = Article.objects.filter(display=True, issue__in=issues)

        message_plain = render_to_string(
            'email.txt',
            {'issues': issues, 'articles': articles, 'date': datetime.date.today()}
        )
        message_html = render_to_string(
            'daily-email.html',
            {'issues': issues, 'articles': articles, 'date': datetime.date.today()}
        )

        subject = "the daily skeww | " + datetime.date.today().strftime("%B %d, %Y")
        # subject = options['subject']
        message = 'Hi.'
        from_email = 'Sean @ the skeww <hi@theskeww.com>'
        bcc = ['sean.graber@gmail.com', 'sean.m.graber.tu18@tuck.dartmouth.edu']
        # to_email = 'sean.graber@gmail.com'
        # to_email = 'sean.m.graber.tu18@tuck.dartmouth.edu'
        # to_email = 'eleanortansey@gmail.com'

        email = EmailMessage(
            subject="the daily skeww | " + datetime.date.today().strftime("%B %d, %Y"),
            body=message_plain,
            from_email='Sean @ the skeww <hi@theskeww.com>',
            to='Sean @ the skeww <hi@theskeww.com>',
            bcc=email_list,
            message_html=
        )



        send_mail(
            subject=subject,
            message=message_plain,
            from_email=from_email,
            recipient_list=recipient_list,
            html_message=message_html,
            fail_silently=False,
        )

        self.stdout.write(self.style.SUCCESS('Sent email!'))