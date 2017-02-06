# -*- coding: utf-8 -*-
import json

from django.http import HttpResponse

from Notissu.models import Notice

RETURN_COUNT = 7

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
}


def get_list(request, category, page):
    is_contain = 0
    for key, value in CATEGORY_LIST.iteritems():
        if category == key:
            is_contain = 1
            continue
    if is_contain == 0:
        return wrong_request()

    page = int(page)
    start_index = (page - 1) * RETURN_COUNT
    end_index = start_index + RETURN_COUNT

    db_notice_list = Notice.objects.filter(category=CATEGORY_LIST[category]).order_by('-date')[
                     start_index:end_index].values()
    if db_notice_list.count() <= 0:
        return wrong_request()

    return_list = []
    for dict in db_notice_list:
        del dict['contents']
        del dict['category']
        return_list.append(dict)

    return_list_json = json.dumps(return_list, ensure_ascii=False)

    return HttpResponse(return_list_json, content_type='application/json')


def get_view(request, notice_id):
    return HttpResponse("view " + notice_id, content_type='application/json')


def wrong_request():
    return HttpResponse("{}", content_type='application/json')
