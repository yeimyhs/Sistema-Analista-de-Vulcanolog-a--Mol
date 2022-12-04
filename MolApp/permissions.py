# permissions.py

from rest_framework import permissions


class postLogStaff(permissions.BasePermission):


    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS 
            or request.user and

           request.method == 'POST' or 
            request.user.is_staff and

            request.user.is_staff 
        )
