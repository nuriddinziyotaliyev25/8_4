from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    """Adminlikka tekshiradi"""
    message = "Bu amalni bajarish uchun admin bo'lishingiz kerak."

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return request.user and request.user.is_staff


class IsAuth(BasePermission):
    """Ro'yxatdan o'tganlikka tekshirish"""
    message = "Faqat ro'yxatdan o'tgan foydalanuvchilar uchun"

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated