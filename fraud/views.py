from django.views.generic.base import RedirectView
from otree.models import Session


class UnblockView(RedirectView):
    url_pattern = 'unlock/<str:code>'
    url_name = 'unlock_session'
    pattern_name = 'AdminReport'

    def get_redirect_url(self, *args, **kwargs):
        try:
            session = Session.objects.get(code=kwargs.get('code'))
            lock_value = not session.vars.get('locked', True)
            session.fraud_subsession.all().update(lock=lock_value)
            session.vars['locked'] = lock_value
            session.save()
            return super().get_redirect_url(*args, **kwargs)
        except Session.DoesNotExist:
            return '/'
