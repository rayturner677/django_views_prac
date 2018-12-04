from django.shortcuts import render, redirect
from app.models import Link
from django.views import View


# Create your views here.
class Create(View):
    def post(self, request):
        url = request.POST['url']
        link = Link.shorten(url)

        if link == None:
            return render(
                request, 'app/create.html', {'invalid_url': True}, status=422)

        else:
            return redirect('app:show', short_code=link.short_code)

    def get(self, request):
        return render(request, 'app/create.html')


class Show(View):
    def get(self, request, short_code):
        link = Link.find_by_short_code(short_code)
        if link:
            return render(request, 'app/show.html', {'link': link})
        else:
            return render(request, 'app/show.html')


class Goto(View):
    def get(self, request, short_code):
        link = Link.find_by_short_code(short_code)
        if link:
            return redirect(link.original)
        else:
            return redirect('app:create')
