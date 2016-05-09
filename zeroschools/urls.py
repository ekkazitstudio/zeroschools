from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from . import views

urlpatterns = [
	url(r'^admin/', include(admin.site.urls)),
	url(r'^tinymce/', include('tinymce.urls')),
	url(r'^mce_filebrowser/', include('mce_filebrowser.urls')),
	url(r'^$', views.index, name='index'),
	url(r'^blog/', include('blog.urls', namespace='blog')),
	url(r'^course/', include('course.urls', namespace='course')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_title = 'ZeroSchools'
admin.site.site_header = 'ZeroSchools Administration'
