class TenantIsolation:

    def isolate(
        self,
        tenant_id,
        data
    ):

        return {
            "tenant_id": tenant_id,
            "data": data
        }
