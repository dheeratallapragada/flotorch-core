from chunking.hierarical_chunking import HieraricalChunker
from chunking.fixedsize_chunking import FixedSizeChunker

class ChunkingFactory:
    """
    Factory to create chunking strategies based on configuration.
    """
    @staticmethod
    def create_chunker(chunking_strategy: str, chunk_size: int, chunk_overlap: int, parent_chunk_size: int = None):
        if chunking_strategy == "Hierarchical":
            return HieraricalChunker(chunk_size, chunk_overlap, parent_chunk_size)
        elif chunking_strategy == "Fixed":
            return FixedSizeChunker(chunk_size, chunk_overlap)
        else:
            raise ValueError(f"Unsupported chunking type: {chunking_strategy}")
