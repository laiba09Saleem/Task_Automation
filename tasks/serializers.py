from rest_framework import serializers
from django.contrib.auth import get_user_model
from tasks.models import Task, TaskAssignment, Notifications

User = get_user_model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','first_name','last_name']

class TaskAssigmentSerializer(serializers.ModelSerializer):
    assignee = UserSerializer(read_only=True)
    assignee_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), sourse='assignee', write_only=True)
    class Meta:
        model = TaskAssignment
        fields = ['id', 'assignee','assignee_id','assigned_at','notified']

class TaskSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only_by=True)
    assignments = TaskAssigmentSerializer(many=True, read_only=True)
    class Meta:
        model = Task
        fields = ['id','title','description','due_date','created_by','status','created_at','assignments']

    def create(self, validated_data):
        user = self.context['request'].user
        task = Task.objects.create(created_by=user, **validated_data)
        return task
    
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = ['id','massage','crated_at','read']
