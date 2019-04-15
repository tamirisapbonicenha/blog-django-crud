from django.db import models
from authors.models import Author
from PIL import Image

from django.utils import timezone

def post_image(instance, filename):
    return 'p_{0}/{1}'.format(instance.id, filename)

class Category(models.Model):
    name = models.CharField(max_length=200)
    
    def publish(self):
        self.save()

    def __str__(self):
        return self.name   


# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(Author, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    image = models.ImageField(upload_to=post_image, null=True)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)
    published = models.BooleanField('Publicar?', default=False)
    created_date = models.DateTimeField(
            default=timezone.now)

    def save(self, *args, **kwargs):
        if self.id is None:
            saved_image = self.image
            self.image = None
            super(Post, self).save(*args, **kwargs)
            self.image = saved_image

        super(Post, self).save(*args, **kwargs)         

    def publish(self):
        self.save()

    def __str__(self):
        return self.title
