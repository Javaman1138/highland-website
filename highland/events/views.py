from django.views import generic
from .models import Event, NewsItem
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
from common.rotation import Rotation
import datetime
import json

class EventView(generic.ListView):
    template_name = 'events.html'

    def get(self, request):
        now = datetime.datetime.now()
        if request.is_ajax():
            return self.get_ajax(request, now)
        else:
            return self.get_html(request, now)
        
    def get_html(self, request, now):
        """Return next 5 events."""
	rotation = Rotation()
	rotation_days = rotation.get_rotation_days(0)

        upcoming_list = Event.objects.filter(start_date__gte=now.date()).order_by('start_date')[:5]
        return render(request, self.template_name, {'upcoming_list':upcoming_list,
						    'today':datetime.datetime.now().date(),
        					    'rotation_days':rotation_days})
        
    def get_ajax(self, request, now):
    	if (request.GET.get('count')):
    	    try:
                count = int(request.GET.get('count'))
            except:
            	count = 0
    	else:
    	    count = 0
    	    
    	if (count > 0):
            events = Event.objects.order_by('start_date')[:count]
        else:
            events = Event.objects.order_by('start_date')

        data = serializers.serialize("json", events)
    	return HttpResponse(json.dumps(data), content_type="application/json")

class NewsView(generic.ListView):
    template_name = 'newsitems.html'
    
    def get(self, request):
    	news_list = NewsItem.objects.all().order_by('-news_date')
    	for item in news_list:
    		if len(item.news_long) > 200:
    			item.news_long = item.news_long[:200]
    			item.show_more = True
    		item.news_long = item.news_long.replace("\n", "<br>")
    	return render(request, self.template_name, {'news_list': news_list})

class NewsItemView(generic.TemplateView):
    template_name = 'single_news_item.html'

    def get(self, request, *args, **kwargs):
    	id = request.GET.get('id')
    	if not id:
	    raise Http404("WTF")
	popup = request.GET.get('popup')
	if popup:
		self.template_name = self.template_name.replace('.html', '_popup.html')
   	news_item = NewsItem.objects.filter(pk=id)[0]
	news_item.news_long = news_item.news_long.replace("\n", "<br>")
        context = {'news_item': news_item}
        return render(request, self.template_name, context)


