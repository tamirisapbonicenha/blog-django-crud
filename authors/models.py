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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        image = Image.open(self.photo)

        width, height = image.size
        left = (width - 200)/2
        top = (height - 200)/2
        right = (width + 200)/2
        bottom = (height + 200)/2        

        # cropped_image = image.crop((100, 100, 200, 200))
        cropped_image = image.crop((left, top, right, bottom))
        resized_image = cropped_image.resize((50, 50), Image.ANTIALIAS)
        resized_image.save((self.photo.path))

    def __str__(self):
        return '%s' % (self.name)       
        