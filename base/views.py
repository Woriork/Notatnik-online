from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
#from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Note, Topic, Message
from .forms import NoteForm
# Create your views here.


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method =="POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request,username=username, password=password)
        
        if user is not None:
            login(request,  user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password does not exist')

    context = {'page':page}
    return render(request, 'base/login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,'An error occurred during registration')

    return render(request,'base/login_register.html',{'form' : form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    notes = Note.objects.filter(topic__name__icontains = q)

    topics = Topic.objects.all()

    context = {'notes' : notes, 'topics' : topics}
    return render(request, 'base/home.html', context)

def note(request, pk):
    note = Note.objects.get(id = pk)
    note_messages = note.message_set.all().order_by('-created')
    participants = note.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            note=note,
            body=request.POST.get('body')
        )
        return redirect('note', pk=note.id)
    context = {'note' : note, 'note_messages' : note_messages,
                'participants': participants}
    return render(request, 'base/note.html', context)

@login_required(login_url='login')
def createNote(request):
    form = NoteForm()
    if request.method =='POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/note_form.html', context)

@login_required(login_url='login')
def updateNote(request,pk):
    note = Note.objects.get(id = pk)
    form = NoteForm(instance=note)

    if request.user != note.host:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/note_form.html', context)

@login_required(login_url='login')
def deleteNote(request,pk):
    note = Note.objects.get(id=pk)

    if request.user != note.host:
        return HttpResponse('You are not allowed here')

    if request.method =="POST":
        note.delete()
        return redirect('home')
    return render(request, 'base/delete.html',{'obj':note})