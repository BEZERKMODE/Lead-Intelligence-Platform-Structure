class RBAC:

    def __init__(self):

        self.permissions = {
            "admin": [
                "read",
                "write",
                "delete",
                "manage_users"
            ],

            "manager": [
                "read",
                "write"
            ],

            "user": [
                "read"
            ]
        }

    def has_permission(
        self,
        role,
        permission
    ):

        return permission in self.permissions.get(
            role,
            []
        )
