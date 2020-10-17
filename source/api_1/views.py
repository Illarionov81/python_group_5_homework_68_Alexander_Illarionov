from django.shortcuts import render, get_object_or_404
import json
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse
from django.views.generic import View
from django.views.decorators.csrf import ensure_csrf_cookie

from api_1.serializers import ArticleSerializer
from webapp.models import Article


@ensure_csrf_cookie
def get_token_view(request, *args, **kwargs):
    if request.method == 'GET':
        return HttpResponse()
    return HttpResponseNotAllowed('Only GET request are allowed')


class ArticleListView(View):
    def get(self, request, *args, **kwargs):
        objects = Article.objects.all()
        slr = ArticleSerializer(objects, many=True)
        return JsonResponse(slr.data, safe=False)


class ArticleDetailView(View):
    def get(self, request, *args, **kwargs):
        print(self.kwargs.get('pk'))
        article = get_object_or_404(Article, pk=self.kwargs.get('pk'))
        srl = ArticleSerializer(article)
        return JsonResponse(srl.data)


class ArticleCreateView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        slr = ArticleSerializer(data=data)
        if slr.is_valid():
            article = slr.save()
            return JsonResponse(slr.data, safe=False)
        else:
            response = JsonResponse(slr.errors, safe=False)
            response.status_code = 400
            return response