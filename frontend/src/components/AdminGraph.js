import React, { useState } from 'react';

const AdminGraph = ({ token }) => {
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8001/api';

  const handleCreateGraph = async () => {
    if (!text.trim()) return alert('請輸入文字');

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch(`${API_BASE_URL}/graphrag/create/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Token ${token}`,
        },
        body: JSON.stringify({ text }),
      });

      const data = await response.json();
      if (response.ok) {
        setResult(data.message || '圖譜建立成功！');
      } else {
        setError(data.error || '建立失敗');
      }
    } catch (err) {
      setError('網路錯誤，請稍後再試');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 max-w-3xl mx-auto">
      <h2 className="text-2xl font-bold mb-4">建立知識圖譜</h2>
      <textarea
        className="w-full border rounded-md p-2 mb-4"
        rows={6}
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="請輸入文字內容，按下建立圖譜"
      />
      <button
        onClick={handleCreateGraph}
        disabled={loading}
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
      >
        {loading ? '建立中...' : '建立圖譜'}
      </button>

      {result && <div className="mt-4 text-green-600">{result}</div>}
      {error && <div className="mt-4 text-red-600">{error}</div>}
    </div>
  );
};

export default AdminGraph;
