from django.contrib import admin

from .models import Post

class PostAdmin(admin.ModelAdmin):
    actions = ['make_published']
    # fields = (('author'), 'title', 'text', ('category', 'image'), ('published', 'slug'))
    # fieldsets = (
    #     ('Dados', { 'fields': ('author', 'title') }),
    #     ('Dados complementares', {
    #         'classes': ('collapse',),
    #         'fields': ('category', 'image', 'published', 'slug')
    #     }),
    # )
    list_display = ['author', 'title', 'category', 'image', 'published']
    list_filter = ('author', 'category')
    search_fields = ('author', )

    def make_published(self, request, queryset):
        rows_updated = queryset.update(published=1)
        if rows_updated == 1:
            message_bit = "1 post foi"
        else:
            message_bit = "%s posts foram" % rows_updated
        self.message_user(request, "%s marcados como publicados." % message_bit)
    make_published.short_description = "Marque os posts selecionados como publicados"


admin.site.register(Post, PostAdmin)
