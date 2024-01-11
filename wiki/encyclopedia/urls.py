from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search/", views.search, name="search"),
    path('new/', views.new, name="new"),
    path('edit/', views.edit, name="edit"),
    path('save_edit', views.save_edit, name="save_edit")
]



'''
Entry Page: Visiting /wiki/TITLE, where TITLE is the title of an encyclopedia entry, should render a page that displays the contents of that encyclopedia entry.
    The view should get the content of the encyclopedia entry by calling the appropriate util function.
    If an entry is requested that does not exist, the user should be presented with an error page indicating that their requested page was not found.
    If the entry does exist, the user should be presented with a page that displays the content of the entry. The title of the page should include the name of the entry.
'''