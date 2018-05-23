import datetime
from django.core.mail import send_mail, BadHeaderError
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string
from slantapp.models import Issue, Article

# from mailchimp3 import MailChimp


# Get email addresses from MailChimp
# client = MailChimp(mc_api='YOUR_API_KEY', mc_user='YOUR_USERNAME')
# return the first 100 member's email addresses for the list with id 123456
# client.lists.members.all('123456', count=100, offset=0, fields="members.email_address")

class Command(BaseCommand):
    help = 'Sends daily email to MailChimp subscribers.'

    def add_arguments(self, parser):
        # parser.add_argument('--subject', type=str, required=True)
        pass

    def handle(self, *args, **options):

        issues = Issue.objects.filter(display=True).order_by('order')
        # TODO Order articles by bias, from left to right
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

        send_mail(
            subject=subject,
            message=message_plain,
            from_email=from_email,
            recipient_list=recipient_list,
            html_message=message_html,
            fail_silently=False,
        )

        self.stdout.write(self.style.SUCCESS('Sent email!'))