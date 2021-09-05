from functools import partial
import re
from django.db.models import manager
from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from state.models import State
from state.serilizer import StateSerilizer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET', 'POST'])
def state(request):
    context = {}
    if request.method == "GET":
        quary_set = request.GET.get('name')
        if  quary_set:
            state_filter = State.objects.filter(name__icontains=quary_set, is_deleted=False)
        else:
            state_filter = State.objects.filter(is_deleted=False)
        serializer = StateSerilizer(state_filter, many=True)
        context['status'] = status.HTTP_200_OK
        context['data'] = serializer.data
        context['message'] = "All State."
        return Response(context, status=status.HTTP_200_OK)

    elif request.method == "POST":
        state_data = JSONParser().parse(request)
        print(state_data)
        state_serializer = StateSerilizer(data=state_data)
        print(state_serializer)
        if state_serializer.is_valid():
            state_serializer.save()
            context['status'] = status.HTTP_200_OK
            context['data'] = state_serializer.data
            context['message'] = "State Sucesfully Created."
            return Response(context, status = status.HTTP_200_OK)
        else:
            context['status'] = status.HTTP_400_BAD_REQUEST
            context['data'] = []
            context['message'] = "State Already Exits!!!"
            return Response(context, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'PUT', 'DELETE'])
def api_state(request, pk):
    context = {}
    try: 
        country = State.objects.get(pk=pk)
        print(country)
        if request.method == 'GET':
            # x = State.objects.filter() 
            state_serializer = StateSerilizer(country)
            return JsonResponse(state_serializer.data) 

        elif request.method == "PUT":
            state_data = JSONParser().parse(request)
            state_serializer = StateSerilizer(country, data=state_data, partial=True)
            if state_serializer.is_valid(): 
                state_serializer.save()
                context['status'] = status.HTTP_200_OK
                context['data'] = state_serializer.data
                context['message'] = "Regions updated."
                return Response(context, status = status.HTTP_200_OK)
            else:
                context['status'] = status.HTTP_400_BAD_REQUEST
                context['error'] = state_serializer.errors
                context['message'] = "Updated Not Sucess!!! "
                return Response(context, status = status.HTTP_404_NOT_FOUND)

        elif request.method == 'DELETE':
            state_delete = State.objects.get(pk=pk)
            delete_filter = State.objects.filter(name=state_delete,is_deleted=False)
            if delete_filter:
                is_deleted = {"is_deleted":"True"}
                state_serializer = StateSerilizer(state_delete, data=is_deleted, partial=True)
                if state_serializer.is_valid(): 
                    state_serializer.save()
                    context['status'] = status.HTTP_200_OK
                    context['message'] = "Deleted Sucessfully."
                    return Response(context, status=status.HTTP_200_OK)
                else:
                    context['status'] = status.HTTP_400_BAD_REQUEST
                    context['message'] = "Delete Not Sucessful"
                    return Response(context, status=status.HTTP_400_BAD_REQUEST)
            else:
                context['status'] = status.HTTP_400_BAD_REQUEST
                context['message'] = "No Country found to delete"
                return Response(context, status=status.HTTP_400_BAD_REQUEST)




    except State.DoesNotExist: 
        return JsonResponse({'message': 'The State does not exist'}, status=status.HTTP_404_NOT_FOUND)
       
