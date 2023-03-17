from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Profile, Dweet
from .forms import DweetForm
from django.contrib.auth.models import User
from django.db.models import Q 
from django.contrib.auth.decorators import login_required
from django.http import Http404

@login_required
def like_view(request, pk):
    dweet = Dweet.objects.get(pk = pk)
    if request.user not in dweet.liked_by.all():
        dweet.liked_by.add(request.user)
    else:
        dweet.liked_by.remove(request.user)
    dweet.save()
    return redirect("dashboard")

@login_required
def detail_view(request, pk):
    context = {}
    dweet = Dweet.objects.get(pk = pk)
    if request.method == "POST":
        form = DweetForm(request.POST)
        if form.is_valid():
            new = form.save(commit = False)
            new.user = request.user
            new.parent = dweet
            new.save()
            return redirect("dashboard")
    else:
        form = DweetForm()
    context["dweet"] = dweet
    context["form"] = form
    return render(request, "dweet_detail.html", context)

@login_required
def delete_view(request, pk):
    post = get_object_or_404(Dweet, pk=pk)
        
    if request.user != post.user:
        raise Http404("You do not have permission to delete this post")

    if request.method == 'POST':
        post.delete()
        return redirect(reverse('dashboard'))

    return redirect(reverse('dashboard'))

@login_required
def search_view(request):
    context = {}
    if request.GET.get("type") == "search_user":
        search = request.GET.get("search")
        profiles = Profile.objects.filter(Q(user__username__icontains=search))
        context["profiles"] = profiles
    return render(request, "search.html", context)

@login_required
def dashboard_view(request):
    context = {}
    form = DweetForm(request.POST or None)
    if request.method == "POST":
        form = DweetForm(request.POST)
        if form.is_valid():
            dweet = form.save(commit = False)
            dweet.user = request.user
            dweet.save()
            return redirect("dashboard")
    context["form"] = form
    followed_dweets = Dweet.objects.filter(
        user__profile__in = request.user.profile.follows.all()
    ).order_by("-created_at")
    context["dweets"] = followed_dweets
    return render(request, "dashboard.html", context)

@login_required
def profile_list_view(request):
    context = {}
    profiles = Profile.objects.exclude(user = request.user)
    context["profiles"] = profiles
    return render(request, "profile_list.html", context)

@login_required
def profile_view(request, username):
    if not hasattr(request.user, "profile"):
        missing_profile = Profile(user=request.user)
        missing_profile.save()
    context = {}
    user = User.objects.get(username = username)
    profile = Profile.objects.get(user = user)
    if request.method == "POST":
        action = request.POST.get("followkey")
        if action == "follow":
            request.user.profile.follows.add(profile)
        elif action == "unfollow":
            request.user.profile.follows.remove(profile)
        request.user.profile.save()
    context["profile"] = profile
    return render(request, "profile.html", context)