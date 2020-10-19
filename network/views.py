from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .models import User , Post
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from django.core.paginator import Paginator


def index(request):

    if request.method == "POST":
        if request.POST["postBody"] == "":
            return HttpResponseRedirect(reverse("index"))
        newPost = Post(poster=request.user, body=request.POST["postBody"])
        newPost.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        posts = Post.objects.order_by("-timestamp")
        # paginator = Paginator(posts, 10)
        #
        # page_number = request.GET.get('page')
        # page_obj = paginator.get_page(page_number)
        return render(request, "network/index.html",{'page_obj': paginate(request,posts)})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@csrf_exempt
def userProfile(request,name):
    profile = User.objects.get(username=name)
    if request.method == "GET":
        posts = paginate(request,profile.posts.all().order_by("-timestamp"))
        return render(request, "network/profile.html", {"profile":profile,'page_obj':posts })

    elif request.method == "PUT":
        if request.user != profile:
            data = json.loads(request.body)
            if data.get("follow") == True:
                request.user.following.add(profile)
                return HttpResponse(status=204)
            else:
                request.user.following.remove(profile)
                return HttpResponse(status=204)
        else:
            return JsonResponse({"error": "Users can't follow themselves."}, status=400)
    else:
        return HttpResponse("GET or PUT request reqired")

@login_required
def following(request):
    #following = [f.id for f in request.user.following.all()]
    posts = Post.objects.filter(poster__in=request.user.following.all()).order_by("-timestamp")
    return render(request,"network/following.html",{"page_obj":paginate(request,posts)})

@csrf_exempt
@login_required
def edit(request,ID):
    if request.method == "PUT":
        data = json.loads(request.body)
        editing_Post = Post.objects.get(id=ID)
        if data.get("text") is not None:
            if editing_Post.poster == request.user:
                editing_Post.body = data.get("text")
                editing_Post.save()
                return HttpResponse(status=204)
            else:
                return JsonResponse({"error": "you can only edit your posts."}, status=400)
        if data.get("like") is not None:
            if data.get("like"):
                editing_Post.like.add(request.user)
            else:
                editing_Post.like.remove(request.user)
            return HttpResponse(status=204)
    else:
        return JsonResponse({"error": "PUT request required."}, status=400)





def paginate(request,posts):
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
