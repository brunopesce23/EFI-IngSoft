def es_admin_global(request):
    """
    Devuelve un booleano 'es_admin_global' para el navbar.
    Admin := user.perfil.rol == 'admin' o is_staff/superuser.
    """
    user = getattr(request, "user", None)
    is_admin = False
    if user and user.is_authenticated:
        try:
            perfil = getattr(user, "perfil", None)  # related_name='perfil'
            is_admin = (getattr(perfil, "rol", None) == "admin") or user.is_staff or user.is_superuser
        except Exception:
            is_admin = user.is_staff or user.is_superuser
    return {"es_admin_global": is_admin}
