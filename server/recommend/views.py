from django.shortcuts import render
from rest_framework.views import APIView

from .forms import SearchForm
from .apps import RecommendConfig
from .utils import add_img_path


class ImageSearch(APIView):
    def get(self, request):
        form = SearchForm()
        return render(request, 'recommend/search.html', {'form': form})

    def post(self, request):
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data.get('sentence')
            labels = RecommendConfig.model.inference(query)
            context = add_img_path(labels)
        else:
            return render(request, 'recommend/search.html', {'form': form})
        return render(request, 'recommend/select.html', context)


class ImagePick(APIView):
    def get(self, request):
        return render(request, 'recommend/select.html')

    def post(self, request):
        pass
