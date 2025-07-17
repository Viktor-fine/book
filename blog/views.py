from django.shortcuts import render, redirect
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required
from django.http import Http404

def index(request):
    return render(request, 'blog/index.html')

@login_required # Этот код должен выполняться до кода def topics()
def topics(request):
    """Выводит список всех тем из БД"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'blog/topics.html', context)

@login_required
def topic(request, topic_id):
    """Выводит одну тему и все её записи"""
    topic = Topic.objects.get(id=topic_id)

    # Проверко того, что тема принадлежит текущему пользователю
    if topic.owner != request.user:
        raise Http404


    entries = topic.entry_set.all()
    context = {'topic': topic, 'entries': entries}
    return render (request, 'blog/topic.html', context)

@login_required
def new_topic(request):
    # Добавляет новую тему
    if request.method != 'POST':
        #Данные не отправились. Создаётся пустая форма
        form = TopicForm()
    else:
        #Отправка данных методом POST и обработка.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('blog:topics')
        #Вывести пустую форму
    context = {'form': form}
    return render(request, 'blog/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    # Добавляет новую запись по конкретной теме
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        #Данные не отправились, создаётся пустая форма
        form = EntryForm()
    else:
        # Отправленны данные методом POST. Обработка данных
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('blog:topic', topic_id=topic_id)
    # Вывести пустую или не действительную форму
    context = {'topic': topic, 'form': form}
    
@login_required
def edit_entry(request, entry_id):
    #Редактирует существующую запись
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    #Защитим эту страницу, чтобы никто не мог подобрать URL для получения доступа к чужим записям
    if topic.owner != request.user:
        raise Http404

    if request.method !='POST':
        #Исходный запрос. Форма заполняется данными текущей записи
        form = EntryForm(instance=entry)
    else:
        # Отправка данных методом POST. Сделать обработку данных
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog:topic', topic_id=topic.id)
    context = {'entry':entry, 'topic':topic, 'form':form}
    return render(request, 'blog/edit_entry.html', context)     
