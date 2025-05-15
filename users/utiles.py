def check_user_permission_level(user, required_level):
    role_levels = {
        'Student': 1,
        'Nurse': 2,
        'Doctor': 3
    }

    user_level = role_levels.get(user.role, 0)
    return user_level >= required_level
