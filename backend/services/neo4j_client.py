import os
from neo4j import GraphDatabase, basic_auth
import logging
import re

logger = logging.getLogger(__name__)

class Neo4jClient:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=basic_auth(user, password))
    
    def close(self):
        self.driver.close()
    
    def test_connection(self):
        """測試 Neo4j 連接"""
        try:
            with self.driver.session() as session:
                result = session.run("RETURN 1 as test")
                record = result.single()
                logger.info("✅ Neo4j connection successful")
                return True
        except Exception as e:
            logger.error(f"❌ Neo4j connection failed: {e}")
            return False
    
    def get_all_sentences(self):
        """獲取所有句子用於調試"""
        try:
            with self.driver.session() as session:
                result = session.run("MATCH (s:Sentence) RETURN s.text as text, s.idx as idx ORDER BY s.idx")
                sentences = []
                for record in result:
                    sentences.append({
                        'idx': record.get('idx'),
                        'text': record.get('text')
                    })
                logger.info(f"📊 Total sentences in database: {len(sentences)}")
                for i, s in enumerate(sentences[:5]):  # 只顯示前5個
                    logger.info(f"  {s['idx']}: {s['text'][:50]}...")
                return sentences
        except Exception as e:
            logger.error(f"Error getting sentences: {e}")
            return []
    
    def create_knowledge_graph(self, text):
        # 改進文本分割邏輯
        sentences = []
        
        # 多種分句方式
        # 1. 按句號分割
        parts = text.split('。')
        for part in parts:
            part = part.strip()
            if part:
                # 2. 如果句子太長，按逗號進一步分割
                if len(part) > 100:
                    sub_parts = part.split('，')
                    for sub_part in sub_parts:
                        sub_part = sub_part.strip()
                        if sub_part and len(sub_part) > 5:  # 過濾太短的片段
                            sentences.append(sub_part)
                else:
                    sentences.append(part)
        
        logger.info(f"📝 Processing {len(sentences)} sentences")
        
        with self.driver.session() as session:
            # 清理舊數據（可選）
            # session.run("MATCH (s:Sentence) DELETE s")
            
            for i, sentence in enumerate(sentences):
                logger.info(f"  Adding sentence {i}: {sentence[:50]}...")
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
        
        logger.info(f"✅ Created graph with {len(sentences)} sentences.")
        return f"建立了 {len(sentences)} 個節點和關聯"
    
    def query_graph_context(self, prompt, limit=3):
        logger.info(f"🔍 Querying with prompt: '{prompt}'")
        
        # 改進關鍵詞提取
        keywords = []
        
        # 1. 分割並清理關鍵詞
        raw_keywords = re.split(r"[，。,\s]+", prompt)
        for kw in raw_keywords:
            kw = kw.strip()
            if kw and len(kw) >= 1:  # 包含單字符關鍵詞
                keywords.append(kw)
        
        logger.info(f"🔑 Extracted keywords: {keywords}")
        
        if not keywords:
            logger.warning("⚠️ No keywords extracted from prompt")
            return ""
        
        with self.driver.session() as session:
            # 先檢查是否有數據
            count_result = session.run("MATCH (s:Sentence) RETURN count(s) as total")
            total_sentences = count_result.single()['total']
            logger.info(f"📊 Total sentences in database: {total_sentences}")
            
            if total_sentences == 0:
                logger.warning("⚠️ No sentences found in database")
                return ""
            
            # 構建更寬鬆的查詢條件
            where_conditions = []
            params = {"limit": limit}
            
            for i, kw in enumerate(keywords):
                param_name = f"kw{i}"
                # 使用 CONTAINS 進行包含匹配
                where_conditions.append(f"toLower(s.text) CONTAINS toLower(${param_name})")
                params[param_name] = kw
            
            where_clause = " OR ".join(where_conditions)
            
            query = f"""
                MATCH (s:Sentence)
                WHERE {where_clause}
                RETURN s.text AS text, s.idx AS idx
                ORDER BY s.idx
                LIMIT $limit
            """
            
            logger.info(f"🔍 Executing query: {query}")
            logger.info(f"📝 Query parameters: {params}")
            
            try:
                result = session.run(query, **params)
                matched = []
                
                for record in result:
                    text_val = record.get("text")
                    idx_val = record.get("idx")
                    if text_val:
                        matched.append(text_val)
                        logger.info(f"  ✅ Match {idx_val}: {text_val[:50]}...")
                
                if not matched:
                    logger.warning("⚠️ No matches found, trying fuzzy search...")
                    # 嘗試更寬鬆的搜索
                    fuzzy_query = """
                        MATCH (s:Sentence)
                        WHERE any(kw in $keywords WHERE toLower(s.text) CONTAINS toLower(kw))
                        RETURN s.text AS text, s.idx AS idx
                        ORDER BY s.idx
                        LIMIT $limit
                    """
                    fuzzy_result = session.run(fuzzy_query, keywords=keywords, limit=limit)
                    for record in fuzzy_result:
                        text_val = record.get("text")
                        if text_val:
                            matched.append(text_val)
                            logger.info(f"  🔍 Fuzzy match: {text_val[:50]}...")
                
                logger.info(f"🎯 Final matched context: {len(matched)} sentences")
                return "\n".join(matched)
                
            except Exception as e:
                logger.error(f"❌ Graph query error: {e}")
                return ""

# 測試和調試功能
def debug_neo4j_setup():
    """調試 Neo4j 設置"""
    NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")
    
    logger.info(f"🔧 Connecting to Neo4j at {NEO4J_URI}")
    
    client = Neo4jClient(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
    
    # 1. 測試連接
    if not client.test_connection():
        logger.error("❌ Cannot connect to Neo4j")
        return False
    
    # 2. 檢查現有數據
    sentences = client.get_all_sentences()
    
    # 3. 如果沒有數據，添加一些測試數據
    if len(sentences) == 0:
        logger.info("📝 No existing data, adding test data...")
        test_text = """
        玉山銀行是台灣的知名銀行。
        客服電話是02-2182-1313。
        營業時間為週一到週五上午9點到下午5點。
        提供各種金融服務包括存款、貸款、投資等。
        """
        client.create_knowledge_graph(test_text)
        sentences = client.get_all_sentences()
    
    # 4. 測試查詢
    test_queries = ["玉山", "客服", "電話", "營業時間"]
    for query in test_queries:
        logger.info(f"\n🔍 Testing query: '{query}'")
        context = client.query_graph_context(query, limit=2)
        logger.info(f"📋 Result: {context}")
    
    client.close()
    return True

# 創建全局實例供其他模塊使用
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

neo4j_client = Neo4jClient(
    uri=NEO4J_URI,
    user=NEO4J_USER,
    password=NEO4J_PASSWORD
)

# 使用示例
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    debug_neo4j_setup()