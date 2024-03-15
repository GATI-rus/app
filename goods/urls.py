from django.urls import path
from goods import views

app_name = 'goods'

urlpatterns = [
   path('search/', views.catalog, name='search'),
   path('<slug:category_slug>/', views.catalog, name='index'),
   path('product/<slug:product_slug>/', views.product, name='product'),
   path('product/<slug:add_comment_slug>/', views.add_comment, name='add_comment'),
   path('product/<slug:product_comments_slug>/', views.product_comments, name='product_comment'),
]

