from rest_framework.throttling import UserRateThrottle


class Estudiante_Throttling(UserRateThrottle):
    scope = 'estudiante_throttling'

class Tutor_Throttling(UserRateThrottle):
    scope = 'tutor_throttling'

class General_Throttling(UserRateThrottle):
    scope = 'general_throttling'