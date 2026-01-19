from typing import List, Dict, Optional
from dataclasses import dataclass

from lib.vector_db import VectorStoreManager
from lib.documents import Document
from lib.short_memory import MemoryFragment


@dataclass
class MemorySearchResult:
    """
    Container for the results of a memory search operation.

    Encapsulates both the retrieved memory fragments and associated metadata
    such as distance scores from the vector search.

    Attributes:
        fragments (List[MemoryFragment]): List of memory fragments matching the search query
        metadata (Dict): Additional information about the search results (e.g., distances, scores)
    """

    fragments: List[MemoryFragment]
    metadata: Dict


@dataclass
class TimestampFilter:
    """
    Filter criteria for time-based memory searches.

    Allows filtering memory fragments based on when they were created,
    enabling retrieval of recent memories or memories from specific time periods.

    Attributes:
        greater_than_value (int, optional): Unix timestamp - only return memories created after this time
        lower_than_value (int, optional): Unix timestamp - only return memories created before this time
    """

    greater_than_value: int = None
    lower_than_value: int = None


class LongTermMemory:
    """
    Manages persistent memory storage and retrieval using vector embeddings.

    This class provides a high-level interface for storing and searching user memories,
    preferences, and contextual information across conversation sessions. It uses
    vector similarity search to find relevant memories based on semantic meaning.

    The memory system supports:
    - Multi-user memory isolation
    - Namespace-based organization
    - Time-based filtering
    - Semantic similarity search
    """

    def __init__(self, db: VectorStoreManager):
        self.vector_store = db.create_store("long_term_memory", force=True)

    def get_namespaces(self) -> List[str]:
        """
        Retrieve all unique namespaces currently stored in memory.

        Useful for understanding how memories are organized and for
        administrative purposes.

        Returns:
            List[str]: List of unique namespace identifiers
        """
        results = self.vector_store.get()
        namespaces = [r["metadatas"][0]["namespace"] for r in results]
        return namespaces

    def register(self, memory_fragment: MemoryFragment, metadata: Optional[Dict[str, str]] = None):
        """
        Store a new memory fragment in the long-term memory system.

        The memory is converted to a vector embedding and stored with associated
        metadata for later retrieval. Additional metadata can be provided to
        enhance searchability.

        Args:
            memory_fragment (MemoryFragment): The memory content to store
            metadata (Optional[Dict[str, str]]): Additional metadata to associate with the memory
        """
        complete_metadata = {
            "owner": memory_fragment.owner,
            "namespace": memory_fragment.namespace,
            "timestamp": memory_fragment.timestamp,
        }
        if metadata:
            complete_metadata.update(metadata)

        self.vector_store.add(
            Document(
                content=memory_fragment.content,
                metadata=complete_metadata,
            )
        )

    def search(
        self,
        query_text: str,
        owner: str,
        limit: int = 3,
        timestamp_filter: Optional[TimestampFilter] = None,
        namespace: Optional[str] = "default",
    ) -> MemorySearchResult:
        """
        Search for relevant memories using semantic similarity.

        Performs a vector similarity search to find memories that are semantically
        related to the query text. Results are filtered by owner, namespace, and
        optionally by timestamp range.

        Args:
            query_text (str): The search query to find similar memories
            owner (str): User identifier to filter memories by ownership
            limit (int): Maximum number of results to return (default: 3)
            timestamp_filter (Optional[TimestampFilter]): Time-based filtering criteria
            namespace (Optional[str]): Namespace to search within (default: "default")

        Returns:
            MemorySearchResult: Container with matching memory fragments and metadata
        """

        where = {
            "$and": [
                {"namespace": {"$eq": namespace}},
                {"owner": {"$eq": owner}},
            ]
        }

        if timestamp_filter:
            if timestamp_filter.greater_than_value:
                where["$and"].append(
                    {
                        "timestamp": {
                            "$gt": timestamp_filter.greater_than_value,
                        }
                    }
                )
            if timestamp_filter.lower_than_value:
                where["$and"].append(
                    {
                        "timestamp": {
                            "$lt": timestamp_filter.lower_than_value,
                        }
                    }
                )

        result = self.vector_store.query(query_texts=[query_text], n_results=limit, where=where)

        fragments = []
        documents = result.get("documents", [[]])[0]
        metadatas = result.get("metadatas", [[]])[0]

        for content, meta in zip(documents, metadatas):
            owner = meta.get("owner")
            namespace = meta.get("namespace", "default")
            timestamp = meta.get("timestamp")

            fragment = MemoryFragment(content=content, owner=owner, namespace=namespace, timestamp=timestamp)

            fragments.append(fragment)

        result_metadata = {"distances": result.get("distances", [[]])[0]}

        return MemorySearchResult(fragments=fragments, metadata=result_metadata)
