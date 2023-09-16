from django.shortcuts import render
from rest_framework.views import APIView

from .forms import SearchForm
from .apps import RecommendConfig


class ImageSearch(APIView):
    def get(self, request):
        form = SearchForm()
        return render(request, 'recommend/search.html', {'form': form})

    def post(self, request):
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data.get('sentence')
            labels = RecommendConfig.model.inference(query)

            image_paths = [
                "https://ifong-image-data.s3.ap-northeast-2.amazonaws.com/0.png",
                "https://ifong-image-data.s3.ap-northeast-2.amazonaws.com/1.png",
                "https://ifong-image-data.s3.ap-northeast-2.amazonaws.com/2.png",
                "https://ifong-image-data.s3.ap-northeast-2.amazonaws.com/3.png",
                "https://ifong-image-data.s3.ap-northeast-2.amazonaws.com/4.png"
            ]

            context = {
                'image_paths': image_paths,
            }
        else:
            return render(request, 'recommend/search.html', {'form': form})
        return render(request, 'recommend/select.html', context)


class ImagePick(APIView):
    def get(self, request):
        return render(request, 'recommend/select.html')

    def post(self, request):
        pass
