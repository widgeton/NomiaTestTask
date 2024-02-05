from django.db import models


class Survey(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=256)
    first_question = models.ForeignKey("Question", on_delete=models.SET_NULL, null=True, blank=True)


class Question(models.Model):
    text = models.CharField(max_length=512)
    srv = models.ForeignKey("Survey", on_delete=models.CASCADE)


class AnswerChoice(models.Model):
    question = models.ForeignKey("Question", on_delete=models.CASCADE, related_name="choices")
    text = models.CharField(max_length=256)
    next_question = models.ForeignKey("Question", on_delete=models.CASCADE, null=True, blank=True)


class Answer(models.Model):
    question = models.ForeignKey("Question", on_delete=models.CASCADE)
    choice = models.ForeignKey("AnswerChoice", on_delete=models.CASCADE)
