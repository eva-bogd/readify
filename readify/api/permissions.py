from rest_framework import permissions


# все действия кроме чтения только админ
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS or
                request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS or
                request.user.is_staff)
        # self.has_permission(request, view)


# создание записи - авторизованные пользователи
# изменение записи - автор записи
# остальные - только чтение
class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS or
                obj.author.id == request.user.id)
