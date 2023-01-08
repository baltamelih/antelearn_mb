from django.db import models
from django.utils.text import slugify


class series(models.Model):
    series_id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    series_name = models.CharField(max_length=100)
    description = models.TextField()
    slug = models.SlugField(null=False,unique=True,db_index=True,blank=True)
    series_img = models.ImageField(upload_to='img')
    def save(self,*args,**kwargs):
        self.slug = slugify(self.series_id)
        super().save(*args,**kwargs)
class registerUser(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    telephone_number = models.CharField(max_length=11)
    repeat_password = models.CharField(max_length=100)
    role = models.CharField(max_length=30)

class season(models.Model):
    season_id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    series_name = models.CharField(max_length=255)
    season_no = models.IntegerField()
class episode(models.Model):
    series_id = models.IntegerField()
    season_id = models.IntegerField()
    episode_id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    episode_name = models.CharField(max_length=255)
    episode_no =models.CharField(max_length=50)
    episode_filepath = models.CharField(max_length=255)
    episode_img = models.ImageField(upload_to='img')
    def __str__(self):
        return str(self.episode_id)
class words(models.Model):
    words_id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    series_id = models.IntegerField()
    season_id = models.IntegerField()
    episode_id = models.IntegerField()
    word = models.CharField(max_length=255)
    count = models.IntegerField()
    translation = models.CharField(max_length=255)
class most_used_words(models.Model):
    word = models.CharField(max_length=255)
    translation = models.CharField(max_length=255)
class patterns(models.Model):

    patterns = models.CharField(max_length=255)
    translation = models.CharField(max_length=255)
    definition = models.CharField(max_length=255)
class game(models.Model):
    words_id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    word = models.CharField(max_length=255)
    translation = models.CharField(max_length=255)
    count = models.IntegerField()

