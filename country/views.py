from functools import partial
import re
from django.db.models import manager
from django.http.response import JsonResponse
# from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from country.models import Country
from country.serilizer import CountrySerilizer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET', 'POST'])
def country(request):
    context = {}
    if request.method == "GET":
        quary_set = request.GET.get('name')
        if  quary_set:
            country_filter = Country.objects.filter(name__icontains=quary_set, is_deleted=False)
        else:
            country_filter = Country.objects.filter(is_deleted=False)
        serializer = CountrySerilizer(country_filter, many=True)
        context['status'] = status.HTTP_200_OK
        context['data'] = serializer.data
        context['message'] = "All Country."
        return Response(context, status=status.HTTP_200_OK)

    elif request.method == "POST":
        country_data = JSONParser().parse(request)
        #print(country_data)
        country_serializer = CountrySerilizer(data=country_data)
        #print(country_serializer)
        if country_serializer.is_valid():
            country_serializer.save()
            context['status'] = status.HTTP_200_OK
            context['data'] = country_serializer.errors
            context['message'] = "Country Sucesfully Created."
            return Response(context, status = status.HTTP_200_OK)
        else:
            context['status'] = status.HTTP_400_BAD_REQUEST
            context['data'] = []
            context['message'] = "Country Already Exits!!!"
            return Response(context, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'PUT', 'DELETE'])
def api_country(request, pk):
    context = {}
    try: 
        country = Country.objects.get(pk=pk)
        #print(country)
        if request.method == 'GET':
            x = Country.objects.filter() 
            country_serializer = CountrySerilizer(country)
            return JsonResponse(country_serializer.data) 

        elif request.method == "PUT":
            country_data = JSONParser().parse(request)
            country_serializer = CountrySerilizer(country, data=country_data, partial=True)
            if country_serializer.is_valid(): 
                country_serializer.save()
                context['status'] = status.HTTP_200_OK
                context['data'] = country_serializer.data
                context['message'] = "Regions updated."
                return Response(context, status = status.HTTP_200_OK)
            else:
                context['status'] = status.HTTP_400_BAD_REQUEST
                context['error'] = country_serializer.errors
                context['message'] = "Updated Not Sucess!!! "
                return Response(context, status = status.HTTP_404_NOT_FOUND)

        elif request.method == 'DELETE':
            country_delete = Country.objects.get(pk=pk)
            delete_filter = Country.objects.filter(name=country_delete,is_deleted=False)
            if delete_filter:
                is_deleted = {"is_deleted":"True"}
                country_serializer = CountrySerilizer(country_delete, data=is_deleted, partial=True)
                if country_serializer.is_valid(): 
                    country_serializer.save()
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




    except Country.DoesNotExist: 
        return JsonResponse({'message': 'The Country does not exist'}, status=status.HTTP_404_NOT_FOUND)
       
