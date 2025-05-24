import { useState, useRef, useEffect } from 'react';

const ChatBot = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: '您好！我是您的AI助手。有什麼我可以幫助您的嗎？',
      sender: 'bot',
      timestamp: new Date().toISOString()
    }
  ]);
  const [inputText, setInputText] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // 使用環境變數或默認值
  const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8001/api';

  // 聊天紀錄自動滾動到最底部
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // 頁面載入後自動聚焦輸入框
  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const handleInputChange = (e) => {
    setInputText(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (inputText.trim() === '') return;
    
    // 添加用戶訊息
    const userMessage = {
      id: messages.length + 1,
      text: inputText,
      sender: 'user',
      timestamp: new Date().toISOString()
    };
    
    setMessages(prevMessages => [...prevMessages, userMessage]);
    const currentInput = inputText;
    setInputText('');
    setIsTyping(true);

    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_BASE_URL}/chat/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': token ? `Token ${token}` : '',
        },
        body: JSON.stringify({ prompt: currentInput }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      const botReply = {
        id: messages.length + 2,
        text: data.response,
        sender: 'bot',
        timestamp: new Date().toISOString(),
      };

      setMessages(prevMessages => [...prevMessages, botReply]);
    } catch (error) {
      console.error('API error:', error);
      const errorMessage = {
        id: messages.length + 2,
        text: '抱歉，發生了錯誤。請稍後再試。',
        sender: 'bot',
        timestamp: new Date().toISOString(),
      };
      setMessages(prevMessages => [...prevMessages, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  // 格式化時間顯示
  const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="flex flex-col h-full bg-gray-50">
      {/* 聊天區域 */}
      <div className="flex-1 overflow-auto p-4">
        <div className="max-w-3xl mx-auto">
          <div className="space-y-4 pb-20">
            {messages.map((message) => (
              <div 
                key={message.id} 
                className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div 
                  className={`max-w-xl rounded-lg p-4 ${
                    message.sender === 'user' 
                      ? 'bg-blue-600 text-white' 
                      : 'bg-white text-gray-800 shadow border'
                  }`}
                >
                  <div className="whitespace-pre-wrap">{message.text}</div>
                  <div 
                    className={`text-xs mt-1 text-right ${
                      message.sender === 'user' ? 'text-blue-200' : 'text-gray-500'
                    }`}
                  >
                    {formatTime(message.timestamp)}
                  </div>
                </div>
              </div>
            ))}
            
            {isTyping && (
              <div className="flex justify-start">
                <div className="bg-white rounded-lg p-4 shadow border">
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                  </div>
                </div>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>
        </div>
      </div>
      
      {/* 輸入區域 */}
      <div className="bg-white border-t p-4">
        <div className="max-w-3xl mx-auto">
          <form onSubmit={handleSubmit} className="flex">
            <input
              ref={inputRef}
              type="text"
              value={inputText}
              onChange={handleInputChange}
              placeholder="輸入訊息..."
              className="flex-1 border rounded-l-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              disabled={isTyping}
            />
            <button 
              type="submit"
              className="bg-blue-600 text-white px-4 py-2 rounded-r-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
              disabled={!inputText.trim() || isTyping}
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <line x1="22" y1="2" x2="11" y2="13"></line>
                <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
              </svg>
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default ChatBot;