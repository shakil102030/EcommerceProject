from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from EcommProduct.models import Category, Product, Images, Comment
from django.contrib import messages
from EcommerceApp.models import Setting
from .forms import SignUpForm, UserUpdateForm, ProfileUpdateForm
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm


def UserSignUp(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['username']
            user.first_name = form.cleaned_data['firstname']
            user.last_name = form.cleaned_data['lastname']
            user.email = form.cleaned_data['email']
            user.username = user.email.split('@')[0]
            user.set_password(form.cleaned_data['password'])
            user.save()
            userprofile = UserProfile.objects.create(user=user, image="images/users/user.jpg")
            userprofile.save()
            return redirect('UserLogin')
        else:
            messages.warning(request, "Your new and reset password is not matching")
    else:
        form = SignUpForm(),
    return render(request, 'signup.html', {'form': form})

def UserLogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.warning(request, 'Your username or password is invalid.')
    category = Category.objects.all()
    setting = Setting.objects.get(id=1)

    context = {'category': category,
               'setting': setting}
    return render(request, 'login.html', context)


def UserLogout(request):
    logout(request)
    return redirect('home')

@login_required(login_url='/account/login')
def userProfile(request):
    category = Category.objects.all()
    setting = get_object_or_404(Setting, id=1)
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)

    context = {'category': category,
               'setting': setting,
               'profile': profile,}
    return render(request, 'user_profile.html', context)


@login_required(login_url='/account/login')  # Check login
def userUpdate(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('userprofile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user)
        category = Category.objects.all()
        setting = Setting.objects.get(id=1)
        context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'category': category,
            'setting': setting,
        }
        return render(request, 'userupdate.html', context)


@login_required(login_url='/account/login')  # Check login
def UserPassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('userprofile')
        else:
            messages.error(
                request, 'Please correct the error below.<br>' + str(form.errors))
            return redirect('UserPassword')
    else:
        category = Category.objects.all()
        setting = Setting.objects.get(id=1)
        form = PasswordChangeForm(request.user)
        context = {'form': form,'category': category,'setting': setting,}
        return render(request, 'userpasswordupdate.html', context)

@login_required(login_url='/account/login')
def UserComments(request):
    category = Category.objects.all()
    setting = Setting.objects.get(id=1)
    current_user = request.user
    comment = Comment.objects.filter(user_id=current_user.id)
    context = {
        'category': category,
        'setting': setting,
        'comment': comment,
    }
    return render(request, 'usercomment.html', context)


def CommentDelete(request, id):
    current_user = request.user
    comment = Comment.objects.filter(user_id=current_user.id, id=id)
    comment.delete()
    messages.success(request, 'Your comment is successfully deleted')
    return redirect('UserComments')
