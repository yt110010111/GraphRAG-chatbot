import os
from neo4j import GraphDatabase, basic_auth
import logging

logger = logging.getLogger(__name__)

class Neo4jClient:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=basic_auth(user, password))
    
    def close(self):
        self.driver.close()
    
    def create_knowledge_graph(self, text):
        sentences = [s.strip() for s in text.split('。') if s.strip()]
        
        with self.driver.session() as session:
            for i, sentence in enumerate(sentences):
                session.run(
                    "MERGE (s:Sentence {text: $text, idx: $idx})",
                    text=sentence, idx=i
                )
                if i > 0:
                    session.run(
                        """
                        MATCH (s1:Sentence {idx: $prev_idx}), (s2:Sentence {idx: $curr_idx})
                        MERGE (s1)-[:NEXT]->(s2)
                        """,
                        prev_idx=i-1, curr_idx=i
                    )
        logger.info(f"Created graph with {len(sentences)} sentences.")
        return f"建立了 {len(sentences)} 個節點和關聯"

    def query_graph_context(self, prompt, limit=3):
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (s:Sentence)
                WHERE s.text CONTAINS $keyword
                RETURN s.text AS text
                LIMIT $limit
                """,
                keyword=prompt, limit=limit
            )
            contexts = [record["text"] for record in result]
        return "\n".join(contexts)
        

# 從環境變數讀取設定
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

neo4j_client = Neo4jClient(
    uri=NEO4J_URI,
    user=NEO4J_USER,
    password=NEO4J_PASSWORD
)
