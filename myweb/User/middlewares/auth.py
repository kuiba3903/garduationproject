from django.utils.deprecation import MiddlewareMixin
from User.models import User

class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user_id = request.session.get("user_id", 0)
        user_object = User.objects.filter(id=user_id).first()
        request.user = user_object

