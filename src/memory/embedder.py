import hashlib
from typing import List


class Embedder:
    def __init__(self, provider: str = "local") -> None:
        self.provider = provider

    async def embed(self, text: str) -> List[float]:
        if self.provider == "openai":
            return await self._openai_embed(text)
        return self._local_embed(text)

    def _local_embed(self, text: str) -> List[float]:
        digest = hashlib.sha256(text.encode("utf-8")).digest()
        return [b / 255.0 for b in digest]

    async def _openai_embed(self, text: str) -> List[float]:
        raise NotImplementedError("OpenAI embedding provider is not implemented yet.")


embedder = Embedder()
