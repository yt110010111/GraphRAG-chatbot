from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from chatbot.models import ChatHistory
from services.ollama import query_ollama
from .serializers import ChatInputSerializer
import logging

logger = logging.getLogger(__name__)

class ChatbotView(APIView):
    def post(self, request):
        try:
            serializer = ChatInputSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            user_input = serializer.validated_data['prompt']
            logger.info(f"Received user input: {user_input}")

            # 1. 從 GraphRAG 抽取上下文 (暫時註解掉)
            # context = retrieve_context(user_input)
            
            # 2. 建立完整的 prompt (暫時不使用 context)
            full_prompt = f"User: {user_input}\nAssistant:"
            
            # 3. 呼叫 Ollama
            logger.info("Calling Ollama...")
            response_text = query_ollama(full_prompt)
            logger.info(f"Ollama response: {response_text[:100]}...")  # 只顯示前100字元

            # 4. 儲存對話紀錄 (確保資料庫表格已建立)
            try:
                ChatHistory.objects.create(
                    user_input=user_input,
                    response=response_text
                )
            except Exception as e:
                logger.warning(f"Failed to save chat history: {e}")

            return Response({
                "response": response_text,
                "status": "success"
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"ChatbotView error: {e}")
            return Response({
                "error": "Internal server error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)