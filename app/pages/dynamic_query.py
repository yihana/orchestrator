import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

HTML = """
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>RFC Dynamic Query</title>

  <!-- Tailwind -->
  <script src="https://cdn.tailwindcss.com"></script>

  <!-- React (UMD) -->
  <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
  <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>

  <style>
    body { margin: 0; background: #020617; }
  </style>
</head>

<body>
<div id="root"></div>

<script>
const { useState, useEffect, useRef } = React;

/* 아이콘 대체 (lucide 제거) */
const Icon = (symbol) =>
  (props) => React.createElement("span", { className: props.className }, symbol);

const Send = Icon("📤");
const Database = Icon("🗄️");
const AlertCircle = Icon("⚠️");
const CheckCircle = Icon("✅");
const Loader = Icon("⏳");
const Grid = Icon("🔎");

function QueryAgent() {
  const [messages, setMessages] = useState([]);
  const [table, setTable] = useState("MARA");
  const [fields, setFields] = useState("");
  const [where, setWhere] = useState("");
  const [maxRows, setMaxRows] = useState(5000);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const availableTables = ["MARA", "MARC", "EKKO", "EKPO", "MBEW"];

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function executeRFC(params) {
    await new Promise(r => setTimeout(r, 800));
    return {
      return: "S",
      fields: "MATNR|CHAR|18,MAKTX|CHAR|40,WERKS|CHAR|4",
      data: [
        { z_value: "MAT001|Material 1|1000" },
        { z_value: "MAT002|Material 2|1000" },
        { z_value: "MAT003|Material 3|2000" }
      ]
    };
  }

  function formatRFCResult(result) {
    if (!result || result.return !== "S") return null;

    const fields = result.fields.split(",").map(f => {
      const [name, type, length] = f.split("|");
      return { name, type, length };
    });

    const rows = result.data.map(r => {
      const values = r.z_value.split("|");
      const obj = {};
      fields.forEach((f, i) => obj[f.name] = values[i] || "");
      return obj;
    });

    return { fields, rows };
  }

  async function handleExecute() {
    if (isLoading) return;
    setIsLoading(true);

    const userMessage = {
      role: "user",
      content:
        "테이블: " + table + "\\n" +
        "필드: " + (fields || "전체") + "\\n" +
        "WHERE: " + (where || "없음") + "\\n" +
        "최대 행: " + maxRows
    };

    setMessages(m => [...m, userMessage, {
      role: "assistant",
      type: "executing",
      content: "테이블 " + table + " 조회 중..."
    }]);

    try {
      const res = await executeRFC({ table, fields, where, maxRows });
      const formatted = formatRFCResult(res);

      setMessages(m => {
        const next = [...m];
        next[next.length - 1] = {
          role: "assistant",
          type: "result",
          result: formatted
        };
        return next;
      });
    } catch (e) {
      setMessages(m => [...m, {
        role: "assistant",
        type: "error",
        content: e.message
      }]);
    } finally {
      setIsLoading(false);
    }
  }

  return React.createElement(
    "div",
    { className: "flex h-screen bg-gradient-to-br from-blue-950 via-slate-900 to-blue-950 text-white" },

    /* 좌측 패널 */
    React.createElement(
      "div",
      { className: "w-96 bg-slate-800/60 border-r border-blue-500/30 flex flex-col p-4 space-y-4" },

      React.createElement("h1", { className: "text-lg font-bold flex gap-2 items-center" },
        React.createElement(Database, null),
        "RFC Dynamic Query"
      ),

      React.createElement("select", {
        className: "bg-slate-900 p-2 rounded",
        value: table,
        onChange: e => setTable(e.target.value)
      }, availableTables.map(t =>
        React.createElement("option", { key: t, value: t }, t)
      )),

      React.createElement("input", {
        className: "bg-slate-900 p-2 rounded",
        placeholder: "Fields",
        value: fields,
        onChange: e => setFields(e.target.value)
      }),

      React.createElement("textarea", {
        className: "bg-slate-900 p-2 rounded",
        placeholder: "WHERE",
        value: where,
        rows: 3,
        onChange: e => setWhere(e.target.value)
      }),

      React.createElement("button", {
        onClick: handleExecute,
        disabled: isLoading,
        className: "bg-blue-600 hover:bg-blue-500 p-3 rounded flex justify-center gap-2"
      },
        isLoading ? React.createElement(Loader) : React.createElement(Send),
        " Execute"
      )
    ),

    /* 우측 결과 */
    React.createElement(
      "div",
      { className: "flex-1 p-6 overflow-y-auto" },
      messages.map((m, i) =>
        React.createElement("pre", {
          key: i,
          className: "mb-4 p-4 rounded bg-slate-800/80"
        },
          m.type === "result"
            ? JSON.stringify(m.result, null, 2)
            : m.content
        )
      ),
      React.createElement("div", { ref: messagesEndRef })
    )
  );
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(React.createElement(QueryAgent));
</script>
</body>
</html>
"""

components.html(HTML, height=900, scrolling=True)
