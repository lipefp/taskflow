from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'created_at', 'updated_at' ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_status(self, new_status):
        instance = self.instance
        if instance is None:
            return new_status
        
        current_status = instance.status

        transitions = {
            'pending': ['in_progress', 'done'],
            'in_progress': ['done'],    
            'done': [],
        }

        allowed = transitions.get(current_status, [])
       
        if new_status != current_status and new_status not in allowed:
            raise serializers.ValidationError(
                f'Transcição inválida de {current_status} para {new_status}.'
            )
        return new_status