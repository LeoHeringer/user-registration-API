from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework_xml.renderers import XMLRenderer

from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

import json



@api_view(['GET'])
@permission_classes([IsAuthenticated])
@renderer_classes([XMLRenderer])
def get_users_xml(request):

    users = User.objects             #irá buscar todos os objetos do banco de dados

    serializer = UserSerializer(users, many=True)   #vai usar o UserSerializar para transformar os objetos de user e serializar eles
    
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_users_json(request):

    users = User.objects

    serializer = UserSerializer(users, many=True) 
    
    return Response(serializer.data, status=status.HTTP_200_OK)


    

@api_view(['GET'])
@renderer_classes([XMLRenderer])
@permission_classes([IsAuthenticated])
def get_by_nick_xml(request):


    if not request.GET['user']:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    user_nickname = request.GET['user']

    user = User.objects.filter(username=user_nickname)

    if not user.exists():
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    serializer = UserSerializer(user.first())
    return Response(serializer.data, status=status.HTTP_200_OK)  


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_by_nick_json(request):


    if not request.GET['user']:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    user_nickname = request.GET['user']

    user = User.objects.filter(username=user_nickname)

    if not user.exists():
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    serializer = UserSerializer(user.first())
    return Response(serializer.data, status=status.HTTP_200_OK)  

    
@api_view(['POST'])
@renderer_classes([XMLRenderer])
@permission_classes([IsAuthenticated])
def create_user_xml(request):

    new_user = request.data

    serializer = UserSerializer(data=new_user)

    if serializer.is_valid():
        serializer.save()
        return Response({'message':'created'}, status=status.HTTP_201_CREATED)

    return Response({'message':'invalid'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_user_json(request):

    new_user = request.data

    serializer = UserSerializer(data=new_user)

    if serializer.is_valid():
        serializer.save()
        return Response({'message':'created'}, status=status.HTTP_201_CREATED)

    return Response({'message':'invalid'}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['PUT'])
@renderer_classes([XMLRenderer])
@permission_classes([IsAuthenticated])
def update_user(request):

    cliente_id = request.query_params.get('id-usuario')

    if not cliente_id: 
        return Response({'message': 'dado incorreto'}, status=status.HTTP_400_BAD_REQUEST)

    update_user = User.objects.filter(id=cliente_id)
    
    if not update_user.exists():
        return Response({'message': 'not exist'}, status=status.HTTP_404_NOT_FOUND)
    

    update_user.is_superuser = request.data.get('is_superuser')
    update_user.save()
    

    return Response({'mensagem': 'Usuário atualizado com sucesso'}, status=status.HTTP_200_OK)
 
    
@api_view(['DELETE'])
@renderer_classes([XMLRenderer])
@permission_classes([IsAuthenticated])
def delete_user(request):

    cliente_id = request.query_params.get('id-usuario')

    try:
        user_to_delete = User.objects.get(id=cliente_id)
        user_to_delete.delete()

        if 'application/xml' in request.headers.get('Accept', ''):  # verifica se 'application/xml' esta no dicionario
            data = {'mensagem': 'Usuario apagado com sucesso'}
            return Response(data, status=status.HTTP_200_OK, content_type='application/xml')
    
        data = {'mensagem': 'Usuario apagado com sucesso'} # caso não tenha achado o xml retornar json por padrão
        return Response(data, status=status.HTTP_200_OK)
    
    except User.DoesNotExist: 
        if 'application/xml' in request.headers.get('Accept', ''):  # verifica se 'application/xml' esta no dicionario
            data = {'mensagem': 'Usuario não encontrado'}
            return Response(data, status=status.HTTP_200_OK, content_type='application/xml')
            
        data = {'mensagem': 'Usuario não encontrado'} # caso não tenha achado o xml retornar json por padrão
        return Response({'mensagem': 'Usuário não encontrado'}, status=status.HTTP_404_NOT_FOUND)


