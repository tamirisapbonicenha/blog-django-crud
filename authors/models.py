from PIL import Image

from django.db import models

def author_image(instance, filename):
    return 'p_{0}/{1}'.format(instance.id, filename)

class Author(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to=author_image, null=True)
    bio = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Autor'
        verbose_name_plural = 'Autores'

    def __str__(self):
        return '%s' % (self.name)       
        