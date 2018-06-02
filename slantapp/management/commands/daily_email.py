import datetime
import json
import os
from django.core.mail import BadHeaderError, get_connection, EmailMessage, EmailMultiAlternatives, send_mail
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string
from slantapp.models import Issue, Article
from mailchimp3 import MailChimp
import sendgrid
from sendgrid.helpers.mail import *


class Command(BaseCommand):
    help = 'Sends daily email to MailChimp subscribers.'

    def add_arguments(self, parser):
        # parser.add_argument('--subject', type=str, required=True)
        pass

    def handle(self, *args, **options):
        # Pull data from database
        issues = Issue.objects.filter(display=True).order_by('order')
        articles = Article.objects.filter(display=True, issue__in=issues)

        # Create email variables
        subject = "the daily skeww | " + datetime.date.today().strftime("%B %d, %Y")
        from_email = Email('hi@theskeww.com', "Sean and Keal @ the skeww")
        message_txt = render_to_string(
            'daily-email.txt',
            {
                'issues': issues,
                'articles': articles,
                'date': datetime.date.today()
            }
        )
        message_html = render_to_string(
            'daily-email.html',
            {
                'issues': issues,
                'articles': articles,
                'date': datetime.date.today()
            }
        )

        # Get email addresses from MailChimp
        mailchimp_user = os.environ.get('MAILCHIMP_USER')
        mailchimp_api = os.environ.get('MAILCHIMP_API')
        client = MailChimp(
            mc_api=mailchimp_api,
            mc_user=mailchimp_user
        )
        email_dictionary = client.lists.members.all(
            '797ef6d1dc',
            get_all=True,
            fields="members.email_address"
        )
        email_list = []
        for item in email_dictionary['members']:
            email_list.append(item['email_address'])

        # Split list into sublists
        list_max = 999
        email_sublists = [email_list[i * list_max:(i + 1) * list_max] for i in range((len(email_list) + list_max - 1) // list_max)]

        for sublist in email_sublists:

            # using SendGrid's Python Library
            # https://github.com/sendgrid/sendgrid-python

            mail = Mail()

            for to_email in sublist:
                personalization = Personalization()
                personalization.add_to(Email(to_email))
                mail.add_personalization(personalization)

            mail.from_email = from_email
            mail.subject = subject
            mail.add_content(Content('text/plain', message_txt))
            mail.add_content(Content('text/html', message_html))

            sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
            response = sg.client.mail.send.post(request_body=mail.get())

            # Print response codes
            print(response.status_code)
            print(response.body)
            print(response.headers)

        self.stdout.write(self.style.SUCCESS('Sent email!'))