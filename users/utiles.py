def check_user_permission_level(user, required_level):
    role_levels = {
        'Student': 1,
        'Nurse': 2,
        'Doctor': 3,
        'Administrator': 4
    }

    if not user.is_authenticated:
        return False

    
    if user.is_staff or user.is_superuser:
        return 4 >= required_level

    user_level = role_levels.get(user.role, 0)
    return user_level >= required_level