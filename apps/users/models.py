from django.db import models
from django.contrib.auth.models import AbstractUser , UserManager
# Create your models here. 
 
class CustomUserManager(UserManager):
    def create_superuser(self, username, email, password):
        user = self.create_user(
            username=username,
            email=email,
            password=password,
            role='admin'
        )
        user.is_staff = True
        user.is_superuser=True
        user.save()
        return user

class User(AbstractUser):
    ROLE_CHOICES =[
        ('tutor','Tutor'),
        ('estudiante', 'Estudiante'),
    ]
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = CustomUserManager()


class Crear_Cuenta_Tutor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="tutor_account")
    tipo = models.CharField(max_length=10,default="ofrece", editable=False)
    biografia = models.TextField()
    titulo_profesional = models.CharField(max_length=150)


class TutorSkill(models.Model):

    NIVEL_EXPERIENCIA = [
        (1, "Básico"),
        (2, "Intermedio"),
        (3, "Avanzado"),
    ]

    DIAS = [
        (1, "Lunes"),
        (2, "Martes"),
        (3, "Miércoles"),
        (4, "Jueves"),
        (5, "Viernes"),
        (6, "Sábado"),
        (7, "Domingo"),
    ]

    tutor_profile = models.ForeignKey(
        Crear_Cuenta_Tutor,
        on_delete=models.CASCADE,
        related_name="skills"
    )

    habilidad = models.CharField(max_length=100)
    nivel_experiencia = models.PositiveSmallIntegerField(choices=NIVEL_EXPERIENCIA)
    dia_disponible = models.PositiveSmallIntegerField(choices=DIAS)



class Crear_Cuenta_Estudiante(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="estudiante_account")
    tipo = models.CharField(max_length=10,default="busca",editable=False)
    biografia = models.TextField(blank=True)


class EstudianteSkill(models.Model):
    NIVEL_EXPERIENCIA = [
        (1, "Básico"),
        (2, "Intermedio"),
        (3, "Avanzado"),
    ]

    DIAS = [
        (1, "Lunes"),
        (2, "Martes"),
        (3, "Miércoles"),
        (4, "Jueves"),
        (5, "Viernes"),
        (6, "Sábado"),
        (7, "Domingo"),
    ]

    estudiante_profile = models.ForeignKey(
        Crear_Cuenta_Estudiante,
        on_delete=models.CASCADE,
        related_name="skills"
    )

    habilidad = models.CharField(max_length=100)
    nivel_experiencia = models.PositiveSmallIntegerField(choices=NIVEL_EXPERIENCIA)
    dia_disponible = models.PositiveSmallIntegerField(choices=DIAS)


class SkillMatch(models.Model):
    tutor = models.ForeignKey(Crear_Cuenta_Tutor, related_name='matches_tutor', on_delete=models.CASCADE)
    estudiante = models.ForeignKey(Crear_Cuenta_Estudiante, related_name='estudiante_matches', on_delete=models.CASCADE)
    estudiante_skill = models.ForeignKey(EstudianteSkill, related_name='estudiante_skill', on_delete=models.CASCADE)
    skills_tutor = models.ForeignKey(TutorSkill, related_name='skill_tutor', on_delete=models.CASCADE)


class Conversacion(models.Model):
    match = models.OneToOneField(SkillMatch,on_delete=models.CASCADE,related_name='conversacion')

class Mensajes(models.Model):
    conversacion = models.ForeignKey(Conversacion,on_delete=models.CASCADE)
    enviados = models.ForeignKey(User,on_delete=models.CASCADE, related_name='mensajes_enviados')
    text = models.TextField()

class TutoringSession(models.Model):
    match = models.OneToOneField(SkillMatch, on_delete=models.CASCADE, related_name='tutorias')
    fecha = models.DateTimeField()
    estado = models.CharField(
        max_length=15,
        choices=[
            ('pendiente', 'Pendiente'),
            ('confirmada', 'Confirmada'),
            ('finalizada', 'Finalizada'),
            ('cancelada', 'Cancelada'),
        ]
    )

class Pago(models.Model):
    METODOS = [
        ("transferencia", "Transferencia"),
        ("pago_movil", "Pago Móvil"),
        ("efectivo", "Efectivo"),
    ]

    ESTADOS = [
        ("pendiente", "Pendiente"),
        ("pagado", "Pagado"),
        ("reembolsado", "Reembolsado"),
        ("rechazado", "Rechazado"),
    ]

    tutoria = models.OneToOneField(TutoringSession, on_delete=models.CASCADE, related_name='pago')

    monto = models.DecimalField(max_digits=10, decimal_places=2)
    metodo = models.CharField(max_length=20,choices=METODOS)
    estado = models.CharField(max_length=20, choices=ESTADOS)

    descripcion = models.CharField(max_length=100, blank=True, null=True)


class Reembolso(models.Model):
    pago = models.OneToOneField(Pago, on_delete=models.CASCADE, related_name='reembolso')
    motivo = models.TextField()

    estado = models.CharField(max_length=20, choices=[
        ("solicitado", "Solicitado"),
        ("aprobado", "Aprobado"),
        ("rechazado", "Rechazado"),
    ])

class Review(models.Model):
    tutoria = models.OneToOneField(TutoringSession, on_delete=models.CASCADE)

    tutor = models.ForeignKey(Crear_Cuenta_Tutor,on_delete=models.CASCADE,related_name='reviews')
    estudiante = models.ForeignKey(Crear_Cuenta_Estudiante, on_delete=models.CASCADE,related_name='reviews')

    calificacion = models.PositiveSmallIntegerField(
        choices=[
            (1,'Muy Malo'),
            (2,'Malo'),
            (3,'Bueno'),
            (4,'Muy Bueno'),
            (5,'Excelente')
        ],
    )

    comentario = models.TextField(blank=True)
    fecha = models.DateTimeField(auto_now_add=True)