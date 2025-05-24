import React, { useState, useEffect } from 'react';
import Login from './components/Login';
import ChatBot from './components/ChatBot';
import './index.css';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // 使用環境變數或默認值
  const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8001/api';

  useEffect(() => {
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    const token = localStorage.getItem('token');
    const userData = localStorage.getItem('user');
    
    if (token && userData) {
      try {
        console.log('Verifying token with:', `${API_BASE_URL}/verify-token/`);
        
        const response = await fetch(`${API_BASE_URL}/verify-token/`, {
          headers: {
            'Authorization': `Token ${token}`,
          },
        });

        if (response.ok) {
          setIsAuthenticated(true);
          setUser(JSON.parse(userData));
        } else {
          localStorage.removeItem('token');
          localStorage.removeItem('user');
        }
      } catch (error) {
        console.error('Token verification failed:', error);
        localStorage.removeItem('token');
        localStorage.removeItem('user');
      }
    }
    setLoading(false);
  };

  const handleLogin = (token, userData) => {
    setIsAuthenticated(true);
    setUser(userData);
  };

  const handleLogout = async () => {
    const token = localStorage.getItem('token');
    
    if (token) {
      try {
        await fetch(`${API_BASE_URL}/logout/`, {
          method: 'POST',
          headers: {
            'Authorization': `Token ${token}`,
          },
        });
      } catch (error) {
        console.error('Logout error:', error);
      }
    }
    
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setIsAuthenticated(false);
    setUser(null);
  };

  if (loading) {
    return (
      <div className="min-h-screen flex justify-center items-center bg-gray-100">
        <div className="text-lg text-gray-600">載入中...</div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Login onLogin={handleLogin} />;
  }

  return (
    <div className="h-screen flex flex-col bg-gray-100">
      {/* 頂部導航欄 */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center">
              <div className="h-8 w-8 rounded-full bg-blue-600 flex items-center justify-center text-white font-bold mr-3">
                AI
              </div>
              <h1 className="text-xl font-semibold text-gray-900">
                AI 聊天助手
              </h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-gray-700 text-sm">
                歡迎, {user?.username}
              </span>
              <button 
                onClick={handleLogout}
                className="bg-red-500 hover:bg-red-600 text-white font-medium py-2 px-4 rounded-md text-sm transition-colors"
              >
                登出
              </button>
            </div>
          </div>
        </div>
      </header>
      
      {/* 聊天區域 */}
      <main className="flex-1 overflow-hidden">
        <ChatBot />
      </main>
    </div>
  );
}

export default App;