from django.db.models import F
from .models import Choice, Question
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.views import View

def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "index.html", context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "details.html", {"question": question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    
    if request.method == "POST":
        selected_choice_id = request.POST.get('choice')
        try:
            selected_choice = question.choice_set.get(pk=selected_choice_id)
        except Choice.DoesNotExist:
            return render(request, 'details.html', {
                'question': question,
                'error_message': "Seçilen seçim geçersiz."
            })
        else:
            # Seçilen oyunu güncelle
            selected_choice.votes += 1
            selected_choice.save()  # Veritabanına kaydet

            # Sonuç sayfasına yönlendir
            return redirect('myapp:results', question.id)

    return render(request, 'details.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "myapp:results.html", {"question": question})
class IndexView(generic.ListView):
    model=Question
    template_name = "index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = "details.html"

   

class NaberView(View):
    def get(self, request):
        return render(request, 'naber.html')

class ResultsView(generic.DetailView):
    model = Question
    template_name = "results.html"

from django.shortcuts import get_object_or_404, render

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "results.html", {"question": question})
