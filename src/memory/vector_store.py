from typing import Any

try:
    import chromadb
    from chromadb.config import Settings as ChromaSettings
except ImportError:
    chromadb = None


class VectorStore:
    def __init__(self, persist_dir: str | None = None, host: str | None = None, port: int | None = None) -> None:
        self.persist_dir = persist_dir
        self.host = host
        self.port = port
        self.client = None
        self.collections: dict[str, list[dict]] = {}

    def connect(self) -> None:
        if chromadb is None:
            return
        if self.host and self.port:
            self.client = chromadb.Client(ChromaSettings(chroma_api_impl="rest", chroma_server_host=self.host, chroma_server_http_port=self.port))
        else:
            self.client = chromadb.Client(ChromaSettings(chroma_db_impl="duckdb+parquet", persist_directory=self.persist_dir))

    def get_collection(self, name: str):
        if self.client is None:
            self.collections.setdefault(name, [])
            return self.collections[name]
        return self.client.get_collection(name)

    async def add(self, collection: str, documents: list[str], embeddings: list[list[float]], metadatas: list[dict[str, Any]]) -> None:
        if self.client is None:
            self.collections.setdefault(collection, []).extend([
                {"document": doc, "embedding": emb, "metadata": meta}
                for doc, emb, meta in zip(documents, embeddings, metadatas)
            ])
            return
        coll = self.client.get_or_create_collection(collection_name=collection)
        coll.add(documents=documents, embeddings=embeddings, metadatas=metadatas)

    async def query(self, collection: str, query_embeddings: list[list[float]], n_results: int = 5, where: dict[str, Any] | None = None) -> dict[str, list[Any]]:
        if self.client is None:
            rows = self.collections.get(collection, [])
            return {
                "documents": [row["document"] for row in rows[:n_results]],
                "metadatas": [row["metadata"] for row in rows[:n_results]],
            }
        coll = self.client.get_collection(collection_name=collection)
        results = coll.query(query_embeddings=query_embeddings, n_results=n_results, where=where)
        return results


vector_store = VectorStore()
