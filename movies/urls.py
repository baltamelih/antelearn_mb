from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path ("login/",views.loginUser,name="login"),
    path ("register/",views.register,name="register"),
    path ("homepage/",views.homePage,name="home"),
    path ("",views.homePage),
    path ("series/",views.ser,name="series"),
    path ("",views.logout,name="logout"),
    path ("jumbbledgame/",views.jumbbledGame,name="jumbbledgame"),
    path ("/series/<int:series_id>/<int:season_no>/<int:episode_id>",views.seriesgame,name="seriesgame"),
    path ("series/<int:series_id>/<int:season_no>/<int:episode_id>",views.series_to_game,name="seriestogame"),
    path ("series/<int:series_id>/",views.dropdown,name="dropdown"),
    path ("series/<int:series_id>/<int:season_no>/",views.episode,name="episode"),
    path ("price/",views.price,name="price"),
    path ("/control/",views.controlJumbbled,name="controljumbbled"),
    path ("point-table/",views.pointtable,name="pointtable"),
    path ("/admin",views.admin,name="admin"),
    path ("hexagongame/",views.hexagongame,name="hexagongame"),



]
urlpatterns +=  static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
