from django.db import models
from django.utils import timezone

from PIL import Image

from django.db.models import signals
from myblog.utils import unique_slug_generator

from authors.models import Author
from categories.models import Category

def post_image(instance, filename):
    return 'p_{0}/{1}'.format(instance.id, filename)

class Post(models.Model):
    created_date = models.DateTimeField(
            default=timezone.now)
    author = models.ForeignKey(Author, null=True, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=256)
    text = models.TextField()
    image = models.ImageField(upload_to=post_image, null=True)
    published = models.BooleanField('Publicar?', default=False)
    visit_count = models.IntegerField(default=0)
    slug = models.SlugField(max_length=200, null=True, blank=True)

    def add_visit(self):
        if self.visit_count is not None:
            self.visit_count += 1
        else:
            self.visit_count = 0
    
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


def pre_save_receiver(sender, instance, *args, **kwargs):
   if not instance.slug:
       instance.slug = unique_slug_generator(instance)


signals.pre_save.connect(pre_save_receiver, sender = Post)