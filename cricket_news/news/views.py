from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import News
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .forms import NewsForm

def home(request):
    context = {}
    
    if request.user.is_authenticated:
        # Author view
        context.update({
            'total_articles': request.user.news_set.count(),
            'recent_articles': request.user.news_set.order_by('-pub_date')[:5]
        })
    else:
        # Public view
        news = News.objects.all().order_by('-pub_date')
        context.update({
            'featured_article': news.first(),
            'latest_news': news[1:7] 
        })
    
    return render(request, 'news/home.html', context)

def news_list(request):
    news = News.objects.all()
    search_query = request.GET.get('search')
    
    if search_query:
        news = news.filter(title__icontains=search_query) | news.filter(content__icontains=search_query)
    
    return render(request, 'news/news_list.html', {'news': news})

def news_detail(request, pk):
    article = get_object_or_404(News, pk=pk)
    return render(request, 'news/news_detail.html', {'article': article})

@login_required
def create_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            messages.success(request, 'Article created successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = NewsForm()
    
    context = {
        'form': form,
        'title': 'Create News Article'
    }
    return render(request, 'news/create_news.html', context)

@login_required
def edit_news(request, pk):
    news = get_object_or_404(News, pk=pk)
    

    if news.author != request.user:
        messages.error(request, "You don't have permission to edit this article.")
        return redirect('news_detail', pk=pk)
    
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            form.save()
            messages.success(request, 'Article updated successfully!')
            return redirect('news_detail', pk=pk)
    else:
        form = NewsForm(instance=news)
    
    return render(request, 'news/edit_news.html', {
        'form': form,
        'news': news
    })


@login_required
def profile(request):
    return render(request, 'profile.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome {user.username}! Your account has been successfully created.')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return render(request, 'base.html')  