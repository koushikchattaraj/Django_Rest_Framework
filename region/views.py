from functools import partial
import re
from django.db.models import manager
from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from region.models import Region
from region.serilizer import RegionSerilizer
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET', 'POST']) 
def region(request):
    context = {}
    if request.method == "GET":
        quary_set = request.GET.get('name')
        if  quary_set:
            regions_filter = Region.objects.filter(name__icontains=quary_set, is_deleted=False)
        else:
            regions_filter = Region.objects.filter(is_deleted=False)
        serializer = RegionSerilizer(regions_filter, many=True)
        context['status'] = status.HTTP_200_OK
        context['data'] = serializer.data
        context['message'] = "All Regions."
        return Response(context, status=status.HTTP_200_OK)

    elif request.method == "POST":
        region_data = JSONParser().parse(request)
        region_serializer = RegionSerilizer(data=region_data)
        if region_serializer.is_valid():
            region_serializer.save()
            context['status'] = status.HTTP_200_OK
            context['data'] = region_serializer.data
            context['message'] = "Region Sucesfully Created."
            return Response(context, status = status.HTTP_200_OK)
        else:
            context['status'] = status.HTTP_400_BAD_REQUEST
            context['data'] = []
            context['message'] = "Region Already Exits!!!"
            return Response(context, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'PUT', 'DELETE'])
def putregion(request, pk):
    context = {}
    try: 
        region = Region.objects.get(pk=pk)
        print(region)
        if request.method == 'GET':
            
            region_serializer = RegionSerilizer(region)
            return JsonResponse(region_serializer.data) 

        elif request.method == "PUT":
            region_data = JSONParser().parse(request)
            region_serializer = RegionSerilizer(region, data=region_data, partial=True)
            if region_serializer.is_valid(): 
                region_serializer.save()
                context['status'] = status.HTTP_200_OK
                context['data'] = region_serializer.data
                context['message'] = "Regions updated."
                return Response(context, status = status.HTTP_200_OK)
            else:
                context['status'] = status.HTTP_400_BAD_REQUEST
                context['error'] = region_serializer.errors
                context['message'] = "Updated Not Sucess!!! "
                return Response(context, status = status.HTTP_404_NOT_FOUND) 

        elif request.method == 'DELETE':
            region_delete = Region.objects.get(pk=pk)
            delete_filter = Region.objects.filter(name=region_delete,is_deleted=False)
            if delete_filter:
                is_deleted = {"is_deleted":"True"}
                region_serializer = RegionSerilizer(region_delete, data=is_deleted, partial=True)
                if region_serializer.is_valid(): 
                    region_serializer.save()
                    context['status'] = status.HTTP_200_OK
                    context['message'] = "Deleted Sucessfully."
                    return Response(context, status=status.HTTP_200_OK)
                else:
                    context['status'] = status.HTTP_400_BAD_REQUEST
                    context['message'] = "Delete Not Sucessful"
                    return Response(context, status=status.HTTP_400_BAD_REQUEST)
            else:
                context['status'] = status.HTTP_400_BAD_REQUEST
                context['message'] = "No region found to delete"
                return Response(context, status=status.HTTP_400_BAD_REQUEST)




    except Region.DoesNotExist: 
        return JsonResponse({'message': 'The Region does not exist'}, status=status.HTTP_404_NOT_FOUND)
       

