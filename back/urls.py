
from django.contrib import admin
from django.urls import path, include
from api.views import ProfileAPIView,LogTrainingView,ChallengeViewSet
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/dj-rest-auth/", include("dj_rest_auth.urls")),
    path("api/dj-rest-auth/registration/", include("dj_rest_auth.registration.urls")),
    path('api/profile/', ProfileAPIView.as_view(), name='profile_api'),
    path('api/logtraining/', LogTrainingView.as_view(), name='logtraining'),path('api/challenges/', ChallengeViewSet.as_view({'get': 'list', 'post': 'create'}), name='challenge-list'),
    path('api/challenges/', ChallengeViewSet.as_view({'get': 'list', 'post': 'create'}), name='challenge-list'),
    path('api/challenges/<int:challenge_id>/', ChallengeViewSet.as_view({'get': 'retrieve', 'delete': 'destroy', 'post': 'create'}), name='challenge-detail'),
]
urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)