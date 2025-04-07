def check_user_permission_level(user, required_level):
    return (
        hasattr(user, "role") and 
        user.role and 
        user.role.permissions.filter(level__gte=required_level).exists()
    )
