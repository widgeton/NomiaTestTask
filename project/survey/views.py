from django.shortcuts import render, redirect
from . import models
from . import result


def index(request):
    objs = models.Survey.objects.all()
    context = {
        'surveys': objs,
    }
    return render(request, 'surveys.html', context)


def survey(request, survey_id):
    choice_id = request.GET.get('choice_id')
    if choice_id == 'None':
        question = models.Survey.objects.get(id=survey_id).first_question
    else:
        choice = models.AnswerChoice.objects.get(id=choice_id)
        models.Answer(question_id=choice.question_id, choice_id=choice.id).save()
        if choice.next_question is None:
            return redirect('result', survey_id=survey_id)
        question = choice.next_question
    choices = question.choices.all()

    context = {
        'survey_id': survey_id,
        'question': question,
        'choices': choices,
    }
    return render(request, 'question.html', context)


def show_result(request, survey_id):
    srv = result.get_survey(survey_id)
    context = {
        'survey': srv
    }
    return render(request, 'result.html', context)
