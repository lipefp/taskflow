from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):

    STATUS_PENDENTE = 'pending'
    STATUS_EM_PROGRESSO = 'in_progress'
    STATUS_CONCLUIDA = 'done'

    STATUS_CHOICES = [
        (STATUS_PENDENTE, 'Pendente'),
        (STATUS_EM_PROGRESSO, 'Em Progresso'),
        (STATUS_CONCLUIDA, 'Concluída'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDENTE)
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title