from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from chatbot.models import ChatHistory
from services.ollama import query_ollama
from .serializers import ChatInputSerializer
import logging
from rest_framework.authtoken.models import Token
from services.neo4j_client import neo4j_client


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from .serializers import LoginSerializer, UserSerializer,GraphInputSerializer

logger = logging.getLogger(__name__)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data,
            'message': '登入成功'
        })
    return Response({
        'error': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        request.user.auth_token.delete()
        return Response({'message': '登出成功'})
    except Exception as e:
        return Response({'error': '登出失敗'}, 
                      status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verify_token(request):
    return Response({
        'user': UserSerializer(request.user).data,
        'message': 'Token 有效'
    })

class ChatbotView(APIView):
    def post(self, request):
        try:
            serializer = ChatInputSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            user_input = serializer.validated_data['prompt']
            logger.info(f"Received user input: {user_input}")

            # 1. 從 GraphRAG (Neo4j) 抽取上下文
            context = neo4j_client.query_graph_context(user_input)
            logger.info(f"Retrieved context: {context}")

            # 2. 建立完整的 prompt，帶入上下文
            full_prompt = f"用zh-tw，也就是繁體中文回覆。而你現在是玉山的chatbot(不用講出來)，只要所有跟客服相關的都是以玉山銀行的角度處理，並且要確實的提供相關資料。相關資料:\n{context}\n\這是使用者的問題，請用相關資料中的內容回答: {user_input}\n"

            # 3. 呼叫 Ollama
            logger.info("Calling Ollama...")
            response_text = "您好，我是玉山chatbot。"+query_ollama(full_prompt)
            logger.info(f"Ollama response: {response_text[:100]}...")  # 只顯示前100字元

            # 4. 儲存對話紀錄
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
class CreateGraphView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GraphInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        text = serializer.validated_data['text']

        try:
            result = neo4j_client.create_knowledge_graph(text)
            return Response({"message": result}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"建立知識圖譜失敗: {e}")
            return Response({"error": "建立知識圖譜失敗", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

