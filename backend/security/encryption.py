from cryptography.fern
<truncated 3302 bytes>
ame__ = "billing"

    id = Column(
        Integer,
        primary_key=True
    )

    tenant_id = Column(Integer)

    amount = Column(Float)

    status = Column(String(100))
