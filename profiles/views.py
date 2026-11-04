from unicodedata import lookup
from urllib import request
import io 
from django.shortcuts import render

# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from . import services
from .models import BookmarkedProfile
def search(request):
    query = request.GET.get("q", "").strip()
    context = {"query": query, "profile": None, "repos": []}
    if query:
        try:
            context["profile"] = services.get_user(query)
            context["repos"] = services.get_repos(context["profile"]["username"])
        except services.GitHubError as exc: # catches all 4 error types
            messages.error(request, str(exc))
    return render(request, "profiles/search.html", context)
@login_required
@require_POST
def bookmark(request, username):    
    try:
        data = services.get_user(username) 
    except services.GitHubError as exc:
            
        return redirect("search")
    lookup = data.pop("username")
    _, created = BookmarkedProfile.objects.get_or_create(
                user=request.user, username=lookup, defaults=data
                )
    if created:
        messages.success(request, f"Bookmarked {lookup}.")
    else:
        messages.info(request, f"{lookup} is already bookmarked.")
    return redirect("bookmarks")
@login_required
def bookmark_list(request):
 items = BookmarkedProfile.objects.filter(user=request.user)
 return render(request, "profiles/bookmarks.html", {"bookmarks": items})
@login_required
@require_POST
def bookmark_delete(request, pk):
 item = get_object_or_404(BookmarkedProfile, pk=pk, user=request.user)
 item.delete()
 messages.success(request, "Bookmark removed.")
 return redirect("bookmarks")

from django.http import HttpResponseBadRequest, HttpResponse, FileResponse
from .temp import render_card
def visualise(request):
    username = request.GET.get("username", "").strip()
    if not username:
       return HttpResponseBadRequest("Missing username parameter.")
    try:
      profile = services.get_user(username)
      repos = services.get_repos(username)
      img = render_card(username=profile['username'],
                        name=profile['name'],
                        bio=profile['bio'],
                        public_repos=profile['public_repos'],
                        followers=profile['followers'],
                        following="N/A",
                        avatar_url=profile['avatar_url'],
                        repos=repos)
    except services.GitHubError as exc:
       return HttpResponseBadRequest(str(exc))
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return FileResponse(buffer, content_type="image/png") 



