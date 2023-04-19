from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.parsers import JSONParser
from .models import Edl, EdlEntry
from .serializers import EdlSerializer, EdlEntrySerializer


class ListEdls(APIView):
    """
    View to list all External Dynamic List in the system.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EdlSerializer

    def get(self, request):
        edls = Edl.objects.all()
        serializer = EdlSerializer(edls, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        serializer = EdlSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
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
        return Response(status=status.HTTP_204_NO_CONTENT)


class ViewEdlEntries(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EdlEntrySerializer

    def get(self, request, name):
        try:
            edl = Edl.objects.get(name=name)
        except Edl.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = EdlEntrySerializer(edl.entries, many=True)
        return Response(serializer.data)

    def post(self, request, name):
        try:
            edl = Edl.objects.get(name=name)
        except Edl.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = request.data
        data["edl"] = edl.id
        # Check if EdlEntry existed
        try:
            edl_entry = EdlEntry.objects.get(entry_value=data['entry_value'], edl_id=edl.id)
        except Edl.DoesNotExist:
            # Edl Entry does not exist, creating new entry
            serializer = EdlEntrySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # Updating old entry, instead of creating new
        serializer = EdlEntrySerializer(edl_entry, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ViewEdlEntriesPaFmt(APIView):
    def get(self, request, edl_id):
        try:
            edl = Edl.objects.get(pk=edl_id)
        except Edl.DoesNotExist:
            return HttpResponse("list_does_not_exist", content_type="text/plain")

        output_string = ""
        print(edl.entries.all())
        for entry in edl.entries.all():
            output_string = entry.entry_value + "\n"
        return HttpResponse(output_string, content_type="text/plain")

