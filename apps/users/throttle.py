from rest_framework.throttling import UserRateThrottle


class Profile_Estudiante(UserRateThrottle):
    scope = 'estudiante'