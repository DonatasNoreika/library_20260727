from django.contrib.auth.models import User
from django.db import models
import uuid
from django.utils import timezone
from tinymce.models import HTMLField
from PIL import Image

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="profile_pics", null=True, blank=True)

    def save(self, *, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
        if self.photo:
            img = Image.open(self.photo.path)
            min_side = min(img.width, img.height)
            left = (img.width - min_side) // 2
            top = (img.height - min_side) // 2
            right = left + min_side
            bottom = top + min_side
            img = img.crop((left, top, right, bottom))
            img = img.resize((300, 300), Image.LANCZOS)
            img.save(self.photo.path)

    def __str__(self):
        return f"{self.user.username} profile"

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
    description = HTMLField(default="")

    def display_books(self):
        return ", ".join(book.title for book in self.books.all())

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Book(models.Model):
    title = models.CharField()
    summary = models.TextField()
    isbn = models.IntegerField()
    genre = models.ManyToManyField(to="Genre")
    author = models.ForeignKey(to="Author",
                               on_delete=models.CASCADE,
                               related_name="books")
    cover = models.ImageField(upload_to="covers", null=True, blank=True)

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
    book = models.ForeignKey(to="Book",
                             on_delete=models.CASCADE,
                             related_name="instances")
    uuid = models.UUIDField(default=uuid.uuid4)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('d', "Administered"),
        ('t', "Taken"),
        ('a', "Available"),
        ('r', "Reserved"),
    )

    status = models.CharField(choices=LOAN_STATUS, max_length=1, default='d')
    reader = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=True)

    def is_overdue(self):
        return self.due_back and timezone.now().date() > self.due_back

    def __str__(self):
        return f"{self.uuid} ({self.book.title})"

    class Meta:
        ordering = ['-pk']


class BookReview(models.Model):
    book = models.ForeignKey(to="Book",
                             on_delete=models.SET_NULL,
                             null=True, blank=True,
                             related_name="reviews")
    author = models.ForeignKey(to=User,
                               on_delete=models.SET_NULL,
                               null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return self.content

