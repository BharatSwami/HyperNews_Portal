from django.shortcuts import render,redirect

# Create your views here.
from django.http import HttpResponse
from django.conf import settings
from django.views import View
import json
import random
from datetime import datetime




class searchEngine(View):
    def jsonFileRead(self,file):
        with open(file, 'r') as json_file:
            news_json_info = json.load(json_file)
            return news_json_info

    def get(self,request,*args,**kwargs):
        toFind = request.GET.get('q')
        news_json_data=self.jsonFileRead(settings.NEWS_JSON_PATH)
        news_data=[]
        if toFind:
            for data in news_json_data:
                if toFind in data['title']:
                    news_data.append(data)
        else:
            news_data=news_json_data
        news_dict = {}
        for i in news_data:
            date = i["created"][:10]
            if date in news_dict:
                news_dict[date].append(i)
            else:
                news_dict[date] = [i]
        news_json_info = dict(sorted(news_dict.items(), key=lambda item: item[0], reverse=True))
        context = {'news_json_info': news_json_info}
        return render(request, 'news/index.html', context=context)

    """def index(self,request):
        with open(settings.NEWS_JSON_PATH, 'r') as json_file:
            news_json = json.load(json_file)
        #  news_json_info=sorted(news_json_info,key=function_datetime)
        news_dict = {}
        for i in news_json:
            date = i["created"][:10]
            if date in news_dict:
                news_dict[date].append(i)
            else:
                news_dict[date] = [i]
        news_json_info = dict(sorted(news_dict.items(), key=lambda item: item[0], reverse=True))
        context = {'news_json_info': news_json_info}
        return render(request, 'news/index.html', context=context)"""

class NewsPage(View):

    def get(self,request,page_id,*args,**kwargs):
        with open(settings.NEWS_JSON_PATH, 'r') as json_file:
            news_json_info = ""
            for i in json.load(json_file):
                if int(i["link"])==int(page_id):
                    news_json_info=i
                    break
        news_info=f"<h2>{news_json_info['title']}</h2>" \
                  f"<p>{news_json_info['created']}</p>"  \
                f"<p>{news_json_info['text']}</p>" \
                f"<a href='/news/' target=''>main</a>"

        return HttpResponse(news_info)


class FormPage(View):

    def jsonFileRead(self,file):
        with open(file, 'r') as json_file:
            news_json_info = json.load(json_file)
            return news_json_info

    def get(self,request,*args,**kwargs):
        return render(request,'news/form.html')

    def post(self,request,*args,**kwargs):
        title=request.POST.get('title')
        text=request.POST.get('text')
        news_json_info=self.jsonFileRead(settings.NEWS_JSON_PATH)
        link_lst = [int(i["link"]) for i in news_json_info]
        new_link = random.randint(1, 1000000000)
        while new_link in link_lst:
            new_link = random.randint(1, 1000000000)
        new_dict = {
            "created": f"{datetime.now()}",
            "text": text,
            "title": title,
            "link": new_link
        }
        news_json_info.append(new_dict)
        with open(settings.NEWS_JSON_PATH,'w') as json_file:
            json.dump(news_json_info,json_file)
        return redirect("/")
