import os

components.html(
    f"""
<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>RFC Dynamic Query</title>
  <link
    href=\"https://cdn.jsdelivr.net/npm/tailwindcss@3.4.4/dist/tailwind.min.css\"
    rel=\"stylesheet\"
  />
  <style>
    body {{ margin: 0; background: #0f172a; }}
    .scrollbar-hide::-webkit-scrollbar {{ display: none; }}
    .scrollbar-hide {{ -ms-overflow-style: none; scrollbar-width: none; }}
  </style>
</head>
<body>
  <div id=\"root\"></div>
  <script crossorigin src=\"https://unpkg.com/react@18/umd/react.production.min.js\"></script>
  <script crossorigin src=\"https://unpkg.com/react-dom@18/umd/react-dom.production.min.js\"></script>
  <script type=\"module\">

    const {{ useEffect, useRef, useState }} = React;
    const IconFactory = (symbol) => ({{ className = "" }}) =>
      React.createElement("span", {{ className }}, symbol);

    const Send = IconFactory("📤");
    const Database = IconFactory("🗄️");
    const AlertCircle = IconFactory("⚠️");
    const CheckCircle = IconFactory("✅");
    const Loader = IconFactory("⏳");
    const Grid = IconFactory("🔎");

    const apiBaseUrl = "{API_BASE_URL}";

    function QueryAgent() {{
      const [messages, setMessages] = useState([]);
      const [table, setTable] = useState("MARA");
      const [fields, setFields] = useState("");
      const [where, setWhere] = useState("");
      const [maxRows, setMaxRows] = useState(5000);
      const [isLoading, setIsLoading] = useState(false);
      const messagesEndRef = useRef(null);

      const availableTables = ["MARA", "MARC", "EKKO", "EKPO", "MBEW"];

      const scrollToBottom = () => {{
        messagesEndRef.current?.scrollIntoView({{ behavior: "smooth" }});
      }};

      useEffect(() => {{
        scrollToBottom();
      }}, [messages]);

      const executeRFC = async (params) => {{
        const response = await fetch(`${{apiBaseUrl}}/erp/dynamic-query`, {{
          method: "POST",
          headers: {{ "Content-Type": "application/json" }},
          body: JSON.stringify({{
            table: params.table,
            fields: params.fields,
            where: params.where,
            maxrows: params.maxRows,
          }}),
        }});

        if (!response.ok) {{
          const text = await response.text();
          throw new Error(text || `Request failed with status ${{response.status}}`);
        }}

        return response.json();
      }};

      const formatRFCResult = (result) => {{
        if (!result || result.return !== "S") return null;

        const fieldDefs = (result.fields || "")
          .split(",")
          .filter(Boolean)
          .map((f) => {{
            const [name, type, length] = f.split("|");
            return {{ name, type, length }};
          }});

        const rows = (result.data || []).map((row) => {{
          const values = (row.z_value || "").split("|");
          const obj = {{}};
          fieldDefs.forEach((field, idx) => {{
            obj[field.name] = values[idx] || "";
          }});
          return obj;
        }});

        return {{ fields: fieldDefs, rows }};
      }};

      const handleExecute = async () => {{
        if (isLoading) return;

        const queryText = `테이블: ${{table}}\n필드: ${{fields || "전체"}}\nWHERE: ${{where || "없음"}}\n최대 행: ${{maxRows}}`;

        const userMessage = {{
          role: "user",
          content: queryText,
          params: {{ table, fields, where, maxRows }},
        }};

        setMessages((prev) => [...prev, userMessage]);
        setIsLoading(true);

        try {{
          setMessages((prev) => [...prev, {{
            role: "assistant",
            content: `테이블 ${{table}} 조회 중...`,
            type: "executing",
            params: {{ table, fields, where, maxRows }},
          }}]);

          const rfcResult = await executeRFC({{ table, fields, where, maxRows }});
          const formattedResult = formatRFCResult(rfcResult);

          setMessages((prev) => {{
            const newMessages = [...prev];
            newMessages[newMessages.length - 1] = {{
              ...newMessages[newMessages.length - 1],
              type: "result",
              result: formattedResult,
              rfcResponse: rfcResult,
            }};
            return newMessages;
          }});
        }} catch (error) {{
          setMessages((prev) => [...prev, {{
            role: "assistant",
            content: `오류: ${{error.message}}`,
            type: "error",
          }}]);
        }} finally {{
          setIsLoading(false);
        }}
      }};

      return (
        React.createElement(
          "div",
          {{ className: "flex h-screen bg-gradient-to-br from-blue-950 via-slate-900 to-blue-950" }},
          React.createElement(
            "div",
            {{ className: "w-96 bg-slate-800/50 backdrop-blur-sm border-r border-blue-500/30 flex flex-col" }},
            React.createElement(
              "div",
              {{ className: "bg-blue-900/30 border-b border-blue-500/30 p-4" }},
              React.createElement(
                "div",
                {{ className: "flex items-center gap-3" }},
                React.createElement(
                  "div",
                  {{ className: "bg-blue-500/20 p-2 rounded-lg" }},
                  React.createElement(Database, {{ className: "w-6 h-6 text-blue-400" }})
                ),
                React.createElement(
                  "div",
                  null,
                  React.createElement(
                    "h1",
                    {{ className: "text-lg font-bold text-white" }},
                    "RFC Dynamic Query"
                  ),
                  React.createElement(
                    "p",
                    {{ className: "text-xs text-blue-300" }},
                    "데이터를 안전하게 조회합니다"
                  )
                )
              )
            ),

            React.createElement(
              "div",
              {{ className: "flex-1 overflow-y-auto p-6 space-y-6 scrollbar-hide" }},
              React.createElement(
                "div",
                null,
                React.createElement(
                  "label",
                  {{ className: "block text-sm font-semibold text-blue-300 mb-2" }},
                  "Table"
                ),
                React.createElement(
                  "select",
                  {{
                    value: table,
                    onChange: (e) => setTable(e.target.value),
                    className:
                      "w-full bg-slate-900/60 text-white rounded-lg px-4 py-2.5 border border-blue-500/30 focus:outline-none focus:ring-2 focus:ring-blue-500",
                    disabled: isLoading,
                  }},
                  availableTables.map((t) =>
                    React.createElement("option", {{ key: t, value: t }}, t)
                  )
                )
              ),

              React.createElement(
                "div",
                null,
                React.createElement(
                  "label",
                  {{ className: "block text-sm font-semibold text-blue-300 mb-2" }},
                  "Fields (comma separated)"
                ),
                React.createElement("input", {{
                  type: "text",
                  value: fields,
                  onChange: (e) => setFields(e.target.value),
                  placeholder: "예: MATNR, MAKTX (비워두면 전체)",
                  className:
                    "w-full bg-slate-900/60 text-white rounded-lg px-4 py-2.5 border border-blue-500/30 focus:outline-none focus:ring-2 focus:ring-blue-500 placeholder-blue-400/50",
                  disabled: isLoading,
                }})
              ),

              React.createElement(
                "div",
                null,
                React.createElement(
                  "label",
                  {{ className: "block text-sm font-semibold text-blue-300 mb-2" }},
                  "WHERE"
                ),
                React.createElement("textarea", {{
                  value: where,
                  onChange: (e) => setWhere(e.target.value),
                  placeholder: "예: WERKS = '1000' AND MATNR LIKE 'MAT%'",
                  rows: 3,
                  className:
                    "w-full bg-slate-900/60 text-white rounded-lg px-4 py-2.5 border border-blue-500/30 focus:outline-none focus:ring-2 focus:ring-blue-500 placeholder-blue-400/50 resize-none",
                  disabled: isLoading,
                }})
              ),

              React.createElement(
                "div",
                null,
                React.createElement(
                  "label",
                  {{ className: "block text-sm font-semibold text-blue-300 mb-2" }},
                  "Max Rows"
                ),
                React.createElement(
                  "div",
                  {{ className: "flex items-center gap-3" }},
                  React.createElement("input", {{
                    type: "number",
                    value: maxRows,
                    onChange: (e) =>
                      setMaxRows(Math.min(5000, Math.max(1, parseInt(e.target.value) || 1))),
                    min: "1",
                    max: "5000",
                    className:
                      "flex-1 bg-slate-900/60 text-white rounded-lg px-4 py-2.5 border border-blue-500/30 focus:outline-none focus:ring-2 focus:ring-blue-500",
                    disabled: isLoading,
                  }}),
                  React.createElement(
                    "button",
                    {{
                      onClick: () => setMaxRows((value) => Math.max(1, value - 100)),
                      className:
                        "bg-slate-700/50 hover:bg-slate-600/50 text-white rounded-lg px-3 py-2.5 border border-blue-500/30",
                      disabled: isLoading,
                    }},
                    "-"
                  ),
                  React.createElement(
                    "button",
                    {{
                      onClick: () => setMaxRows((value) => Math.min(5000, value + 100)),
                      className:
                        "bg-slate-700/50 hover:bg-slate-600/50 text-white rounded-lg px-3 py-2.5 border border-blue-500/30",
                      disabled: isLoading,
                    }},
                    "+"
                  )
                )
              ),

              React.createElement(
                "button",
                {{
                  onClick: handleExecute,
                  disabled: isLoading,
                  className:
                    "w-full bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-500 hover:to-blue-400 disabled:from-slate-700 disabled:to-slate-700 disabled:cursor-not-allowed text-white rounded-lg px-6 py-3.5 flex items-center justify-center gap-2 transition-all shadow-lg hover:shadow-blue-500/25 font-semibold",
                }},
                isLoading
                  ? React.createElement(
                      React.Fragment,
                      null,
                      React.createElement(Loader, {{ className: "w-5 h-5 animate-spin" }}),
                      React.createElement("span", null, "실행 중...")
                    )
                  : React.createElement(
                      React.Fragment,
                      null,
                      React.createElement(Send, {{ className: "w-5 h-5" }}),
                      React.createElement("span", null, "Execute RFC")
                    )
              )
            ),

            React.createElement(
              "div",
              {{ className: "bg-blue-900/20 border-t border-blue-500/20 p-4" }},
              React.createElement(
                "p",
                {{ className: "text-xs text-blue-300 flex items-center gap-2" }},
                React.createElement(Grid, {{ className: "w-4 h-4" }}),
                React.createElement(
                  "span",
                  null,
                  `허용 테이블: ${{availableTables.join(", ")}}`
                )
              )
            )
          ),

          React.createElement(
            "div",
            {{ className: "flex-1 flex flex-col" }},
            React.createElement(
              "div",
              {{ className: "bg-blue-900/30 backdrop-blur-sm border-b border-blue-500/30 p-4 shadow-lg" }},
              React.createElement(
                "div",
                {{ className: "max-w-5xl mx-auto" }},
                React.createElement(
                  "h2",
                  {{ className: "text-xl font-bold text-white" }},
                  "Query Results"
                ),
                React.createElement(
                  "p",
                  {{ className: "text-sm text-blue-300" }},
                  "실행 결과가 여기에 표시됩니다"
                )
              )
            ),

            React.createElement(
              "div",
              {{ className: "flex-1 overflow-y-auto p-4 bg-slate-900/30 scrollbar-hide" }},
              React.createElement(
                "div",
                {{ className: "max-w-5xl mx-auto space-y-4" }},
                messages.length === 0 &&
                  React.createElement(
                    "div",
                    {{ className: "text-center py-16" }},
                    React.createElement(
                      "div",
                      {{ className: "bg-blue-500/10 w-24 h-24 rounded-full flex items-center justify-center mx-auto mb-6" }},
                      React.createElement(Database, {{ className: "w-12 h-12 text-blue-400" }})
                    ),
                    React.createElement(
                      "h2",
                      {{ className: "text-2xl font-bold text-white mb-3" }},
                      "쿼리를 실행하세요"
                    ),
                    React.createElement(
                      "p",
                      {{ className: "text-blue-300" }},
                      "왼쪽 패널에서 조회 조건을 입력하고 Execute RFC 버튼을 클릭하세요"
                    )
                  ),

                messages.map((msg, idx) =>
                  React.createElement(
                    "div",
                    {{
                      key: idx,
                      className: `flex ${{msg.role === "user" ? "justify-end" : "justify-start"}}`,
                    }},
                    React.createElement(
                      "div",
                      {{
                        className: `max-w-3xl rounded-xl p-4 shadow-lg ${{
                          msg.role === "user"
                            ? "bg-gradient-to-r from-blue-600 to-blue-500 text-white"
                            : "bg-slate-800/90 backdrop-blur text-blue-50 border border-blue-500/20"
                        }}`,
                      }},
                      msg.role === "user"
                        ? React.createElement(
                            "div",
                            null,
                            React.createElement(
                              "p",
                              {{ className: "text-sm font-semibold mb-2" }},
                              "조회 요청"
                            ),
                            React.createElement(
                              "pre",
                              {{ className: "whitespace-pre-wrap text-sm" }},
                              msg.content
                            )
                          )
                        : React.createElement(
                            React.Fragment,
                            null,
                            msg.type === "executing" &&
                              React.createElement(
                                "div",
                                null,
                                React.createElement(
                                  "div",
                                  {{ className: "flex items-center gap-3 mb-3" }},
                                  React.createElement(Loader, {{ className: "w-5 h-5 text-blue-400 animate-spin" }}),
                                  React.createElement(
                                    "p",
                                    {{ className: "text-sm font-semibold" }},
                                    msg.content
                                  )
                                ),
                                React.createElement(
                                  "div",
                                  {{ className: "bg-slate-900/70 rounded-lg p-4 text-xs font-mono border border-blue-500/20" }},
                                  React.createElement(
                                    "div",
                                    {{ className: "text-blue-400 mb-2 font-semibold" }},
                                    "RFC Parameters:"
                                  ),
                                  React.createElement(
                                    "pre",
                                    {{ className: "text-blue-200 overflow-x-auto" }},
                                    JSON.stringify(msg.params, null, 2)
                                  )
                                )
                              ),

                            msg.type === "result" &&
                              msg.result &&
                              React.createElement(
                                "div",
                                null,
                                React.createElement(
                                  "div",
                                  {{ className: "flex items-center gap-3 mb-4" }},
                                  React.createElement(CheckCircle, {{ className: "w-5 h-5 text-green-400" }}),
                                  React.createElement(
                                    "p",
                                    {{ className: "text-sm font-semibold" }},
                                    "조회 완료"
                                  ),
                                  React.createElement(
                                    "span",
                                    {{ className: "bg-blue-500/20 text-blue-300 px-2 py-1 rounded text-xs" }},
                                    `${{msg.result.rows.length}} rows`
                                  )
                                ),

                                React.createElement(
                                  "div",
                                  {{ className: "overflow-x-auto bg-slate-900/70 rounded-lg border border-blue-500/20" }},
                                  React.createElement(
                                    "table",
                                    {{ className: "w-full text-xs" }},
                                    React.createElement(
                                      "thead",
                                      null,
                                      React.createElement(
                                        "tr",
                                        {{ className: "border-b border-blue-500/30 bg-blue-900/20" }},
                                        msg.result.fields.map((field, i) =>
                                          React.createElement(
                                            "th",
                                            {{
                                              key: i,
                                              className: "text-left p-3 font-semibold text-blue-300",
                                            }},
                                            React.createElement(
                                              "div",
                                              {{ className: "flex items-center gap-2" }},
                                              field.name,
                                              React.createElement(
                                                "span",
                                                {{ className: "text-blue-500 text-xs bg-blue-900/30 px-1.5 py-0.5 rounded" }},
                                                field.type
                                              )
                                            )
                                          )
                                        )
                                      )
                                    ),
                                    React.createElement(
                                      "tbody",
                                      null,
                                      msg.result.rows.map((row, i) =>
                                        React.createElement(
                                          "tr",
                                          {{
                                            key: i,
                                            className: "border-b border-slate-700/50 hover:bg-blue-900/10 transition-colors",
                                          }},
                                          msg.result.fields.map((field, j) =>
                                            React.createElement(
                                              "td",
                                              {{ key: j, className: "p-3 text-blue-100" }},
                                              row[field.name]
                                            )
                                          )
                                        )
                                      )
                                    )
                                  )
                                ),

                                React.createElement(
                                  "details",
                                  {{ className: "mt-4" }},
                                  React.createElement(
                                    "summary",
                                    {{ className: "text-xs text-blue-400 cursor-pointer hover:text-blue-300 flex items-center gap-2" }},
                                    React.createElement("span", null, "응답 상세 보기")
                                  ),
                                  React.createElement(
                                    "div",
                                    {{ className: "bg-slate-900/70 rounded-lg p-4 text-xs font-mono mt-2 border border-blue-500/20" }},
                                    React.createElement(
                                      "pre",
                                      {{ className: "text-blue-200 overflow-x-auto" }},
                                      JSON.stringify(msg.rfcResponse, null, 2)
                                    )
                                  )
                                )
                              ),

                            msg.type === "error" &&
                              React.createElement(
                                "div",
                                {{ className: "flex items-start gap-3" }},
                                React.createElement(AlertCircle, {{ className: "w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" }}),
                                React.createElement(
                                  "p",
                                  {{ className: "whitespace-pre-wrap text-sm text-red-300" }},
                                  msg.content
                                )
                              )
                          )
                    )
                  )
                ),

                React.createElement("div", {{ ref: messagesEndRef }})
              )
            )
          )
        )
      );
    }}

    const root = ReactDOM.createRoot(document.getElementById("root"));
    root.render(React.createElement(QueryAgent));
  </script>
</body>
</html>
""",
    height=900,
    scrolling=True,
)

