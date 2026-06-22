import os
import psycopg2
from psycopg2.extras import Json

class VectorStore:
    def __init__(self):
        self.connection_string = os.getenv("PGVECTOR_CONNECTION_STRING")
        if not self.connection_string:
            raise ValueError("PGVECTOR_CONNECTION_STRING environment variable not set.")
        self.table_name = "vectors"

    def _connect(self):
        return psycopg2.connect(self.connection_string)

    def upsert(self, id: str, vector: list, metadata: dict):
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(f"""
                    INSERT INTO {self.table_name} (id, vector, metadata)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (id) DO UPDATE
                    SET vector = EXCLUDED.vector, metadata = EXCLUDED.metadata;
                """, (id, vector, Json(metadata)))
                conn.commit()

    def search(self, query_embedding: list, top_k: int, **filters) -> list:
        filter_conditions = " AND ".join([f"metadata->>'{key}' = %s" for key in filters.keys()])
        filter_values = list(filters.values())
        query = f"""
            SELECT id, metadata, 1 - (vector <-> %s) AS distance
            FROM {self.table_name}
            WHERE {filter_conditions} 
            ORDER BY distance DESC
            LIMIT %s;
        """ if filters else f"""
            SELECT id, metadata, 1 - (vector <-> %s) AS distance
            FROM {self.table_name}
            ORDER BY distance DESC
            LIMIT %s;
        """
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(query, [query_embedding, *filter_values, top_k] if filters else [query_embedding, top_k])
                results = cur.fetchall()
                return [{"id": row[0], "metadata": row[1], "distance": row[2]} for row in results]