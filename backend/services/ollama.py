import requests
import os
import logging

logger = logging.getLogger(__name__)

# 在 Docker 環境中使用容器名稱，本地開發使用 localhost
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api/generate")

def query_ollama(prompt: str, model: str = "llama3") -> str:
    """
    傳送 prompt 到 Ollama 並取得回應。
    """
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    try:
        logger.info(f"Sending request to Ollama: {OLLAMA_API_URL}")
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        
        ollama_response = data.get("response", "")
        if not ollama_response:
            logger.warning("Empty response from Ollama")
            return "抱歉，模型沒有回應內容。"
            
        logger.info("Successfully received response from Ollama")
        return ollama_response.strip()
        
    except requests.exceptions.Timeout:
        logger.error("Timeout when calling Ollama API")
        return "抱歉，回應時間過長，請重試。"
    except requests.exceptions.ConnectionError:
        logger.error("Cannot connect to Ollama API")
        return "無法連線到 Ollama 服務，請確認服務是否正常運行。"
    except requests.RequestException as e:
        logger.error(f"Ollama API error: {e}")
        return f"Ollama API 錯誤: {str(e)}"
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return "發生未預期的錯誤，請重試。"