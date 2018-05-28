import datetime
import os
from django.core.mail import BadHeaderError, get_connection, EmailMessage, EmailMultiAlternatives, send_mail
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string
from slantapp.models import Issue, Article
from mailchimp3 import MailChimp


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
        from_email = 'hi@theskeww.com'
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
        list_max = 250
        email_sublists = [email_list[i * list_max:(i + 1) * list_max] for i in range((len(email_list) + list_max - 1) // list_max)]

        for sublist in email_sublists:
            # Get and open connection
            connection = get_connection()
            connection.open()

            # Create email object and attach html content
            email = EmailMultiAlternatives(
                subject,
                message_txt,
                from_email,
                ["hi@theskeww.com"],
                bcc=sublist,
                connection=connection,
            )
            email.attach_alternative(message_html, "text/html")

            # Send email and close connection
            email.send()
            connection.close()









        # subject = options['subject']
        # message = 'Hi.'
        # from_email = 'hi@theskeww.com'
        # bcc = ['sean.graber@gmail.com', 'sean.m.graber.tu18@tuck.dartmouth.edu']
        # to_email = 'sean.graber@gmail.com'
        # # to_email = 'sean.m.graber.tu18@tuck.dartmouth.edu'
        # # to_email = 'eleanortansey@gmail.com'
        #
        # email = EmailMultiAlternatives(
        #     subject="the daily skeww | " + datetime.date.today().strftime("%B %d, %Y"),
        #     body=message_plain,
        #     from_email='hi@theskeww.com',
        #     to=['sean.graber@gmail.com',],
        #     # html_message=message_html,
        #     headers={
        #         'X-SES-CONFIGURATION-SET': 'DailySkewwTracking',
        #         'X-SES-MESSAGE-TAGS': datetime.date.today().strftime("%B %d, %Y"),
        #     },
        # )
        #
        # email.attach_alternative(message_html, "text/html")
        #
        # connection.open()
        # email.send(fail_silently=False)
        # connection.close()


        # subject, from_email, to = 'hello', 'from@example.com', 'to@example.com'
        # text_content = 'This is an important message.'
        # html_content = '<p>This is an <strong>important</strong> message.</p>'
        # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        # msg.attach_alternative(html_content, "text/html")
        # msg.send()


        # send_mail(
        #     subject=subject,
        #     message=message_plain,
        #     from_email=from_email,
        #     recipient_list=['sean.m.graber.tu18@tuck.dartmouth.edu', ],
        #     # recipient_list=recipient_list,
        #     html_message=message_html,
        #     fail_silently=False,
        # )

        # send_mail(
        #     "Hi.",
        #     'Hi.',
        #     'Sean @ the skeww <hi@theskeww.com>',
        #     ['sean.graber@gmail.com', 'sean.m.graber.tu18@tuck.dartmouth.edu'],
        #     # recipient_list=recipient_list,
        #     html_message=message_html,
        #     fail_silently=False,
        #     # headers={'X-SES-CONFIGURATION-SET': Email_Tracking_1},
        #     headers={
        #         'X-SES-CONFIGURATION-SET': 'DailySkewwTracking',
        #         'X-SES-MESSAGE-TAGS': datetime.date.today().strftime("%B %d, %Y"),
        # },
        # )

        self.stdout.write(self.style.SUCCESS('Sent email!'))