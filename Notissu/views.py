# -*- coding: utf-8 -*-
import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from Notissu.models import Keyword
from Notissu.models import Notice
from Notissu.models import NoticeFiles
from Notissu.models import User

RETURN_COUNT = 15

CATEGORY_LIST = {
    'all': '전체',
    'student': '학사',
    'scholarship': '장학',
    'global': '국제교류',
    'foreign': '외국인유학생',
    'recruit': '모집·채용',
    'inner': '교내행사',
    'outer': '교외행사',
    'volunteer': '봉사',
    'library': '도서관',
}


def get_list(request, category, page):
    is_contain = 0
    for key, value in CATEGORY_LIST.items():
        if category == key:
            is_contain = 1
            break
    if is_contain == 0:
        return wrong_request()

    if category == 'all':
        db_notice_list = Notice.objects.all()
    else:
        db_notice_list = Notice.objects.filter(category=CATEGORY_LIST[category])

    return get_notice_list_return(db_notice_list, page)


def search_list(request, keyword, page):
    db_notice_list = Notice.objects.filter(title__contains=keyword)

    return get_notice_list_return(db_notice_list, page)


def get_notice_list_return(db_notice_list, page):
    page = int(page)
    start_index = (page - 1) * RETURN_COUNT
    end_index = start_index + RETURN_COUNT
    db_notice_list = db_notice_list.order_by('-date')[
                     start_index:end_index].values()
    if db_notice_list.count() <= 0:
        return wrong_request()
    return_list = []
    for dict in db_notice_list:
        del dict['contents']
        del dict['category']
        return_list.append(dict)
    return response_json(return_list)


def get_view(request, notice_id):
    notice = Notice.objects.filter(id=notice_id).values()
    if notice.count() <= 0:
        return wrong_request()

    notice = notice[0]

    db_notice_files_list = NoticeFiles.objects.filter(notice_id=notice_id).values()

    attached_file_list = []
    for dict in db_notice_files_list:
        del dict['id']
        del dict['notice_id']
        attached_file_list.append(dict)

    notice.update({'attached_files': attached_file_list})
    notice.update({'notice_id': notice['id']})
    del notice['category']
    del notice['id']

    return response_json(notice)


@csrf_exempt
def keyword(request, token):
    if request.method == 'GET':
        has_user = User.objects.filter(token=token).first()
        if has_user:
            db_keyword_list = Keyword.objects.filter(user_id=has_user.id).values()
            return_list = []
            for dict in db_keyword_list:
                del dict['user_id']
                del dict['id']
                return_list.append(dict)
            return response_json(return_list)
    elif request.method == 'POST':
        if not ('keyword' and 'hash' in request.POST):
            return response_fail()
        keyword = request.POST['keyword']
        hash = request.POST['hash']

        has_token = User.objects.filter(token=token).first()

        if has_token:
            has_keyword = Keyword.objects.filter(user_id=has_token.id, keyword=keyword).first()
            if not has_keyword:
                insert_keyword = Keyword(user_id=has_token.id, keyword=keyword, hash=hash)
                insert_keyword.save()
                return response_add()
    elif request.method == 'DELETE':
        has_user = User.objects.filter(token=token).first()
        if has_user:
            Keyword.objects.filter(user_id=has_user.id).delete()
            return response_delete()

    return response_fail()


@csrf_exempt
def delete_keyword(request, token, keyword):
    if request.method == 'DELETE':
        db_user = User.objects.filter(token=token).first()
        has_keyword = Keyword.objects.filter(user_id=db_user.id, keyword=keyword).first()
        if has_keyword:
            has_keyword.delete()
            return response_delete()

    return response_fail()


@csrf_exempt
def set_token(request):
    if request.method == 'POST':
        if not ('token' in request.POST):
            return response_fail()
        token = request.POST['token']
        has_token = User.objects.filter(token=token).first()
        if not has_token:
            insert_token = User(token=token)
            insert_token.save()
            return response_add()
        else:
            return response_update()

    return response_fail()


@csrf_exempt
def delete_token(request, token):
    if request.method == 'DELETE':
        has_token = User.objects.filter(token=token).first()
        if has_token:
            has_token.delete()
            return response_delete()
    return response_fail()


def response_json(dict):
    return_json = json.dumps(dict, ensure_ascii=False)
    return HttpResponse(return_json, content_type='application/json')


def response_add():
    return response_crud("ADD")


def response_fail():
    return response_crud("FAIL")


def response_update():
    return response_crud("UPDATE")


def response_delete():
    return response_crud("DELETE")


def response_crud(message):
    return_value_json = json.dumps({"result": message}, ensure_ascii=False)
    return HttpResponse(return_value_json, content_type='application/json')


def wrong_request():
    return HttpResponse("{}", content_type='application/json')
