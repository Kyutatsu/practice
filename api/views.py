import json
from collections import OrderedDict
from django.http import HttpResponse
from cms.models import Book, Impression


def render_json_response(request, data, status=None):
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    callback = request.GET.get('callback')
    if not callback:
        callback = request.POST.get('callback')
    if callback:
        # これ何が起こるんや...??? url(json)ってなんや...??-->> これがjsのAjaxで使うやつらしい。
        json_str = "%s(%s)" % (callback, json_str)
        response = HttpResponse(json_str, content_type='application/javascript; charset=UTF-8', status=status)
    # こっちはわかる。
    else:
        response = HttpResponse(json_str, content_type='application/json; charset=UTF-8', status=status)
    return response


def book_list(request):
    books = []
    for book in Book.objects.all().order_by('id'):
        impressions = []
        # ↓でQuerySet取れる。Impression.objects.filter(book_id=book.id)とせんでええんやな。
        for impression in book.impressions.order_by('id'):
            temp_impression_info_dict = OrderedDict([
                ('id', impression.id),
                ('comment', impression.comment),
            ])
            impressions.append(temp_impression_info_dict)
        temp_book_info_dict = OrderedDict([
            ('id', book.id),
            ('name', book.name),
            ('publisher', book.publisher),
            ('page', book.page),
            ('impressions', impressions),
        ])
        books.append(temp_book_info_dict)
    data = OrderedDict([('books', books)])
    return render_json_response(request, data)
