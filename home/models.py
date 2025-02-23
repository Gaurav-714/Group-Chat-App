from django.db import models

class GroupModel(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'

    def __str__(self):
        return self.name
    

class ChatModel(models.Model):
    content = models.CharField(max_length=1000)
    timestamp = models.DateField(auto_now=True)
    group = models.ForeignKey(GroupModel, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Chat'
        verbose_name_plural = 'Chats'

    def __str__(self):
        return self.content