from django.http.response import Http404

from rest_framework import status
from rest_framework.response import Response
from django.contrib import messages

from core_app.utils import error_response, success_response, specific_object_error_response, success_response_message


class SoftDeleteDestroyViewMixin:
    def destroy(self, request, *args, **kwargs):
        object = self.get_object()
        object.active = False
        object.save()
        # return Response(status=status.HTTP_204_NO_CONTENT)
        return success_response_message(data={},message="Record successfully deleted",status_code=200)

class DeleteResponseMixin:
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Http404:
            return specific_object_error_response(message='record not found')

        self.perform_destroy(instance)
        return Response({"success": True, 'data':{}, "message": "Record Deleted Successfully", "status_code": 200},
                        status=status.HTTP_200_OK)


class RetrieveResponseMixin:
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Http404:
            return specific_object_error_response(message='record not found')
        serializer = self.get_serializer(instance)
        return success_response(serializer, message='record fetched successfully')


class CreateResponseMixin:
    def create(self, request):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer, message='record created successfully', status_code=201)
        return error_response(serializer)


class UpdateResponseMixin:
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        try:
            instance = self.get_object()
        except Http404:
            return specific_object_error_response(message='record not found')

        serializer = self.get_serializer(instance, data=request.data, partial=partial, context={"request": request})
        # serializer.is_valid(raise_exception=True)
        if not serializer.is_valid():
            return error_response(serializer)

        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return success_response(serializer, message='record updated successfully')


class APIResponseGenericViewMixin(RetrieveResponseMixin, UpdateResponseMixin,CreateResponseMixin):
    ...


class RemoveAdminDefaultMessageMixin:

    def remove_default_message(self, request):
        storage = messages.get_messages(request)
        try:
            del storage._queued_messages[-1]
        except KeyError:
            pass
        return True

    def response_add(self, request, obj, post_url_continue=None):
        """override"""
        response = super().response_add(request, obj, post_url_continue)
        self.remove_default_message(request)
        return response

    def response_change(self, request, obj):
        """override"""
        response = super().response_change(request, obj)
        self.remove_default_message(request)
        return response

    def response_delete(self, request, obj_display, obj_id):
        """override"""
        response = super().response_delete(request, obj_display, obj_id)
        self.remove_default_message(request)
        return response

__all__ = [
    "UpdateResponseMixin",
    "CreateResponseMixin",
    "RetrieveResponseMixin",
    "SoftDeleteDestroyViewMixin",
    "DeleteResponseMixin"
]
