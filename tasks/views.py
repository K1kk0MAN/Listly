from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout  
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils import timezone
import json

from .models import *

# Create your views here.
def index(request):
    return render(request, "tasks/index.html", {
        "page_title": "Welcome",
    })


@login_required
def profile(request, username):
    lists = List.objects.filter(user__username=username).order_by("name", "-timestamp")

    paginator = Paginator(lists, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "tasks/profile.html", {
        "list": lists,
        "lists": page_obj,
        "page_title": "Profile: " + username,
    })


@login_required
def create_list(request):
    if request.method == "POST":
        name = request.POST["name"]
        description = request.POST["description"] if request.POST["description"] else ""
        public = bool(request.POST.get("public"))
        everyday_uncheck = bool(request.POST.get("everyday_uncheck"))

        if not name:
            return render(request, "tasks/create.html", {
                "page_title": "Create Fresh List",
                "message": "List Must Have a Name"
            })
        
        new_list = List.objects.create(
            user=request.user,
            name=name,
            description=description,
            public=public,
            everyday_uncheck=everyday_uncheck,
        )
        return redirect("task_list", list_id=new_list.id)
    
    return render(request, "tasks/create.html", {
        "page_title": "Create Fresh List",
    })


def task_list(request, list_id):
    list_obj = List.objects.get(id=list_id)
    items = list_obj.item.all().order_by("-id")

    today = timezone.now().date()

    if list_obj.everyday_uncheck and list_obj.last_reset != today:
        Item.objects.filter(list=list_obj).update(checked=False)
        list_obj.last_reset = today
        list_obj.save()

    return render(request, "tasks/task_list.html", {
        "page_title": "List: " + list_obj.name,
        "list": list_obj,
        "items": items,
    })


@login_required
def copy_list(request, list_id):
    if request.method == "POST":
        try:
            original = List.objects.get(id=list_id)

            copied = List.objects.create(
                name=f"{original.name} (copy)",
                user=request.user,
                description=original.description,
                public=original.public,
                everyday_uncheck=original.everyday_uncheck,
            )

            for item in original.item.all():
                Item.objects.create(
                    list=copied,
                    content=item.content,
                    checked=False,
                )

            return JsonResponse({"success": True})

        except List.DoesNotExist:
            return JsonResponse({"error": "List Not Found"})
        
    return JsonResponse({"error": "Invalid Request"}, status=400)


@login_required
def add_item(request, list_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            content = data.get("content", "").strip()

            if not content:
                return JsonResponse({"error": "Task content is empty"}, status=400)

            list_obj = List.objects.get(id=list_id, user=request.user)
            new_item = Item.objects.create(list=list_obj, content=content)

            return JsonResponse({
                "id": new_item.id,
                "content": new_item.content,
                "checked": new_item.checked
            })

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except List.DoesNotExist:
            return JsonResponse({"error": "List not found"}, status=404)

    return JsonResponse({"error": "Invalid Request"}, status=400)


@login_required
def toggle_item(request, item_id):
    try:
        item = Item.objects.get(id=item_id, list__user=request.user)
        item.checked = not item.checked
        item.save()

        return JsonResponse({"id": item.id, "checked": item.checked})

    except Item.DoesNotExist:
        return JsonResponse({"error": "Item Not Found"}, status=404)


@login_required 
def delete_item(request, item_id):
    if request.method == "POST":
        try:
            item = Item.objects.get(id=item_id, list__user=request.user)
            item.delete()
            
            return JsonResponse({"success": True})
        
        except Item.DoesNotExist:
            return JsonResponse({"error": "Item Not Found"}, status=404)
        
    return JsonResponse({"error": "Invalid Request"}, status=400)


def public_lists(request):
    lists = List.objects.filter(public=True).order_by("-timestamp")

    paginator = Paginator(lists, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "tasks/browse.html", {
        "list": lists,
        "lists": page_obj,
        "page_title": "Browse Public Lists"
    })


def login_view(request):
    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("profile", user.username)
        else:
            return render(request, "tasks/login.html", {
                "message": "Invalid Username and/or Password",
                "page_title": "Log In"
            })
    
    return render(request, "tasks/login.html")


def register_view(request):
    if request.method == "POST":

        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request, "tasks/register.html", {
                "message": "Passwords Do Not Match",
                "page_title": "Sign Up",
            })
        
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "tasks/register.html", {
                "message": "User Already Exists",
                "page_title": "Sign Up",
            })
        
        login(request, user)
        return redirect("profile", user.username)

    return render(request, "tasks/register.html", {
        "page_title": "Sign Up",
    })


def logout_view(request):
    logout(request)
    return redirect("index")