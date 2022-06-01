from django.urls import path, include

from product import views

urlpatterns = [
    path('latest-products/', views.LatestProductList.as_view()),
    path('products/search/', views.search),
    path('products/category=<slug:category_slug>/product=<slug:product_slug>/',
         views.ProductDetail.as_view()),
    path('products/category=<slug:category_slug>/', views.CategoryDetail.as_view()),
    path('products/all/', views.AllProductList.as_view()),
    path('products/count/', views.ProductCount.as_view()),
    path('products/add/', views.AddProduct.as_view()),
    path('products/delete/', views.DeleteProduct.as_view()),
    path('products/update/', views.UpdateProduct.as_view()),
]
