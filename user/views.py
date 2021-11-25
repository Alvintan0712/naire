from django.contrib import auth
from django.core.exceptions import BadRequest
from django.http import HttpResponse
from django.views.decorators.http import require_safe

from common.errors import ERR_DUPL_USERNAME, ERR_DUPL_EMAIL
from common.log import logger
from common.rest import rest_ok, rest_fail, acquire_json, rest_data, rest
from common.types import ensure_str
from .models import User


@require_safe
def hello(request):
    logger.info(f'hello to {request.user}')
    if request.user.is_authenticated:
        return HttpResponse(f'Hello, {request.user.username}?')
    return HttpResponse('Hello, world!')


@require_safe
def info(request):
    if request.user.is_authenticated:
        return rest_data(request.user.info())
    return rest_fail()


@acquire_json
def login(request, data):
    username = ensure_str(data['username_or_email'])  # TODO: handle emails
    password = ensure_str(data['password'])
    user = auth.authenticate(request, username=username, password=password)
    if user is None:
        return rest_fail()
    auth.login(request, user)
    logger.info(f'Logged: {user}')
    return rest_data(user.info())


@require_safe
def logout(request):
    auth.logout(request)
    return rest_ok()


@acquire_json
def register(request, data):
    username = ensure_str(data['username'])
    email = ensure_str(data['email']).lower()
    password = ensure_str(data['password'])
    dname = ensure_str(data['dname'])
    if User.objects.filter(username=username).exists():
        return rest(ERR_DUPL_USERNAME)
    if User.objects.filter(email=email).exists():
        return rest(ERR_DUPL_EMAIL)
    try:
        user = User.objects.create_user(username=username, password=password, email=email, dname=dname)
    except Exception as e:
        # Shouldn't be reached from our validating frontend
        logger.warning(f'Bad request caused {type(e).__name__} {e}')
        raise BadRequest
    logger.info(f'Registered: {user}')
    return rest_data(user.info())
