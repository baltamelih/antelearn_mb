from django.contrib import admin
from .models import series,words,season,episode,most_used_words,patterns
from .models import registerUser,game
# Register your models here.
admin.site.register(series)
admin.site.register(registerUser)
admin.site.register(words)
admin.site.register(season)
admin.site.register(most_used_words)
admin.site.register(patterns)
admin.site.register(episode)
admin.site.register(game)

