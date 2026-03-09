from django.urls import path, include
from rest_framework_nested import routers
router = routers.DefaultRouter()

urlpatterns = [
    path('',include(router.urls)),
    path('qr/', include('qr_master.urls'), name='qr-master'),
    path('keep/', include('keep_note.urls'), name='keep-notes'),
    path('convert/', include('pw_converter.urls'), name='pw-converter'),

    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
