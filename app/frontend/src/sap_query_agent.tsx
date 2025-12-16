import React, { useState, useRef, useEffect } from 'react';
import { Send, Database, AlertCircle, CheckCircle, Loader, Grid } from 'lucide-react';

export default function QueryAgent() {
  const [messages, setMessages] = useState([]);
  const [table, setTable] = useState('MARA');
  const [fields, setFields] = useState('');
  const [where, setWhere] = useState('');
  const [maxRows, setMaxRows] = useState(5000);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // Available tables (whitelist from RFC)
  const availableTables = ['MARA', 'MARC', 'EKKO', 'EKPO', 'MBEW'];

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Simulate RFC call (in real implementation, this would call ERP system)
  const executeRFC = async (params) => {
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // Mock response data
    const mockData = {
      fields: 'MATNR|CHAR|18,MAKTX|CHAR|40,WERKS|CHAR|4',
      return: 'S',
      message: 'Query executed successfully',
      data: [
        { z_value: 'MAT001|Material 1|1000' },
        { z_value: 'MAT002|Material 2|1000' },
        { z_value: 'MAT003|Material 3|2000' }
      ]
    };
    
    return mockData;
  };

  // Format RFC result as table
  const formatRFCResult = (result) => {
    if (!result || result.return !== 'S') {
      return null;
    }

    // Parse field metadata
    const fieldDefs = result.fields.split(',').map(f => {
      const [name, type, length] = f.split('|');
      return { name, type, length };
    });

    // Parse data rows
    const rows = result.data.map(row => {
      const values = row.z_value.split('|');
      const obj = {};
      fieldDefs.forEach((field, idx) => {
        obj[field.name] = values[idx] || '';
      });
      return obj;
    });

    return { fields: fieldDefs, rows };
  };

  const handleExecute = async () => {
    if (isLoading) return;

    // Create query text for message
    const queryText = `테이블: ${table}\n필드: ${fields || '전체'}\nWHERE: ${where || '없음'}\n최대 행: ${maxRows}`;
    
    const userMessage = { 
      role: 'user', 
      content: queryText,
      params: { table, fields, where, maxRows }
    };
    
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      // Execute RFC with parameters
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: `테이블 ${table} 조회 중...`,
        type: 'executing',
        params: { table, fields, where, maxRows }
      }]);

      const rfcResult = await executeRFC({ table, fields, where, maxRows });
      const formattedResult = formatRFCResult(rfcResult);

      // Show results
      setMessages(prev => {
        const newMessages = [...prev];
        newMessages[newMessages.length - 1] = {
          ...newMessages[newMessages.length - 1],
          type: 'result',
          result: formattedResult,
          rfcResponse: rfcResult
        };
        return newMessages;
      });
    } catch (error) {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: `오류: ${error.message}`,
        type: 'error'
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-gradient-to-br from-blue-950 via-slate-900 to-blue-950">
      {/* Left Panel - Input Form */}
      <div className="w-96 bg-slate-800/50 backdrop-blur-sm border-r border-blue-500/30 flex flex-col">
        {/* Header */}
        <div className="bg-blue-900/30 border-b border-blue-500/30 p-4">
          <div className="flex items-center gap-3">
            <div className="bg-blue-500/20 p-2 rounded-lg">
              <Database className="w-6 h-6 text-blue-400" />
            </div>
            <div>
              <h1 className="text-lg font-bold text-white">RFC Dynamic Query</h1>
              <p className="text-xs text-blue-300">데이터를 안전하게 조회합니다</p>
            </div>
          </div>
        </div>

        {/* Form */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {/* Table */}
          <div>
            <label className="block text-sm font-semibold text-blue-300 mb-2">
              Table
            </label>
            <select
              value={table}
              onChange={(e) => setTable(e.target.value)}
              className="w-full bg-slate-900/60 text-white rounded-lg px-4 py-2.5 border border-blue-500/30 focus:outline-none focus:ring-2 focus:ring-blue-500"
              disabled={isLoading}
            >
              {availableTables.map(t => (
                <option key={t} value={t}>{t}</option>
              ))}
            </select>
          </div>

          {/* Fields */}
          <div>
            <label className="block text-sm font-semibold text-blue-300 mb-2">
              Fields (comma separated)
            </label>
            <input
              type="text"
              value={fields}
              onChange={(e) => setFields(e.target.value)}
              placeholder="예: MATNR, MAKTX (비워두면 전체)"
              className="w-full bg-slate-900/60 text-white rounded-lg px-4 py-2.5 border border-blue-500/30 focus:outline-none focus:ring-2 focus:ring-blue-500 placeholder-blue-400/50"
              disabled={isLoading}
            />
          </div>

          {/* WHERE */}
          <div>
            <label className="block text-sm font-semibold text-blue-300 mb-2">
              WHERE
            </label>
            <textarea
              value={where}
              onChange={(e) => setWhere(e.target.value)}
              placeholder="예: WERKS = '1000' AND MATNR LIKE 'MAT%'"
              rows={3}
              className="w-full bg-slate-900/60 text-white rounded-lg px-4 py-2.5 border border-blue-500/30 focus:outline-none focus:ring-2 focus:ring-blue-500 placeholder-blue-400/50 resize-none"
              disabled={isLoading}
            />
          </div>

          {/* Max Rows */}
          <div>
            <label className="block text-sm font-semibold text-blue-300 mb-2">
              Max Rows
            </label>
            <div className="flex items-center gap-3">
              <input
                type="number"
                value={maxRows}
                onChange={(e) => setMaxRows(Math.min(5000, Math.max(1, parseInt(e.target.value) || 1)))}
                min="1"
                max="5000"
                className="flex-1 bg-slate-900/60 text-white rounded-lg px-4 py-2.5 border border-blue-500/30 focus:outline-none focus:ring-2 focus:ring-blue-500"
                disabled={isLoading}
              />
              <button
                onClick={() => setMaxRows(Math.max(1, maxRows - 100))}
                className="bg-slate-700/50 hover:bg-slate-600/50 text-white rounded-lg px-3 py-2.5 border border-blue-500/30"
                disabled={isLoading}
              >
                -
              </button>
              <button
                onClick={() => setMaxRows(Math.min(5000, maxRows + 100))}
                className="bg-slate-700/50 hover:bg-slate-600/50 text-white rounded-lg px-3 py-2.5 border border-blue-500/30"
                disabled={isLoading}
              >
                +
              </button>
            </div>
          </div>

          {/* Execute Button */}
          <button
            onClick={handleExecute}
            disabled={isLoading}
            className="w-full bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-500 hover:to-blue-400 disabled:from-slate-700 disabled:to-slate-700 disabled:cursor-not-allowed text-white rounded-lg px-6 py-3.5 flex items-center justify-center gap-2 transition-all shadow-lg hover:shadow-blue-500/25 font-semibold"
          >
            {isLoading ? (
              <>
                <Loader className="w-5 h-5 animate-spin" />
                <span>실행 중...</span>
              </>
            ) : (
              <>
                <Send className="w-5 h-5" />
                <span>Execute RFC</span>
              </>
            )}
          </button>
        </div>

        {/* Footer Info */}
        <div className="bg-blue-900/20 border-t border-blue-500/20 p-4">
          <p className="text-xs text-blue-300 flex items-center gap-2">
            <Grid className="w-4 h-4" />
            <span>허용 테이블: {availableTables.join(', ')}</span>
          </p>
        </div>
      </div>

      {/* Right Panel - Messages */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="bg-blue-900/30 backdrop-blur-sm border-b border-blue-500/30 p-4 shadow-lg">
          <div className="max-w-5xl mx-auto">
            <h2 className="text-xl font-bold text-white">Query Results</h2>
            <p className="text-sm text-blue-300">실행 결과가 여기에 표시됩니다</p>
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 bg-slate-900/30">
          <div className="max-w-5xl mx-auto space-y-4">
            {messages.length === 0 && (
              <div className="text-center py-16">
                <div className="bg-blue-500/10 w-24 h-24 rounded-full flex items-center justify-center mx-auto mb-6">
                  <Database className="w-12 h-12 text-blue-400" />
                </div>
                <h2 className="text-2xl font-bold text-white mb-3">
                  쿼리를 실행하세요
                </h2>
                <p className="text-blue-300">
                  왼쪽 패널에서 조회 조건을 입력하고 Execute RFC 버튼을 클릭하세요
                </p>
              </div>
            )}

            {messages.map((msg, idx) => (
              <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-3xl rounded-xl p-4 shadow-lg ${
                  msg.role === 'user' 
                    ? 'bg-gradient-to-r from-blue-600 to-blue-500 text-white' 
                    : 'bg-slate-800/90 backdrop-blur text-blue-50 border border-blue-500/20'
                }`}>
                  {msg.role === 'user' ? (
                    <div>
                      <p className="text-sm font-semibold mb-2">조회 요청</p>
                      <pre className="whitespace-pre-wrap text-sm">{msg.content}</pre>
                    </div>
                  ) : (
                    <>
                      {msg.type === 'executing' && (
                        <div>
                          <div className="flex items-center gap-3 mb-3">
                            <Loader className="w-5 h-5 text-blue-400 animate-spin" />
                            <p className="text-sm font-semibold">{msg.content}</p>
                          </div>
                          <div className="bg-slate-900/70 rounded-lg p-4 text-xs font-mono border border-blue-500/20">
                            <div className="text-blue-400 mb-2 font-semibold">RFC Parameters:</div>
                            <pre className="text-blue-200 overflow-x-auto">
                              {JSON.stringify(msg.params, null, 2)}
                            </pre>
                          </div>
                        </div>
                      )}
                      
                      {msg.type === 'result' && msg.result && (
                        <div>
                          <div className="flex items-center gap-3 mb-4">
                            <CheckCircle className="w-5 h-5 text-green-400" />
                            <p className="text-sm font-semibold">조회 완료</p>
                            <span className="bg-blue-500/20 text-blue-300 px-2 py-1 rounded text-xs">
                              {msg.result.rows.length} rows
                            </span>
                          </div>
                          
                          {/* Data Table */}
                          <div className="overflow-x-auto bg-slate-900/70 rounded-lg border border-blue-500/20">
                            <table className="w-full text-xs">
                              <thead>
                                <tr className="border-b border-blue-500/30 bg-blue-900/20">
                                  {msg.result.fields.map((field, i) => (
                                    <th key={i} className="text-left p-3 font-semibold text-blue-300">
                                      <div className="flex items-center gap-2">
                                        {field.name}
                                        <span className="text-blue-500 text-xs bg-blue-900/30 px-1.5 py-0.5 rounded">
                                          {field.type}
                                        </span>
                                      </div>
                                    </th>
                                  ))}
                                </tr>
                              </thead>
                              <tbody>
                                {msg.result.rows.map((row, i) => (
                                  <tr key={i} className="border-b border-slate-700/50 hover:bg-blue-900/10 transition-colors">
                                    {msg.result.fields.map((field, j) => (
                                      <td key={j} className="p-3 text-blue-100">
                                        {row[field.name]}
                                      </td>
                                    ))}
                                  </tr>
                                ))}
                              </tbody>
                            </table>
                          </div>
                          
                          {/* RFC Response Details */}
                          <details className="mt-4">
                            <summary className="text-xs text-blue-400 cursor-pointer hover:text-blue-300 flex items-center gap-2">
                              <span>응답 상세 보기</span>
                            </summary>
                            <div className="bg-slate-900/70 rounded-lg p-4 text-xs font-mono mt-2 border border-blue-500/20">
                              <pre className="text-blue-200 overflow-x-auto">
                                {JSON.stringify(msg.rfcResponse, null, 2)}
                              </pre>
                            </div>
                          </details>
                        </div>
                      )}
                      
                      {msg.type === 'error' && (
                        <div className="flex items-start gap-3">
                          <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
                          <p className="whitespace-pre-wrap text-sm text-red-300">{msg.content}</p>
                        </div>
                      )}
                    </>
                  )}
                </div>
              </div>
            ))}
            
            <div ref={messagesEndRef} />
          </div>
        </div>
      </div>
    </div>
  );
}