from django.urls import include, path
urlpatterns=[
    path("users/",include("users.api_urls")),path("posts/",include("posts.api_urls")),
    path("media/",include("media_app.api_urls")),path("pregnancy/",include("pregnancy.api_urls")),
    path("hospitals/",include("hospitals.api_urls")),path("chat/",include("chat.api_urls")),
    path("search/",include("search_app.api_urls")),
]
