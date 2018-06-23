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
    help = 'Sends daily email to SendGrid subscribers.'

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
        to_email = Email('sean.graber@gmail.com')
        # TODO Check message_txt for accuracy
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

        """ MailChimp begins...
        
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
        
        ... and ends """

        # email_list = []
        #
        # sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
        # # Limit of 1000 emails per call
        # for i in range(1, 1000000):
        #     try:
        #         params = {'page': 1, 'page_size': 999, }
        #         response = sg.client.contactdb.recipients.get(query_params=params)
        #         json_response = json.loads(response.body)
        #         for item in json_response['recipients']:
        #             email_list.append(item['email'])
        #     finally:
        #         break
        #
        # print(email_list)

        # Split list into sublists
        # list_max = 999
        # email_sublists = [email_list[i * list_max:(i + 1) * list_max] for i in range((len(email_list) + list_max - 1) // list_max)]
        #
        # for sublist in email_sublists:
        #
        #     # using SendGrid's Python Library
        #     # https://github.com/sendgrid/sendgrid-python

        mail = Mail()

        personalization = Personalization()
        personalization.add_to(to_email)
        mail.add_personalization(personalization)

        mail.from_email = from_email
        mail.subject = subject
        mail.add_content(Content('text/plain', message_txt))
        mail.add_content(Content('text/html', message_html))

        # from_email = from_email
        # subject = subject
        # to_email = Email('sean.graber@gmail.com')
        # content = Content("text/plain", "some text here")
        # mail = Mail(from_email, subject, to_email, content)

        sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
        response = sg.client.mail.send.post(request_body=mail.get())

        # Print response codes
        print(response.status_code)
        print(response.body)
        print(response.headers)

        self.stdout.write(self.style.SUCCESS('Sent email!'))