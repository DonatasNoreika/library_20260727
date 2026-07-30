from django.db import models
import uuid

# Create your models here.

class Genre(models.Model):
    name = models.CharField()

    class Meta:
        verbose_name = "Žanras"
        verbose_name_plural = "Žanrai"

    def __str__(self):
        return self.name

class Author(models.Model):
    first_name = models.CharField()
    last_name = models.CharField()

    def display_books(self):
        return ", ".join(book.title for book in self.books.all())

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Book(models.Model):
    title = models.CharField()
    summary = models.TextField()
    isbn = models.IntegerField()
    genre = models.ManyToManyField(to="Genre")
    author = models.ForeignKey(to="Author", on_delete=models.CASCADE, related_name="books")

    # def display_genre(self):
    #     genres = self.genre.all()
    #     result = ""
    #     for genre in genres:
    #         result += genre.name + ", "
    #     return result

    def display_genre(self):
        return ", ".join(genre.name for genre in self.genre.all())

    display_genre.short_description = "Genre"

    def __str__(self):
        return f"{self.title} - {self.author}"


class BookInstance(models.Model):
    book = models.ForeignKey(to="Book", on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('d', "Administered"),
        ('t', "Taken"),
        ('a', "Available"),
        ('r', "Reserved"),
    )

    status = models.CharField(choices=LOAN_STATUS, max_length=1, default='d')

    def __str__(self):
        return f"{self.uuid} ({self.book.title})"
