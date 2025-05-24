from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from chatbot.models import ChatHistory

from services.ollama import query_ollama
#from services.graphrag import retrieve_context
from .serializers import ChatInputSerializer

class ChatbotView(APIView):
    def post(self, request):
        serializer = ChatInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_input = serializer.validated_data['prompt']

        # 1. 從 GraphRAG 抽取上下文
        context = retrieve_context(user_input)

        # 2. 將 context 加入 prompt
        full_prompt = f"{context}\n\nUser: {user_input}"

        # 3. 呼叫 Ollama
        response_text = query_ollama(full_prompt)

        # 4. 儲存對話紀錄
        #ChatHistory.objects.create(
        #    user_input=user_input,
        #    response=response_text
        #)

        return Response({"response": response_text}, status=status.HTTP_200_OK)
