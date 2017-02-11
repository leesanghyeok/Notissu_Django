# -*- coding: utf-8 -*-
import json

from django.http import HttpResponse

from Notissu.models import Notice
from Notissu.models import NoticeFiles

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
    'library': '도서관',
}


def get_list(request, category, page):
    is_contain = 0
    for key, value in CATEGORY_LIST.iteritems():
        if category == key:
            is_contain = 1
            break
    if is_contain == 0:
        return wrong_request()

    page = int(page)
    start_index = (page - 1) * RETURN_COUNT
    end_index = start_index + RETURN_COUNT

    if category == 'all':
        db_notice_list = Notice.objects.all()
    else:
        db_notice_list = Notice.objects.filter(category=CATEGORY_LIST[category])

    db_notice_list = db_notice_list.order_by('-date')[
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
    notice = Notice.objects.filter(notice_id=notice_id).values()
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

    return_json = json.dumps(notice, ensure_ascii=False)

    return HttpResponse(return_json, content_type='application/json')


def wrong_request():
    return HttpResponse("{}", content_type='application/json')
