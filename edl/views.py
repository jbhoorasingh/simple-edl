from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework.parsers import JSONParser
from .models import Edl, EdlEntry, EdlLog
from .serializers import EdlSerializer, EdlEntrySerializer, EdlLogSerializer
from datetime import datetime
from urllib.parse import unquote
from django.utils import timezone

class ListEdls(APIView):
    """
    View to list all External Dynamic List in the system.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EdlSerializer

    @extend_schema(
        request=[],
        responses={200: EdlSerializer(many=True)},
        parameters=[
            OpenApiParameter(
                name='list_name',
                type=OpenApiTypes.STR,
                description='Optional parameter for list_name filtering.',
                required=False
            ),
            OpenApiParameter(
                name='description',
                type=OpenApiTypes.STR,
                description='Optional parameter for description filtering.',
                required=False
            ),
            OpenApiParameter(
                name='list_type',
                type=OpenApiTypes.STR,
                description='Optional parameter for list_type filtering.',
                required=False
            ),
            OpenApiParameter(
                name='created_range_start',
                type=OpenApiTypes.DATETIME,
                description='Optional parameter for created_range_start filtering.',
                required=False
            ),
            OpenApiParameter(
                name='created_range_end',
                type=OpenApiTypes.DATETIME,
                description='Optional parameter for created_range_end filtering.',
                required=False
            ),
        ]
    )
    def get(self, request):
        # Get query params
        list_name = request.query_params.get('list_name')
        list_description = request.query_params.get('list_description')
        list_type = request.query_params.get('list_type')
        created_range_start = request.query_params.get('created_range_start')
        created_range_end = request.query_params.get('timestamp_end')

        # Validate query params
        if list_name:
            if not isinstance(list_name, str):
                return Response({'status': 'failed', 'message': 'list_name must be a string'},
                                status=status.HTTP_400_BAD_REQUEST)
            # check if list_name is valid containing only letters, numbers, and underscores
            if not list_name.isalnum() and not list_name.isalpha() and not list_name.isnumeric() and not list_name.isascii():
                return Response(
                    {'status': 'failed', 'message': 'list_name must contain only letters, numbers, and underscores'},
                    status=status.HTTP_400_BAD_REQUEST)
        if list_type:
            if not isinstance(list_type, str):
                return Response({'status': 'failed', 'message': 'list_type must be a string'},
                                status=status.HTTP_400_BAD_REQUEST)
            # check if object_changed is valid containing only letters, numbers, and underscores
            if not list_type.isalnum() and not list_type.isalpha() and not list_type.isnumeric() and not list_type.isascii():
                return Response({'status': 'failed',
                                 'message': 'list_type must contain only letters, numbers, and underscores'},
                                status=status.HTTP_400_BAD_REQUEST)
        if list_description:
            if not isinstance(list_description, str):
                return Response({'status': 'failed',
                                 'message': 'list_description must be a string'},
                                status=status.HTTP_400_BAD_REQUEST)
            # check if list_description is valid containing only letters, numbers, underscores, and spaces
            if not list_description.isalnum() and not list_description.isalpha() and not list_description.isnumeric() and not list_description.isascii() and not list_description.isspace():
                return Response({'status': 'failed',
                                 'message': 'list_description must contain only letters, numbers, underscores, and spaces'},
                                status=status.HTTP_400_BAD_REQUEST)

        if created_range_start:
            try:
                decoded_start = unquote(created_range_start)
                created_range_start = datetime.strptime(decoded_start, '%Y-%m-%dT%H:%M')
            except:
                return Response(
                    {'status': 'failed', 'message': 'created_range_start must be in format YYYY-MM-DDTHH:MM'},
                    status=status.HTTP_400_BAD_REQUEST)
        if created_range_end:
            try:
                decoded_end = unquote(created_range_start)
                created_range_end = datetime.strptime(decoded_end, '%Y-%m-%dT%H:%M')
            except:
                return Response(
                    {'status': 'failed', 'message': 'created_range_end must be in format YYYY-MM-DDTHH:MM'},
                    status=status.HTTP_400_BAD_REQUEST)

        edls = Edl.objects.all()

        if list_name:
            edls = edls.filter(name__icontains=list_name)
        if list_type:
            edls = edls.filter(edl_type=list_type)
        if list_description:
            edls = edls.filter(description__icontains=list_description)
        if created_range_start:
            edls = edls.filter(created__gte=created_range_start)
        if created_range_end:
            edls = edls.filter(created__lte=created_range_end)

        serializer = EdlSerializer(edls, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        serializer = EdlSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            log = EdlLog(performed_by=request.user, edl_name=data['name'], edl_entry=None, action='edl_create',
                         log_message="{} was created".format(data['name']))
            log.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ViewEdlDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EdlSerializer
    """
    Operations for a specific External Dynamic List entry by ID.
    """
    def get(self, request, name):
        try:
            edl = Edl.objects.get(name=name)
        except Edl.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = EdlSerializer(edl)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, name):
        try:
            edl = Edl.objects.get(name=name)
        except Edl.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = EdlSerializer(edl, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, name):
        try:
            edl = Edl.objects.get(name=name)
        except Edl.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        edl.delete()
        log = EdlLog(performed_by=request.user, edl_name=name, edl_entry=None, action='edl_delete',
                     log_message="{} was deleted".format(name))
        log.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ViewEdlEntries(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EdlEntrySerializer

    # DRF Spectacular Schema
    @extend_schema(
        request=[],
        responses={200: EdlEntrySerializer(many=True)},
        parameters=[
            OpenApiParameter(
                name='entry',
                type=OpenApiTypes.STR,
                description='Optional parameter for entry filtering.',
                required=False
            ),
        ]
    )
    def get(self, request, edl_name):

        try:
            edl = Edl.objects.get(name=edl_name)
        except Edl.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Get all entries for this edl
        entries = EdlEntry.objects.filter(edl=edl).order_by('-created')

        # Filter entries by entry
        entry = request.query_params.get('entry_value')
        # Validate query params
        if entry:
            if not isinstance(entry, str):
                return Response({'status': 'failed', 'message': 'entry must be a string'},
                                status=status.HTTP_400_BAD_REQUEST)
            # check if message is valid containing only letters, numbers, underscores, and spaces
            if not entry.isalnum() and not entry.isalpha() and not entry.isnumeric() and not entry.isascii():
                return Response({'status': 'failed',
                                 'message': 'entry must contain only letters, numbers, underscores'},
                                status=status.HTTP_400_BAD_REQUEST)
        if entry:
            entries = entries.filter(entry_value__icontains=entry)

        serializer = EdlEntrySerializer(entries, many=True)

        return Response(serializer.data)

    def post(self, request, edl_name):
        try:
            edl = Edl.objects.get(name=edl_name)
        except Edl.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = request.data
        data["edl"] = edl.id
        # Check if EdlEntry existed
        try:
            edl_entry = EdlEntry.objects.get(entry_value=data['entry_value'], edl_id=edl.id)
        except EdlEntry.DoesNotExist:
            # Edl Entry does not exist, creating new entry
            serializer = EdlEntrySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                log = EdlLog(performed_by=request.user, edl_name=edl_name, edl_entry=data['entry_value'], action='edl_entry_create',
                             log_message="{} was added to edl until {}".format(data['entry_value'], data['valid_until']))
                log.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # Updating old entry, instead of creating new
        serializer = EdlEntrySerializer(edl_entry, data=data)
        if serializer.is_valid():
            serializer.save()
            log = EdlLog(performed_by=request.user, edl_name=edl_name, edl_entry=data['entry_value'], action='edl_entry_update',
                         log_message="{} was updated to edl until {}".format(data['entry_value'], data['valid_until']))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ViewEdlEntriesPaFmt(APIView):
    def get(self, request, edl_name):
        try:
            edl = Edl.objects.get(name=edl_name)
        except Edl.DoesNotExist:
            return HttpResponse("list_does_not_exist", content_type="text/plain")

        output_string = ""
        current_time = timezone.now()
        valid_entries = edl.entries.filter(valid_until__gt=current_time)  # Filter out expired entries

        # print(edl.entries.all())
        for entry in valid_entries.all():
            output_string += entry.entry_value + "\n"
        return HttpResponse(output_string, content_type="text/plain")


class ViewEdlLogs(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EdlLogSerializer
    def get(self, request, edl_name):

        try:
            edl = Edl.objects.get(name=edl_name)
        except Edl.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Get all entries for this edl
        logs = EdlLog.objects.filter(edl_name=edl_name).order_by('-timestamp')

        serializer = EdlLogSerializer(logs, many=True)

        return Response(serializer.data)
