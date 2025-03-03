from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status'] # Поля, которые будут отображаться в ListView
    list_filter = ['status', 'created', 'publish', 'author'] # Добавление боковой панели фильтр по указанным поляи
    search_fields = ['title', 'body'] # Добавлен поиск и указаны поля, к которым применяется поиск
    prepopulated_fields = {'slug': ('title', )} # Заполняй поле slug вводимыми данными в соотвествии с title
    raw_id_fields = ['author'] # Поле автор теперь отображается с поисковым виджетом, который будет заменён вместо выпадающего списка
    date_hierarchy = 'publish' # Добавление навигационных ссылок по датам
    ordering = ['status', 'publish'] # Критерии сортировки по умолчанию
