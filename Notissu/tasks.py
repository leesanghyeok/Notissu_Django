import requests
from bs4 import BeautifulSoup
from celery import shared_task
from pyfcm import FCMNotification

from Notissu.models import Keyword
from Notissu.models import Notice
from Notissu.models import NoticeFiles

AUTHORIZATION_KEY = "AIzaSyBy0Nmcs_KeG00yJ2z1TpH3D1LlUQO5mpo"
NOTICE_LIST_URL = "http://m.ssu.ac.kr/html/themes/m/html/notice_univ_list.jsp?sCategory=%s&curPage=%d"
LIBRARY_LIST_URL = "http://oasis.ssu.ac.kr/bbs/Bbs.ax?bbsID=1&pageSize=10&page=%d"
NOTICE_VIEW_URL = "http://m.ssu.ac.kr/html/themes/m/html/notice_univ_view.jsp?messageId=%s&sCategory=%s"
LIBRARY_VIEW_URL = "https://oasis.ssu.ac.kr/bbs/Detail.ax?bbsID=1&articleID=%s"
FIREBASE_MESSAGE_SEND_URL = "https://fcm.googleapis.com/fcm/send"
API_KEY = "AAAAKni3MTU:APA91bFv18y_shYTMxmKi8YZ1Rc2FLm8FolnWkb6PKoO2pLleh7fM343m3gCd5BfPy-b3mzwzvUvUwfoxnrQp-D83wYHi-BwQcj2V2dJsWYO71ROmBmpjhuKAZT6fe7paLbyDPPQK1U9"


@shared_task
def crawling_push():
    keyword_list = get_keyword()
    category = ['도서관', '학사', '장학', '국제교류', '외국인유학생', '모집·채용', '교내행사', '교외행사', '봉사']
    notice_list = fetch_notice(category, 1, 1)
    unduplicated_list = check_duplicate(notice_list)
    contain_keyword = get_contain_keyword(unduplicated_list, keyword_list)
    push_message(contain_keyword)
    insert_notice(unduplicated_list)
    for notice, files in unduplicated_list:
        print(notice.title)
    return "ok"


def get_keyword():
    return_keyword_list = []
    db_keyword_list = Keyword.objects.all().values()
    for dict in db_keyword_list:
        del dict['id']
        del dict['user_id']
        return_keyword_list.append(dict)

    return return_keyword_list


def get_contain_keyword(unduplicated_list, keyword_list):
    return_keyword_list = []
    for notice, files in unduplicated_list:
        for keyword_dict in keyword_list:
            keyword = keyword_dict['keyword']
            if notice.title.find(keyword) != -1:
                is_contain = False
                for return_keyword in return_keyword_list:
                    if keyword == return_keyword['keyword']:
                        is_contain = True
                        break
                if not is_contain:
                    return_keyword_list.append(keyword_dict)

    return return_keyword_list


def push_message(contain_keyword):
    push_service = FCMNotification(api_key=API_KEY)
    for keyword_dict in contain_keyword:
        hash = keyword_dict['hash']
        push_service.notify_topic_subscribers(message_body="구독한 공지사항이 올라왔습니다.", topic_name=hash)


def get_notice_id(tag, start_delimiter, end_delimiter):
    tag_a = tag.find('a')
    str_tag_a = str(tag_a)
    start_index = str_tag_a.find(start_delimiter)
    end_index = str_tag_a.find(end_delimiter)
    if end_index == -1 or start_index == -1:
        return
    return str_tag_a[start_index + len(start_delimiter):end_index]


def get_contents(soup, tag_name, tag_class, replace_old, replace_new):
    contents = soup.find(tag_name, class_=tag_class)
    return str(contents).replace(replace_old, replace_new)


def get_files_url(base_url, file_data):
    string_file_data = str(file_data)
    start_index = string_file_data.find("href=\"") + len("href=\"")
    end_index = string_file_data.find("\">")
    return base_url + string_file_data[start_index:end_index].replace("&amp;", "&")


def get_file_list(soup, notice_id, tag_name, tag_class, base_url):
    file_list = []
    file_tag = soup.find(tag_name, class_=tag_class)
    if file_tag != None:
        for file_data in file_tag.find_all('a'):
            title = file_data.string
            url = get_files_url(base_url, file_data)
            file = NoticeFiles(title=title, url=url)
            file_list.append(file)
    return file_list


def from_library(tag):
    notice_id = get_notice_id(tag, "articleID=", "&amp;currentPage")
    if notice_id == None: return

    title = tag.find('a').contents[0]
    date = tag.find('td', headers="listDate").contents[0]
    category = "도서관"

    request_url = LIBRARY_VIEW_URL % (notice_id)
    soup = BeautifulSoup(requests.get(request_url).content, "html.parser")
    contents = get_contents(soup, "div", "xed", 'src="/Image.file', 'src="https://oasis.ssu.ac.kr/Image.file')

    notice = Notice(notice_id=notice_id, title=title, date=date, category=category, contents=contents)

    file_list = get_file_list(soup, notice_id, 'div', 'boredattach', "https://oasis.ssu.ac.kr")

    return notice, file_list


def from_notice(tag, category):
    notice_id = get_notice_id(tag, "messageId=", "&amp;curPage=")
    category = category
    title = tag.find('a').contents[0]
    date = tag.find('span').contents[0]

    request_url = NOTICE_VIEW_URL % (notice_id, category)
    soup = BeautifulSoup(requests.get(request_url).content, "html.parser")
    contents = get_contents(soup, "div", "contents", '/portlet-repositories', 'http://m.ssu.ac.kr/portlet-repositories')

    notice = Notice(notice_id=notice_id, title=title, date=date, category=category, contents=contents)

    file_list = get_file_list(soup, notice_id, 'div', 'file', "http://m.ssu.ac.kr")

    return notice, file_list


def fetch_notice(category_list, start_page, end_page):
    notice_list = []
    for category in category_list:
        for page in range(start_page, end_page + 1):
            if category == "도서관":
                request_url = LIBRARY_LIST_URL % (page)
                list_response = requests.get(request_url)
                soup = BeautifulSoup(list_response.content, "html.parser")
                tag_list = soup.find_all('tr')[1:]
                for tag in tag_list:
                    notice = from_library(tag)
                    notice_list.append(notice)
            else:
                request_url = NOTICE_LIST_URL % (category, page)
                list_response = requests.get(request_url)
                soup = BeautifulSoup(list_response.content, "html.parser")
                tag_list = soup.find_all('li', class_='first-child')

                for tag in tag_list:
                    notice = from_notice(tag, category)
                    notice_list.append(notice)

    return notice_list


def insert_notice(unduplicated_list):
    for notice, files in unduplicated_list:
        notice.save()
        for file in files:
            file.save()
            notice.noticefiles_set.add(file)


def check_duplicate(notice_list):
    return_list = []
    for index in range(len(notice_list)):
        if notice_list[index] == None:
            continue

        if is_duplicate(notice_list[index][0].notice_id):
            pass
        else:
            return_list.append(notice_list[index])
    return return_list


def is_duplicate(id):
    result = Notice.objects.filter(notice_id=id)
    if len(result) > 0:
        return 1
    else:
        return 0

# def get_keyword():
#     request_header = {"Authorization": "key=" + AUTHORIZATION_KEY}
#     print list_response.content
