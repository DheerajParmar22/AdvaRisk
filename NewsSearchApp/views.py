import requests
from django.shortcuts import render, redirect
from .models import UserSearch, SearchResult
from datetime import datetime
from django.conf import settings
from django.utils import timezone
from .forms import SearchForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from celery import shared_task


def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('search')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exists')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('search')
        else:
            messages.error(request, 'Username or Password does not exists')

    context = {'page': page}
    return render(request, 'login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def registerUser(request):
    # page ='register'
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('search')
        else:
            messages.error(request, 'An error occured during registration.')

    context = {'form': form}
    return render(request, 'login_register.html', context)


# @login_required(login_url='login')
def search(request):
    form = SearchForm(request.POST or None)

    # if request.user != user_search.user:
    #     return HttpResponse('You are not allowed here.')

    if request.method == 'POST':
        keyword = request.POST.get('keyword')

        existing_search = UserSearch.objects.filter(keyword=keyword).first()

        if existing_search:
            user_search = existing_search
            existing_search.date_searched = timezone.now()
            existing_search.save()
        else:
            # Fetch news articles using NewsAPI
            newsapi_url = f'https://newsapi.org/v2/everything?q={keyword}&apiKey={settings.NEWSAPI_KEY}'
            response = requests.get(newsapi_url)
            news_data = response.json()

            # Create UserSearch instance
            user_search = UserSearch.objects.create(
                keyword=keyword, date_searched=timezone.now(),
                user=request.user)

            # Create SearchResult instances
            for article in news_data['articles']:
                SearchResult.objects.create(
                    user_search=user_search,
                    title=article['title'],
                    description=article['description'],
                    url=article['url'],
                    date_published=datetime.strptime(
                        article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
                )
            # Delete the existing search (if any) to avoid duplicates
            UserSearch.objects.filter(keyword=keyword).exclude(
                id=user_search.id).delete()

        return redirect('search_results', search_id=user_search.id)

    searches = UserSearch.objects.filter(
        user=request.user).order_by('-date_searched')
    context = {'searches': searches, 'form': form}
    return render(request, 'search.html', context)


# @login_required(login_url='login')
def search_results(request, search_id):
    search = UserSearch.objects.get(pk=search_id)
    results = SearchResult.objects.filter(
        user_search=search).order_by('-date_published')

    # Apply date filter if start_date and end_date
    # are provided in the query parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        results = results.filter(
            date_published__gte=start_date, date_published__lte=end_date)

    context = {'search': search, 'results': results}
    return render(request, 'search_results.html', context)


# @login_required(login_url='login')
@shared_task
def refresh_results(request):
    keyword = request.POST.get('keyword')
    search = UserSearch.objects.get(keyword=keyword)

    latest_result = SearchResult.objects.filter(
        user_search=search).order_by('-date_published').first()
    if latest_result:
        latest_date = latest_result.date_published

        # Fetch news articles using NewsAPI published after latest_date
        newsapi_url = f'https://newsapi.org/v2/everything?q={keyword}&from={latest_date.strftime("%Y-%m-%dT%H:%M:%SZ")}&apiKey={settings.NEWSAPI_KEY}'
        response = requests.get(newsapi_url)
        news_data = response.json()

        # Create SearchResult instances for new articles
        for article in news_data['articles']:
            new_date = timezone.make_aware(
                datetime.strptime(
                    article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ'),
                timezone.utc
            )
            if new_date > latest_date:
                SearchResult.objects.create(
                    user_search=search,
                    title=article['title'],
                    description=article['description'],
                    url=article['url'],
                    date_published=new_date
                )

    return redirect('search_results', search_id=search.id)


@login_required(login_url='login')
def delete_search(request, search_id):
    try:
        search_to_delete = UserSearch.objects.get(
            id=search_id, user=request.user)
    except UserSearch.DoesNotExist:
        messages.error(request, 'Search not found or does not belong to you.')
        return redirect('search')

    search_to_delete.delete()
    messages.success(request, 'Search deleted successfully.')
    return redirect('search')


@login_required(login_url='login')
def userProfile(request, pk):
    user = User.objects.get(id=pk)

    context = {'user': user}
    return render(request, 'profile.html', context)
