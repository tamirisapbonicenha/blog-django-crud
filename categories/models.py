from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50)

    def publish(self):
        self.save()

    def __str__(self):
        return self.name
