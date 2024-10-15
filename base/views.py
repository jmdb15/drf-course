import requests, os
from dotenv import load_dotenv
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.conf import settings

# Create your views here.


@api_view(['POST'])
def login(request):
    load_dotenv()
    
    user = request.data.get('username')
    password = request.data.get('password')

    
    token_url = f"{settings.OAUTH2_PROVIDER_URL}/token/"
    client_id = os.environ.get('OAUTH2_CLIENT_ID')
    client_secret = os.environ.get('OAUTH2_CLIENT_SECRET')
    
    print(client_id)
    print(client_secret)

    data = {
        'grant_type' : 'password',
        'client_id' : client_id,
        'client_secret' : client_secret,
        'username' : user,
        'password' : password
    }

    try:
        response = requests.post(token_url, data=data)
        response_data = response.json()

        if response.status_code == 200:
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(response_data, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

