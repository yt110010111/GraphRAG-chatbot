import { useState, useRef, useEffect } from 'react';

const ChatApp = () => {
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

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (inputText.trim() === '') return;
    
    // 添加用戶訊息
    const userMessage = {
      id: messages.length + 1,
      text: inputText,
      sender: 'user',
      timestamp: new Date().toISOString()
    };
    
    setMessages([...messages, userMessage]);
    setInputText('');
    setIsTyping(true);
    /*
    // 模擬AI回應
    setTimeout(() => {
      const botReply = {
        id: messages.length + 2,
        text: generateResponse(inputText),
        sender: 'bot',
        timestamp: new Date().toISOString()
      };
      
      setMessages(prevMessages => [...prevMessages, botReply]);
      setIsTyping(false);
    }, 1000 + Math.random() * 2000); // 隨機延遲模擬思考時間*/
    // 把原本的 setTimeout 替換成這段：
fetch('http://localhost:8001/api/chat/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ prompt: inputText }),
})
  .then((res) => res.json())
  .then((data) => {
    const botReply = {
      id: messages.length + 2,
      text: data.response, // 後端回傳的文字
      sender: 'bot',
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, botReply]);
    setIsTyping(false);
  })
  .catch((err) => {
    console.error('API error:', err);
    setIsTyping(false);
  });

  };

  // 簡單的回應生成邏輯
  const generateResponse = (input) => {
    const lowerInput = input.toLowerCase();
    
    if (lowerInput.includes('你好') || lowerInput.includes('嗨')) {
      return '您好！很高興能與您交談。有什麼我能幫助您的嗎？';
    } else if (lowerInput.includes('名字') || lowerInput.includes('誰')) {
      return '我是一個AI助手，基於類似Claude的界面設計。';
    } else if (lowerInput.includes('謝謝') || lowerInput.includes('感謝')) {
      return '不客氣！如果您有其他問題，隨時可以詢問我。';
    } else if (lowerInput.includes('再見') || lowerInput.includes('拜拜')) {
      return '再見！祝您有愉快的一天。需要幫助時隨時回來。';
    } else if (lowerInput.includes('功能') || lowerInput.includes('做什麼')) {
      return '我可以回答問題、提供資訊、協助創意寫作，以及進行一般的對話交流。不過目前我的功能是有限的演示版本。在實際應用中，您可以連接後端API來提供更豐富的功能。';
    }
    
    return '謝謝您的訊息。在完整版本中，這裡會連接到後端API來處理更複雜的對話。您可以繼續測試這個界面的其他功能。';
  };

  // 格式化時間顯示
  const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="flex flex-col h-screen bg-gray-100">
      {/* 頂部導航欄 */}
      <header className="bg-white p-4 shadow">
        <div className="max-w-4xl mx-auto flex justify-between items-center">
          <div className="flex items-center">
            <div className="h-8 w-8 rounded-full bg-purple-600 flex items-center justify-center text-white font-bold mr-2">A</div>
            <h1 className="text-xl font-semibold">Chatbot</h1>
          </div>
          <button className="text-gray-600 hover:bg-gray-100 p-2 rounded-full">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="12" cy="12" r="1"></circle>
              <circle cx="19" cy="12" r="1"></circle>
              <circle cx="5" cy="12" r="1"></circle>
            </svg>
          </button>
        </div>
      </header>
      
      {/* 聊天區域 */}
      <main className="flex-1 overflow-auto p-4">
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
                      ? 'bg-purple-600 text-white' 
                      : 'bg-white text-gray-800 shadow'
                  }`}
                >
                  <div className="whitespace-pre-wrap">{message.text}</div>
                  <div 
                    className={`text-xs mt-1 text-right ${
                      message.sender === 'user' ? 'text-purple-200' : 'text-gray-500'
                    }`}
                  >
                    {formatTime(message.timestamp)}
                  </div>
                </div>
              </div>
            ))}
            
            {isTyping && (
              <div className="flex justify-start">
                <div className="bg-white rounded-lg p-4 shadow">
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
      </main>
      
      {/* 輸入區域 */}
      <footer className="bg-white border-t p-4 fixed bottom-0 w-full">
        <div className="max-w-3xl mx-auto">
          <div className="flex">
            <input
              ref={inputRef}
              type="text"
              value={inputText}
              onChange={handleInputChange}
              onKeyPress={(e) => {
                if (e.key === 'Enter') {
                  handleSubmit(e);
                }
              }}
              placeholder="輸入訊息..."
              className="flex-1 border rounded-l-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-purple-600"
            />
            <button 
              onClick={handleSubmit}
              className="bg-purple-600 text-white px-4 py-2 rounded-r-lg hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-purple-600"
              disabled={!inputText.trim()}
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <line x1="22" y1="2" x2="11" y2="13"></line>
                <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
              </svg>
            </button>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default ChatApp;