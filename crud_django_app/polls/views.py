from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from polls.domain.entity.question import Question
from polls.domain.entity.choice import Choice


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "lastest_question_list"

    def get_queryset(self):
        """Return the last five published question"""
        question = Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
        return question


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/details.html"

    def get_queryset(self):
        """
        Excludes any question that aren´t published yet
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])

    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/details.html', {
            'question': question,
            'error_message': 'No elegiste una respuesta'
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:result', args=(question.id,)))

