"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.users.views import RegisterViewRole,TutorView,TutorSkillView,EstudianteView,EstudianteSkillView,logout_post, SkillMatchView, TutoringSessionView, ReviewView, CustomTokenObtainPairView, CustomRefreshTokenView, mi_perfil_tutor, mi_perfil_estudiante, ConversacionView, MensajeView, PagoView, ReembolsoView


router = DefaultRouter()

router.register(r'register',RegisterViewRole)
router.register(r'tutor_cuenta',TutorView)
router.register(r'estudiante_cuenta',EstudianteView)
router.register(r'tutor_skill',TutorSkillView)
router.register(r'estudiante_skill',EstudianteSkillView)
router.register(r'skill_match', SkillMatchView)
router.register(r'conversacion',ConversacionView)
router.register(r'mensaje',MensajeView)
router.register(r'tutoria',TutoringSessionView)
router.register(r'pago',PagoView)
router.register(r'reembolso',ReembolsoView)
router.register(r'review',ReviewView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tutor_perfil/',mi_perfil_tutor, name="perfil_tutor"),
    path('estudiante_perfil/',mi_perfil_estudiante, name="perfil_estudiante"),
    path('api/', include(router.urls)),
    path('api-auth/',include('rest_framework.urls')),
    path('logout/',logout_post, name="logout"),
    path('login/', CustomTokenObtainPairView.as_view(), name="token"),
    path('refresh/',CustomRefreshTokenView.as_view() , name="token_refresh"),
]
