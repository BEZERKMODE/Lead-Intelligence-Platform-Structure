class
<truncated 3494 bytes>
     )

    def create_embedding(
        self,
        text
    ):

        vector = self.model.encode(text)

        return vector.tolist()
