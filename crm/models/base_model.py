from django.db import models
import threading

from crm.models.User import User


_thread_local = threading.local()


def get_current_user():
    return getattr(_thread_local, 'user', None)


class ThreadLocalsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _thread_local.user = request.user
        response = self.get_response(request)
        return response


class BaseModel(models.Model):
    created_date = models.DateTimeField(
        verbose_name='Created date', auto_created=True, blank=True, null=True)
    updated_date = models.DateTimeField(
        verbose_name='Updated date', auto_created=True, blank=True, null=True)

    created_by = models.ForeignKey(to=User, on_delete=models.SET_NULL, blank=True,
                                   default=None, null=True, related_name='%(class)s_created_by', editable=False)
    updated_by = models.ForeignKey(to=User, on_delete=models.SET_NULL, blank=True,
                                   default=None, null=True, related_name='%(class)s_updated_by', editable=False)

    class Meta:
        abstract = True