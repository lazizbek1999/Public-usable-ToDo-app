from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm, CustomUserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
import json  # Import Python's built-in json tool at the top of your views.py
from django.contrib import messages  # Standard Django message framework


def register_view(request):
    if request.user.is_authenticated:
        return redirect('task_list')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_list')
        else:
            # Loop through errors and add them to Django messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
            
            # This redirect completely protects you from the refresh popup!
            return redirect('register') 
            
    else:
        form = CustomUserCreationForm()
            
    return render(request, 'my_app/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('task_list')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('task_list')
        
    else:
        form = AuthenticationForm()
    return render(request, 'my_app/login.html', {'form':form})



def task_list_view(request):
    if request.method == 'POST':
        # Safety: Prevent non-logged-in guests
        # from submitting tasks via POST
        if not request.user.is_authenticated:
            return redirect('login')
        form = TaskForm(request.POST,request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    # this down code only for logged in users!Django require user.tasks >
    # if user not created a task then web crashes !'AnonymousUser' 
    # OR demands only loggedin user,renders data belonging to only user which clicked button 
    # then django executed the code fetches only data for request.user!
    # tasks = request.user.tasks.all().order_by('-created_at')
    
    # NOT Valid Only fetch tasks belonging to THIS logged-in user!
    # now i allow all users to see whole submitted tasks
    # Fetch ALL tasks across the entire app so guests and users see everything
    tasks = Task.objects.all().order_by('-created_at')
    
    return render(request, 'my_app/task_list.html', {'tasks': tasks, 'form': form})

@login_required
def task_update_view(request,pk):
    # code down throws error if non-loggedin user tries to edit or delete!
    task = get_object_or_404(Task, pk=pk, user=request.user)
    
    if request.method == 'POST':
        # passing 'instance=task' tells Django to update this specific task, not create a new one
        #In Django, a ModelForm can be used for both creating new items and updating existing ones
        #By passing instance=task, you are telling Django: "Don't create a new database row.
        # Instead, pre-fill this form with the data from this existing task,
        # and overwrite it when saved.
        form = TaskForm(request.POST,request.FILES,instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task) # Pre-fill the form with current task details
        
    return render(request, 'my_app/task_update.html',{'form': form, 'task': task})

@login_required
def task_delete_view(request, pk):
    # Security: Ensure the task exists AND belongs to the logged-in user
    # otherwise it will throw an error
    task = get_object_or_404(Task, pk=pk, user=request.user)
    
    if request.method == 'POST':
        task.delete() # i delete opted task from database
        return redirect('task_list')
    return render(request, 'my_app/task_delete.html',{'task':task})

