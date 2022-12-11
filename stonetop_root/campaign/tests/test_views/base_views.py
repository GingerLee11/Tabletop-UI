from django.test import TestCase
from django.urls import reverse, resolve
from django.http import HttpRequest
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import models


from campaign.tests.base import BaseTestClass


class BaseViewsTestClass(BaseTestClass):
    def login_user(self, user):
        self.client.force_login(user, settings.AUTHENTICATION_BACKENDS[0])

    def set_campaign_session_data(self, campaign):
        session = self.client.session
        session['current_campaign_id'] = campaign.pk
        session['current_campaign_name'] = campaign.name
        session.save()

    def convert_data_to_foreign_keys(self, data):
        for k, o in data.items():
            if isinstance(o, models.query.QuerySet):
                o = list(o)
                o = [i.pk for i in o]
                data[k] = o
        return data
