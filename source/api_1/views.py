from django.shortcuts import render, get_object_or_404
import json
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse, HttpResponseBadRequest
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
    def dispatch(self, request, *args, **kwargs):
        answer = {}
        if request.method !='GET':
            answer['error 405'] = "Not Allowed Method"
            response = JsonResponse(answer)
            response.status_code = 405
            return response
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        objects = Article.objects.all()
        slr = ArticleSerializer(objects, many=True)
        return JsonResponse(slr.data, safe=False)


class ArticleDetailView(View):

    def dispatch(self, request, *args, **kwargs):
        answer = {}
        if request.method != 'GET':
            answer['error 405'] = "Not Allowed Method"
            response = JsonResponse(answer)
            response.status_code = 405
            return response
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=self.kwargs.get('pk'))
        srl = ArticleSerializer(article)
        return JsonResponse(srl.data)


class ArticleUpdateView(View):
    def dispatch(self, request, *args, **kwargs):
        answer = {}
        if request.method not in ('POST', 'GET'):
            answer['error 405'] = "Not Allowed Method"
            response = JsonResponse(answer)
            response.status_code = 405
            return response
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=self.kwargs.get('pk'))
        srl = ArticleSerializer(article)
        return JsonResponse(srl.data)

    def post(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=self.kwargs.get('pk'))
        try:
            data = json.loads(request.body)
            slr = ArticleSerializer(data=data, instance=article)
            if slr.is_valid():
                slr.save()
                return JsonResponse(slr.data, safe=False)
            else:
                response = JsonResponse(slr.errors, safe=False)
                response.status_code = 400
                return response
        except Exception as e:
            response = HttpResponseBadRequest(e)
        return response


class ArticleCreateView(View):
    def dispatch(self, request, *args, **kwargs):
        answer = {}
        if request.method != 'POST':
            answer['error 405'] = "Not Allowed Method"
            response = JsonResponse(answer)
            response.status_code = 405
            return response
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        slr = ArticleSerializer(data=data)
        if slr.is_valid():
            article = slr.save()
            # return render(request, 'article/article_view.html', context={'article': article})
            return JsonResponse(slr.data, safe=False)
        else:
            response = JsonResponse(slr.errors, safe=False)
            response.status_code = 400
            return response


class ArticleDeleteView(View):
    def dispatch(self, request, *args, **kwargs):
        answer = {}
        if request.method != 'DELETE':
            answer['error 405'] = "Not Allowed Method"
            response = JsonResponse(answer)
            response.status_code = 405
            return response
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        article_id = self.kwargs.get('pk')
        article = get_object_or_404(Article, pk=article_id)
        article.delete()
        answer = {'pk': article_id}
        return JsonResponse(answer, safe=False)


