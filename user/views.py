from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Account
from .forms import UserRegisterForm, UserUpdateForm, UploadFileForms
from django.views.generic import TemplateView
from django.core.exceptions import ValidationError

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
import os
import time
import pathlib
import requests
from bs4 import BeautifulSoup as bs
from django.contrib import messages
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render
from .forms import UploadForm
from .models import Record
# Create your views here.
def upload_form(request):
    if request.method == 'POST':
        form=UploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        else:
            context ={'form': form}
            return render(request, 'user/uploadaudio.html',context)
    context={'form':UploadForm()}
    return  render(request, 'user/uploadaudio.html',context)



from django.shortcuts import render
from haystack.query import SearchQuerySet
from .models import Post
from django.views.generic import (
    ListView,DetailView,
    CreateView,
    UpdateView,
    DeleteView)


class PostListView(ListView):
    model = Post
    template_name = 'user/homepage.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']

class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'file']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def validate_file_extension(value):
        import os
        ext = os.path.splitext(value.name)[1]
        valid_extensions = ['.wav', '.mp3', '.docx']
        if not ext in valid_extensions:
            raise ValidationError(u'File not supported!')


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def search(request):
    query = request.GET.get('q')
    results = []

    if query:
        results = SearchQuerySet().models(Post).filter(content=query)

    return render(request, 'searchresult.html', {'results': results})

def record(request):
    if request.method == "POST":
        audio_file = request.FILES.get("recorded_audio")
        language = request.POST.get("language")
        record = Record.objects.create(language=language, voice_record=audio_file)
        record.save()
        messages.success(request, "Audio recording successfully added!")
        return JsonResponse(
            {
                "success": True,
            }
        )
    context = {"page_title": "Record audio"}
    return render(request, "user/record.html", context)


def record_detail(request, id):
    record = get_object_or_404(Record, id=id)
    context = {
        "page_title": "Recorded audio detail",
        "record": record,
    }
    return render(request, "user/record_detail.html", context)


def audio(request):
    records = Record.objects.all()
    context = {"page_title": "Voice records", "records": records}
    return render(request, "user/audio.html", context)

def userfeed(request):
    return render(request, 'user/userfeed.html', {'title': '  Home Page'})
def userfeed(request):
    return render(request, 'accounts/userfeed.html', {'title': '  Home Page'})


def start(request):
    return render(request, 'user/start.html', {'title': ' Start Page'})

def about(request):
    return render(request, 'user/about.html', {'title': 'About'})
def login(request):
    return render(request, 'user/login.html', {'title': 'Login'})
def indexsocial(request):
    return render(request, 'user/indexsocial.html', {'title': 'Login'})
def upload(request):
    return HttpResponse('<h1>Upload View </h1>')
class Home(TemplateView):
    template_name = "home.html"

def index(request):
    context = {'redirect_to': request.path}

    return render(request, 'index3.html',context), {'title': 'Search'}

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your Account Has Been Created!')
            return redirect('site-user-login')



    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html', {'form': form})



posts = [
    {
        'author': 'CoreyMS',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'August 27, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'August 28, 2018'
    }
]


@login_required
def homepage(request):
    {'user': Account.objects.all(),
     'posts': posts



     }
    return render(request, 'user/homepage.html', {'title': 'Homepage'})


@login_required
def editacc(request):
    if request.method == 'POST':

     u_form= UserUpdateForm(request.POST,instance=request.user)
     if u_form.is_valid():
         u_form.save()
         messages.success(request, f'Your Account Has Been Updated!')
         return redirect('site-homepage')
    else:
        u_form = UserUpdateForm( instance=request.user)

    context={
        'u_form':u_form
    }

    return render(request, 'user/editacc.html', {'u_form':u_form})






@login_required
def logout(request):
    return render(request, 'user/logout.html', {'title': 'Logout'})


def passreset(request):
    return render(request, 'user/passreset.html', {'title': 'Password Reset'})


def passreset2(request):
    return render(request, 'user/passreset2.html', {'title': 'Password Reset'})

def search(request):
    if request.method == 'POST':
        search = request.POST['search']
        url = 'https://www.ask.com/web?q='+search
        # url = 'https://www.google.com/search?q='+search
        res = requests.get(url)
        soup = bs(res.text, 'lxml')

        result_listings = soup.find_all('div', {'class': 'PartialSearchResults-item'})
        # result_listings = soup.find_all('div', {'class': 'PartialSearchResults-item'})

        final_result = []

        for result in result_listings:
            result_title = result.find(class_='PartialSearchResults-item-title').text
            result_url = result.find('a').get('href')
            result_desc = result.find(class_='PartialSearchResults-item-abstract').text

            final_result.append((result_title, result_url, result_desc))

        context = {
            'final_result': final_result
        }

        return render(request, 'search.html', context)
    else:
        return render(request, 'search.html')