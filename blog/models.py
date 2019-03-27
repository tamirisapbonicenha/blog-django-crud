from django.db import models

from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=200)
    
    def publish(self):
        self.save()

    def __str__(self):
        return self.name   


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)
    created_date = models.DateTimeField(
            default=timezone.now)

    def publish(self):
        self.save()

    def __str__(self):
        return self.title
