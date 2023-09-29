from djoser.views import TokenDestroyView
from rest_framework.response import Response
from djoser import utils
from rest_framework import status

class CustomTokenDestroyView(TokenDestroyView):

    def post(self, request, *args, **kwargs):
        utils.logout_user(request)
        return Response(status=status.HTTP_204_NO_CONTENT)
