from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('', include('games.urls')),
    path('alias/', include('alias.urls')),
    path('pig/', include('pig.urls', namespace='pig')),
    path('mafia/', include('mafia.urls')),
    path('who_am_i/', include('who_am_i.urls')),
    path('puzzle/', include('puzzle.urls')),
    path('five_seconds/', include('five_seconds.urls')),
    path('danetki/', include('danetki.urls')),
    path('never_have_i_ever/', include('never_have_i_ever.urls')),
    path('dilemma/', include('dilemma.urls')),
    path('crocodile/', include('crocodile.urls')),
    path('games/', include('games.urls')),
    

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)