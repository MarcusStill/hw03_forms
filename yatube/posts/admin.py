from django.contrib import admin

from .models import Group, Post


class PostAdmin(admin.ModelAdmin):
    # поля в админке
    list_display = ('pk', 'text', 'pub_date', 'author', 'group')
    # интерфейс для поиска по тексту постов
    list_editable = ('group',)
    search_fields = ('text',)
    # возможность фильтрации по дате
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


admin.site.register(Post, PostAdmin)
admin.site.register(Group)
