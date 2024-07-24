"""
URL configuration for whyteflyte project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from kenonline.views import home, register, my_login, my_logout, store, my_cart, checkout, user_logout, update_item, process_order, cancel_order
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    path('kenonline/', home, name="home"),

    path('my_cart/', my_cart, name="my_cart"),

    path('my_login/', my_login, name="my_login"),

    path('my_logout/', my_logout, name="my_logout"),

    path('register/', register, name="register"),

    path('store/', store, name="store"),

    path('checkout/', checkout, name="checkout"),

    path('user_logout/', user_logout, name="user_logout"),

    path('store/', store, name="store"),

    path('update_item/', update_item, name="update_item"),

    path('process_order/', process_order, name="process_order"),

    path('cancel_order/', cancel_order, name="cancel_order"),

    # path('download/', download, name="download"),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

