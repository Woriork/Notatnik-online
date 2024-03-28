from django.shortcuts import render, redirect
from .models import Note, Topic
from .forms import NoteForm
# Create your views here.


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    notes = Note.objects.filter(topic__name__icontains = q)

    topics = Topic.objects.all()

    context = {'notes' : notes, 'topics' : topics}
    return render(request, 'base/home.html', context)

def note(request, pk):
    note = Note.objects.get(id = pk)
    context = {'note': note}
    return render(request, 'base/note.html',context)

def createNote(request):
    form = NoteForm()
    if request.method =='POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/note_form.html', context)

def updateNote(request,pk):
    note = Note.objects.get(id = pk)
    form = NoteForm(instance=note)

    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/note_form.html', context)

def deleteNote(request,pk):
    note = Note.objects.get(id=pk)
    if request.method =="POST":
        note.delete()
        return redirect('home')
    return render(request, 'base/delete.html',{'obj':note})