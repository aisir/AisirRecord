from django.shortcuts import render


from Main.core import grab_article, similar_article, relate_news
from Main.models import Record, Tag, Evaluate
import logging
logger = logging.getLogger(__name__) # 这里用__name__通用,自动检测.


# Create your views here.
def index(request):
    hotrecords = Record.objects.all().order_by('-likenum')[:5]
    newrecords = Record.objects.all().order_by('-publish_time')[:10]
    tags = Tag.objects.all()
    evaluates = Evaluate.objects.all().order_by('-create_time')[:5]

    c ={"hotrecords": hotrecords, 'newrecords': newrecords, 'tags': tags, 'evaluates': evaluates}
    return render(request, template_name='index.html', context=c)


def detail(request, id):
    record = Record.objects.filter(id=int(id))[0]
    c = {"record": record, 'relaterecord': relate_record(record), 'relatenews':relatenews(record)}
    return render(request, template_name='detail.html', context=c)


def grabrecord(request):
    id = 0
    url = request.GET['urlname']
    title, original, content, time, keywords = grab_article.run(url)
    # content = ''.join(['<p>' + x + '</p>' for x in content])
    filterobj = Record.objects.filter(title=title)
    c={}
    if len(filterobj) == 0:
        record = Record()
        record.title = title
        record.source = url
        record.content = content
        record.publish_time = time
        record.originalpage = original
        record.keywords = keywords
        record.author = ''
        record.save()
        c = {"record": record}
    else:
        c = {"record": filterobj[0]}
    return render(request, template_name='detail.html', context=c)


def relate_record(record):
    if record:
        keywords = record.keywords
        objs =[]
        objall = Record.objects.all()
        for obj in objall:
            if obj.id == record.id:
                continue
            if similar_article.similar_check(keywords, obj.keywords):
                objs.append(obj)
        return objs


def relatenews(record):
    result = relate_news.redisresult(record)
    return result

