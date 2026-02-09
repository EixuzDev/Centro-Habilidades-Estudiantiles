from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from .serializer import RegisterSerializer,EstudianteCuentaSerializer,CustomTokenObtainPairSerializer, TutorCuentaSerializer,SkillMatchSerializer, TutoringSessionSerializer,ReviewSerializer, TutorSkillSerializer, TutorProfileSerializer, EstudianteSkillSerializer, EstudianteProfileSerializer, ConversacionSerializer, MensajeSerializer, PagoSerializer, ReembolsoSerializer
from .models import User,Crear_Cuenta_Tutor,Crear_Cuenta_Estudiante , SkillMatch, TutoringSession, Review, TutorSkill, EstudianteSkill, Conversacion, Mensajes, Pago, Reembolso
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .permission import IsTutor, IsEstudiante, IsAdmin
from .throttle import Profile_Estudiante
# Create your views here.

class RegisterViewRole(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [IsAuthenticated]

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self,request,*args,**kwargs):
        serializer = CustomTokenObtainPairSerializer(data = request.data)

        try:
            serializer.is_valid()
            response = super().post(request,*args,**kwargs)
            tokens = response.data
        except:
            return Response({'Error':'Credenciales Invalidas'}, status=status.HTTP_400_BAD_REQUEST)

        tokens = serializer.validated_data

        access_token = tokens['access']
        refresh_token = tokens['refresh']

        res = Response()

        res.data = {'Mensaje':'Login Exitoso'}

        res.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=True,
                samesite='None',
                path='/',
                max_age=900 #15 minutos

            )

        res.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                secure=True,
                samesite='None',
                path='/',
                max_age=1800 # 30 minutos
            )

        return res
    

class CustomRefreshTokenView(TokenRefreshView):
    def post(self,request, *args, **kwargs):

        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({'Error':'Falta el token de Autorizacion'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            request.data['refresh'] = refresh_token
            response = super().post(request, *args, **kwargs)
            tokens = response.data
            access_token = tokens['access']

            response = Response({
            'Mensaje': 'Token Refrescado'
            }, status=status.HTTP_200_OK)
        
            response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=True,
            samesite='None',
            path='/'
            )

            return response
        except:
            return Response({
                'Error': 'Token refresh invalido'
            }, status=status.HTTP_401_UNAUTHORIZED)
           

@api_view(['POST'])
def logout_post(request):
    try:
        response = Response({'mensaje': 'Logout exitoso!'})
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response
    except:
        return Response({'Error'}, status=status.HTTP_400_BAD_REQUEST)


class TutorView(ModelViewSet):
    queryset = Crear_Cuenta_Tutor.objects.all()
    serializer_class = TutorCuentaSerializer
    permission_classes = [IsAuthenticated, IsTutor]
    
    def get_queryset(self):
        user = self.request.user

        return Crear_Cuenta_Tutor.objects.filter(user=user)
    
    def perform_create(self, serializer):
        user = self.request.user
        if Crear_Cuenta_Tutor.objects.filter(user=user).exists():
            raise ValueError('Ya tienes un perfil Creado')
        serializer.save(user=user)

class TutorSkillView(ModelViewSet):
    queryset = TutorSkill.objects.all()
    serializer_class = TutorSkillSerializer
    permission_classes = [IsAuthenticated, IsTutor]
    
    def get_queryset(self):
        user = self.request.user

        return TutorSkill.objects.filter(tutor_profile__user=user)
    
    def perform_create(self, serializer):
        user = self.request.user

        try:
            perfil = Crear_Cuenta_Tutor.objects.get(user=user)

        except Crear_Cuenta_Tutor.DoesNotExist:
            raise ValueError('Debes Crearte una Cuenta')
        
        serializer.save(tutor_profile=perfil)


@api_view(['GET','DELETE'])
@permission_classes([IsAuthenticated, IsTutor])
def mi_perfil_tutor(request):
    try:
        perfil = Crear_Cuenta_Tutor.objects.prefetch_related("skills").get(user=request.user)
    except Crear_Cuenta_Tutor.DoesNotExist:
        return Response({'Mensaje':'No tienes una cuenta creada'}, status=status.HTTP_404_NOT_FOUND)


    if request.method == 'GET':
        serializer = TutorProfileSerializer(perfil)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
    if request.method == 'DELETE':
        perfil.delete()
        return Response({'Mensaje':'Perfil eliminado correctamente'}, status=status.HTTP_200_OK)

class EstudianteView(ModelViewSet):
      queryset = Crear_Cuenta_Estudiante.objects.all()
      serializer_class = EstudianteCuentaSerializer
      permission_classes = [IsAuthenticated,IsEstudiante]

      def get_queryset(self):
        user = self.request.user

        return Crear_Cuenta_Estudiante.objects.filter(user=user)
    
      def perform_create(self, serializer):
        user = self.request.user
        if Crear_Cuenta_Estudiante.objects.filter(user=user).exists():
            raise ValueError('Ya tienes un perfil Creado')
        serializer.save(user=user)

class EstudianteSkillView(ModelViewSet):
    queryset = EstudianteSkill.objects.all()
    serializer_class = EstudianteSkillSerializer
    permission_classes = [IsAuthenticated,IsEstudiante]

    def get_queryset(self):
        user = self.request.user

        return EstudianteSkill.objects.filter(estudiante_profile__user=user)
        
    def perform_create(self, serializer):
        user = self.request.user

        try:
            perfil = Crear_Cuenta_Estudiante.objects.get(user=user)

        except Crear_Cuenta_Estudiante.DoesNotExist:
            raise ValueError('Debes Crearte una Cuenta')
        
        serializer.save(estudiante_profile=perfil)
      

@api_view(['GET','DELETE'])
@permission_classes([IsAuthenticated, IsEstudiante])
def mi_perfil_estudiante(request):
    try:
        perfil = Crear_Cuenta_Estudiante.objects.prefetch_related("skills").get(user=request.user)
    except Crear_Cuenta_Estudiante.DoesNotExist:
        return Response({'Mensaje':'No tienes una cuenta creada'})

    if request.method == 'GET':
        serializer = EstudianteProfileSerializer(perfil)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    if request.method == 'DELETE':
        perfil.delete()
        return Response({'Mensaje':'Perfil eliminado correctamente'}, status=status.HTTP_200_OK)

    
class SkillMatchView(ModelViewSet):
    queryset = SkillMatch.objects.all()
    serializer_class = SkillMatchSerializer
    permission_classes = [IsAuthenticated,IsEstudiante]
    def get_queryset(self):
          user = self.request.user
          return SkillMatch.objects.filter(estudiante__user=user)
      
    def perform_create(self,serializer):
        user = self.request.user

        try:
            estudiante_profile = Crear_Cuenta_Estudiante.objects.get(user=user)
        except Crear_Cuenta_Estudiante.DoesNotExist:
          raise ValueError('Debes crear tu cuenta primero')

        estudiante_skill = serializer.validated_data.get('estudiante_skill')

        tutor_profile = serializer.validated_data.get("tutor")

        if not estudiante_skill:
            raise ValueError('Debes Seleccionar una habilidad del estudiante')
        
        if not tutor_profile:
            raise ValueError('Debes seleccionar un tutor')
        
        if estudiante_skill.estudiante_profile != estudiante_profile:
            raise ValueError('No puedes usar habilidades de otro estudiante')
        
        skill_tutor = TutorSkill.objects.filter(
            tutor_profile=tutor_profile,
            habilidad__iexact=estudiante_skill.habilidad,
            dia_disponible=estudiante_skill.dia_disponible,
            nivel_experiencia__gte=estudiante_skill.nivel_experiencia
        ).first()

        if not skill_tutor:
            raise ValueError('Este tutor no posee los requerimientos que buscas')
        

        serializer.save(
            estudiante = estudiante_profile,
            skills_tutor=skill_tutor
        )

class ConversacionView(ModelViewSet):
    queryset = Conversacion.objects.all()
    serializer_class = ConversacionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "estudiante":
            return Conversacion.objects.filter(match__estudiante__user=user)
        if user.role == "tutor":
            return Conversacion.objects.filter(match__tutor__user=user)

class MensajeView(ModelViewSet):
    queryset = Mensajes.objects.all()
    serializer_class = MensajeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == "estudiante":
            return Mensajes.objects.filter(conversacion__match__estudiante__user=user)
        
        if user.role == "tutor":
            return Mensajes.objects.filter(conversacion__match__tutor__user=user)
        
        return Mensajes.objects.none()
    
    def perform_create(self, serializer):
        user = self.request.user
        conversacion = serializer.validated_data['conversacion']

        match = conversacion.match

        es_estudiante = match.estudiante.user == user
        es_tutor = match.tutor.user == user

        if not(es_estudiante or es_tutor):
            raise ValueError('No puedes enviar mensaje en esta conversacion')
        
        existe_mensaje = Mensajes.objects.filter(conversacion=conversacion).exists()

        if not existe_mensaje:
            if not es_estudiante:
                raise ValueError('Solo el estudiante puede iniciar el chat')
            
        serializer.save(enviados=user)

class TutoringSessionView(ModelViewSet):
      queryset = TutoringSession.objects.all()
      serializer_class = TutoringSessionSerializer
      permission_classes = [IsAuthenticated]

      def get_queryset(self):
          user = self.request.user

          if user.role =="estudiante":
              return TutoringSession.objects.filter(match__estudiante__user=user)
          if user.role=="tutor":
              return TutoringSession.objects.filter(match__tutor__user=user)
          
          return TutoringSession.objects.none()
      
      def perform_create(self, serializer):
          user = self.request.user

          if user.role !="estudiante":
            raise ValueError('Solo los estudiantes pueden crear una tutoria')
          
          try:
            estudiante_profile = Crear_Cuenta_Estudiante.objects.get(user=user)
          except Crear_Cuenta_Estudiante.DoesNotExist:
            raise ValueError('Debes crearte una cuenta primero')
          
          match = serializer.validated_data.get("match")

          if match.estudiante != estudiante_profile:
            raise ValueError('No puedes crear tutorias que no son tuyos')
          
          if TutoringSession.objects.filter(match=match).exists():
              raise ValueError('esta tutoria ya esta creada')
          
          serializer.save()
            

class PagoView(ModelViewSet):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "estudiante":
            return Pago.objects.filter(tutoria__match__estudiante__user=user)
        
        if user.role == "tutor":
            return Pago.objects.filter(tutoria__match__tutor__user=user)
        
        return Pago.objects.none()
    
    def perform_create(self, serializer):
        user = self.request.user
        tutoria = serializer.validated_data["tutoria"]

        match = tutoria.match

        if match.estudiante.user !=user:
            raise ValueError("Solo el estudiante match puede pagar la tutoria")


        if Pago.objects.filter(tutoria=tutoria).exists():
            raise ValueError('Esta tutoria ya tiene pago registrado')
        

        serializer.save(estado="pagado")

class ReembolsoView(ModelViewSet):
    queryset=Reembolso.objects.all()
    serializer_class = ReembolsoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == "estudiante":
            return Reembolso.objects.filter(pago__tutoria__match__estudiante__user=user)
        if user.role == "tutor":
            return Reembolso.objects.filter(pago__tutoria__match__tutor__user=user)
        

    def perform_create(self, serializer):
        user = self.request.user

        pago = serializer.validated_data["pago"]

        match = pago.tutoria.match

        if match.estudiante.user !=user:
            raise ValueError('Solo el estudiante puede solicitar reembolso')
        
        if pago.estado != "pagado":
            raise ValueError('Solo puedes pedir reembolso si el pago está en estado pagado.')
        
        if Reembolso.objects.filter(pago=pago).exists():
            raise ValueError('Ya existe una solicitud de reembolso para este pago.')
        
        serializer.save()

class ReviewView(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role =="tutor":
            return Review.objects.filter(tutor__user=user)


    def perform_create(self, serializer):
        user = self.request.user

        if user.role == "tutor":
            raise ValueError('Los tutores no pueden crear reseñas')
        
        tutoria = serializer.validated_data["tutoria"]

        if user.role != "estudiante":
            raise ValueError('Solo los estudiante pueden crear reseñas')

        if tutoria.match.estudiante.user != user:
            raise ValueError('No puedes reseñar una tutoria que no es tuya')
        
        if tutoria.estado != "finalizada":

            raise ValueError('Solo puedes reseñar una tutoría finalizada.')
        
        serializer.save(
            tutor=tutoria.match.tutor,
            estudiante=tutoria.match.estudiante
        )
          

