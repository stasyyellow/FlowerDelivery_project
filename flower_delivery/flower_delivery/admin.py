from django.contrib import admin
from .models import Review, Slide

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'created_at')
    search_fields = ('user__username', 'text')
    list_filter = ('created_at',)

@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ('title',)  # Отображаем только название слайда
    search_fields = ('title', 'description')  # Поиск по названию и описанию
