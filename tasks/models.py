from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Task(models.Model):
    class Status(models.TextChoices):
        PENDENTE = 'PENDENTE', 'Pendente'
        EM_PROGRESSO = 'EM_PROGRESO', 'Em Progresso'
        CONCLUIDA = 'CONCLUIDA', 'Concluída'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default='')
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDENTE
    )
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
         
    def __str__(self):
        return f'{self.title} ({self.status})'