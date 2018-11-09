from django.contrib import admin

# Register your models here.
from django.contrib import admin
from ReadingRec.models import Book, Impression

# admin.site.register(Book)
# admin.site.register(Impression)


class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'publisher', 'page', 'created_at')  # 一覧に出したい項目
    list_display_links = ('name',)  # 修正リンクでクリックできる項目


admin.site.register(Book, BookAdmin)

