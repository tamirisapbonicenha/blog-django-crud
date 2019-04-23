from django.contrib import admin
import decimal, csv
from django.http import HttpResponse
from .models import Post, Category

def export_posts_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="posts.csv"'
    writer = csv.writer(response)
    writer.writerow(['Autor', 'Título', 'Categoria', 'Publicado'])
    posts = queryset.values_list('author', 'title', 'category', 'published',)
    for post in posts:
        writer.writerow(post)
    return response
export_posts_csv.short_description = 'Exportar para csv' 


class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'title', 'category', 'published']
    actions = ['make_published', export_posts_csv]  

    def make_published(self, request, queryset):
        rows_updated = queryset.update(published=1)
        if rows_updated == 1:
            message_bit = "1 post foi"
        else:
            message_bit = "%s posts foram" % rows_updated
        self.message_user(request, "%s marcados como publicados." % message_bit)
    make_published.short_description = "Marque os posts selecionados como publicados"

# admin.site.add_action(export_as_json)
admin.site.register(Post, PostAdmin)
admin.site.register(Category)

