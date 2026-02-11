from rest_framework import serializers
from .models import User, Crear_Cuenta_Tutor,Crear_Cuenta_Estudiante, SkillMatch, TutoringSession, Review, TutorSkill, EstudianteSkill, Conversacion, Mensajes, Pago, Reembolso
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username','email', 'password', 'role')

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            role=validated_data.get('role')
        )

        user.set_password(validated_data['password'])
        user.save()
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['email'] = user.email
        token['role'] = user.role

        return token

class TutorCuentaSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    class Meta:
        model = Crear_Cuenta_Tutor
        fields = ['id','username','biografia','tipo','titulo_profesional']

class TutorSkillSerializer(serializers.ModelSerializer):
    tutor_profile_user=serializers.CharField(source="tutor_profile.user.username",read_only=True)
    class Meta:
        model = TutorSkill
        fields = ['id','tutor_profile_user','habilidad','nivel_experiencia','dia_disponible']

class TutorProfileSerializer(serializers.ModelSerializer):
    skills = TutorSkillSerializer(many=True, read_only=True)
    username = serializers.CharField(source="user.username",read_only=True)

    class Meta:
        model = Crear_Cuenta_Tutor
        fields = ['id','username','biografia','tipo','titulo_profesional','skills']
        

class EstudianteCuentaSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    class Meta:
        model = Crear_Cuenta_Estudiante
        fields = ['id','username','biografia','tipo']

class EstudianteSkillSerializer(serializers.ModelSerializer):
    estudiante_profile_user=serializers.CharField(source="estudiante_profile.user.username", read_only=True)
    class Meta:
        model = EstudianteSkill
        fields = ['id','estudiante_profile_user','habilidad','nivel_experiencia','dia_disponible']

class EstudianteProfileSerializer(serializers.ModelSerializer):
    skills = EstudianteSkillSerializer(many=True, read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    class Meta:
        model = Crear_Cuenta_Estudiante
        fields = ['id','username','biografia','tipo','skills']


class SkillMatchSerializer(serializers.ModelSerializer):
    tutor_username = serializers.CharField(source="tutor.user.username", read_only=True)
    estudiante_username=serializers.CharField(source="estudiante.user.username", read_only=True)
    estudiante_skill_detalle = EstudianteSkillSerializer(source="estudiante_skill", read_only=True)
    skill_tutor_detalle = TutorSkillSerializer(source="skills_tutor",read_only=True)


    class Meta:
        model = SkillMatch
        fields = ['id','tutor','tutor_username','estudiante','estudiante_username','estudiante_skill','estudiante_skill_detalle','skill_tutor_detalle']

class ConversacionSerializer(serializers.ModelSerializer):
    tutor = serializers.CharField(source="match.tutor.user.username", read_only=True)
    estudiante = serializers.CharField(source="match.estudiante.user.username", read_only=True)

    class Meta:
        model = Conversacion
        fields =['id','match','tutor','estudiante']

class MensajeSerializer(serializers.ModelSerializer):
    usuario_enviado = serializers.CharField(source="enviados.username",read_only=True)

    class Meta:
        model = Mensajes
        fields = ['id','conversacion','usuario_enviado','text']

class TutoringSessionSerializer(serializers.ModelSerializer):
    tutor_username=serializers.CharField(source="match.tutor.user.username", read_only=True)
    estudiante_username=serializers.CharField(source="match.estudiante.user.username", read_only=True)
    class Meta:
        model = TutoringSession
        fields = ['id', 'match','tutor_username','estudiante_username','fecha','estado']

class PagoSerializer(serializers.ModelSerializer):
    estudiante_username = serializers.CharField(source="tutoria.match.estudiante.user.username", read_only=True)
    tutor_username = serializers.CharField(source="tutoria.match.tutor.user.username", read_only=True)

    class Meta:
        model = Pago
        fields = ['id','tutoria','metodo','monto','estado','estudiante_username','tutor_username','descripcion']

class ReembolsoSerializer(serializers.ModelSerializer):
    estudiante_username=serializers.CharField(source="pago.tutoria.match.estudiante.user.username",read_only=True)
    tutor_username = serializers.CharField(source="pago.tutoria.match.tutor.user.username", read_only=True)

    class Meta:
        model = Reembolso
        fields = ['id','pago','motivo','estado','estudiante_username','tutor_username']


class ReviewSerializer(serializers.ModelSerializer):
    tutor_username = serializers.CharField(source="tutor.user.username", read_only=True)
    estudiante_username = serializers.CharField(source="estudiante.user.username",read_only=True)
    class Meta:
        model = Review
        fields = ['id','tutoria','tutor_username','estudiante_username','comentario','calificacion','fecha']



        
