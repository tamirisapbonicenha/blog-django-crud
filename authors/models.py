from django.db import models

class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    introduction = models.CharField(max_length=256)

    class Meta:
        ordering = ['first_name']
        verbose_name = 'Autor'
        verbose_name_plural = 'Autores'

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)       
        