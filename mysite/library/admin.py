from django.contrib import admin
from .models import Genre, Author, Book, BookInstance

class AuthorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'display_books']

class BookInstanceInLine(admin.TabularInline):
    model = BookInstance
    extra = 0
    readonly_fields = ['uuid']
    can_delete = False
    fields = ['uuid', 'due_back', 'status']

class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'isbn', 'author', 'display_genre']
    inlines = [BookInstanceInLine]

class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'book', 'status', 'due_back']
    list_filter = ['status', 'due_back']
    search_fields = ['uuid', 'book__title', 'book__author__last_name']
    list_editable = ['due_back', 'status']

    fieldsets = [
        ('General', {'fields': ('uuid', 'book')}),
        ('Availability', {'fields': ('status', 'due_back')}),
    ]

# Register your models here.
admin.site.register(Genre)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookInstance, BookInstanceAdmin)
