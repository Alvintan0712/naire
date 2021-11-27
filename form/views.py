from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_safe

from common.deco import check_logged_in
from common.models import save_or_400, get_user
from common.rest import rest_data, acquire_json, rest_ok, rest_fail
from common.types import ensure_str, ensure_dict, ensure_int

from .models import Form, Response


def ensure_modifiable(user, form):
    # TODO: form owner 有可能是 Org
    if user != form.owner_user:
        raise PermissionDenied


@require_safe
@check_logged_in
def get_all(request):
    forms = Form.objects.filter(owner_user=request.user)
    return rest_data([dict(f.info(), resp_count=f.response_set.count()) for f in forms])


@check_logged_in
@acquire_json
def create(request, data):
    title = ensure_str(data['title'])
    body = ensure_dict(data['body'])
    form = Form(title=title, body=body, owner_user=request.user)
    save_or_400(form)
    return rest_ok()


@acquire_json
def get_detail(request, data):
    fid = ensure_int(data['fid'])
    try:
        form = Form.objects.get(id=fid)
    except Form.DoesNotExist:
        return rest_fail()

    # TODO: Check (future) permissions.
    #  Maybe we shouldn't distinguish permission denying from nonexistence in the result code for security?

    return rest_data(form.detail())


@acquire_json
def save_resp(request, data):
    fid = ensure_int(data['fid'])
    resp_body = ensure_dict(data['resp_body'])
    # TODO: After we implement Orgs, some member might delete a Form which another is editing.
    form = get_object_or_404(Form, id=fid)
    resp = Response(form=form, body=resp_body, user=get_user(request))
    resp.save()
    return rest_ok()


@check_logged_in
@acquire_json
def save_title(request, data):
    fid = ensure_int(data['fid'])
    title = ensure_str(data['title'])
    form = get_object_or_404(Form, id=fid)
    ensure_modifiable(request.user, form)
    form.title = title
    save_or_400(form)
    return rest_ok()


@check_logged_in
@acquire_json
def change_body(request, data):
    fid = ensure_int(data['fid'])
    body = ensure_dict(data['body'])
    form = get_object_or_404(Form, id=fid)
    ensure_modifiable(request.user, form)
    form.response_set.all().delete()
    form.body = body
    form.save()
    return rest_ok()


@check_logged_in
@acquire_json
def remove(request, data):
    fid = ensure_int(data['fid'])
    form = get_object_or_404(Form, id=fid)
    ensure_modifiable(request.user, form)
    form.delete()
    return rest_ok()


@check_logged_in
@acquire_json
def get_form_resps(request, data):
    fid = ensure_int(data['fid'])
    form = get_object_or_404(Form, id=fid)
    ensure_modifiable(request.user, form)
    return rest_data({
        'form': form.detail(),
        'resps': [r.info() for r in form.response_set.all()]
    })


@check_logged_in
@acquire_json
def get_form_stats(request, data):
    fid = ensure_int(data['fid'])
    form = get_object_or_404(Form, id=fid)
    ensure_modifiable(request.user, form)
    return rest_data({
        'form': form.detail(),
        'resps': [r.detail() for r in form.response_set.all()]
    })


def get_modifiable_resp(request, rid, fid):
    resp = get_object_or_404(Response, id=rid)
    form = resp.form
    if form.id != fid:
        raise Http404  # TODO: can be exploited
    ensure_modifiable(request.user, form)
    return resp, form


@check_logged_in
@acquire_json
def get_resp_detail(request, data):
    fid = ensure_int(data['fid'])
    rid = ensure_int(data['rid'])
    resp, _ = get_modifiable_resp(request, rid, fid)
    return rest_data(resp.detail())


@check_logged_in
@acquire_json
def remove_resp(request, data):
    fid = ensure_int(data['fid'])
    rid = ensure_int(data['rid'])
    resp, _ = get_modifiable_resp(request, rid, fid)
    resp.delete()
    return rest_ok()
