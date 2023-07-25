from rest_framework import permissions


class CitizensOwnerUser(permissions.BasePermission):
    """ permission validated if citizen register belong to user authenticated """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
