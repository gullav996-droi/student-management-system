
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import Student


# Home Page
def home(request):

    if (
        request.method == "POST"
        and request.user.is_authenticated
        and request.user.is_staff
    ):
        name = request.POST["name"]
        age = request.POST["age"]
        email = request.POST["email"]
        phone = request.POST["phone"]

        Student.objects.create(
            created_by=request.user,   # 👈 NEW LINE
            name=name,
            age=age,
            email=email,
            phone=phone
        )

    students = Student.objects.all()

    return render(request, "index.html", {"students": students})


# Create Admin (Only gulla)
@login_required
def register(request):

    if request.user.username != "gulla":
        return redirect("/")

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password != confirm_password:
            return render(
                request,
                "register.html",
                {"error": "Passwords do not match"}
            )

        if User.objects.filter(username=username).exists():
            return render(
                request,
                "register.html",
                {"error": "Username already exists"}
            )

        user = User.objects.create_user(
            username=username,
            password=password
        )

        user.is_staff = True
        user.is_superuser = True
        user.save()

        return redirect("/")

    return render(request, "register.html")


# Logout
def logout_view(request):
    logout(request)
    return redirect("/")


# Delete Student
@login_required
def delete_student(request, id):

    if not request.user.is_staff:
        return redirect("/")

    student = Student.objects.get(id=id)
    student.delete()

    return redirect("/")


# Edit Student
@login_required
def edit_student(request, id):

    if not request.user.is_staff:
        return redirect("/")

    student = Student.objects.get(id=id)

    if request.method == "POST":

        student.name = request.POST["name"]
        student.age = request.POST["age"]
        student.email = request.POST["email"]
        student.phone = request.POST["phone"]

        student.save()

        return redirect("/")

    return render(request, "edit.html", {"student": student})

