import { useState, useRef, useEffect } from "react"
import axios from "axios"
import MessageBubble from "./MessageBubble"

export default function ChatWindow() {

  // Store all messages in the conversation
  // Each message = { role: "user" or "bot", text: "..." }
  const [messages, setMessages] = useState([
    {
      role: "bot",
      text: "Hi! Upload a PDF on the left and ask me anything about it."
    }
  ])

  // Store what user is currently typing
  const [input, setInput] = useState("")

  // Track if waiting for bot response
  const [loading, setLoading] = useState(false)

  // Reference to bottom of chat — for auto scrolling
  const bottomRef = useRef(null)

  // Auto scroll to bottom whenever messages change
  // useEffect runs after every render where [messages] changed
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" })
    // ?. means "only call if bottomRef.current exists"
    // behavior: "smooth" = animated scroll
  }, [messages])  // only run when messages array changes


  const sendMessage = async () => {
    const question = input.trim()  // remove extra spaces

    // Don't send if empty or already waiting
    if (!question || loading) return

    // Add user message to chat immediately
    // Don't wait for bot — feels more responsive
    setMessages(prev => [...prev, { role: "user", text: question }])
    // prev → current messages array
    // ...prev → spread/copy all existing messages
    // then add new user message at the end

    setInput("")      // clear input box
    setLoading(true)  // show "Thinking..." bubble

    try {
      // Send question to FastAPI backend
      // const res = await axios.post("http://localhost:8000/ask", {
      //   question  // shorthand for { question: question }
      // })

      // Use VITE_API_URL from .env for backend URL
      const res = await axios.post("http://localhost:8000/ask", {
        question  // shorthand for { question: question }
      })

      // Add bot response to chat
      setMessages(prev => [
        ...prev,
        { role: "bot", text: res.data.answer }
      ])

    } catch (err) {
      // Show error message in chat
      setMessages(prev => [
        ...prev,
        {
          role: "bot",
          text: "Error connecting to backend!!"
        }
      ])
    } finally {
      setLoading(false)  // hide "Thinking..." bubble
    }
  }


  // Send message when Enter key is pressed
  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      // Enter alone → send message
      // Shift+Enter → new line (not sending)
      e.preventDefault()
      sendMessage()
    }
  }


  return (
    <div className="flex-1 flex flex-col h-screen bg-gray-50">

      {/* ── Header ── */}
      <div className="bg-white border-b border-gray-200 px-6 py-4 shadow-sm">
        <h1 className="text-xl font-bold text-gray-800">RAG Chatbot</h1>
        <p className="text-sm text-gray-400">
        
        </p>
      </div>

      {/* ── Messages Area ── */}
      <div className="flex-1 overflow-y-auto px-6 py-4">
        {/* Render each message */}
        {messages.map((msg, index) => (
          <MessageBubble key={index} message={msg} />
        ))}

        {/* Thinking bubble — shows while waiting for response */}
        {loading && (
          <div className="flex justify-start mb-3">
            <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center
                            justify-center text-white text-sm font-bold mr-2 mt-1">
              AI
            </div>
            <div className="bg-white border px-4 py-3 rounded-2xl
                            rounded-bl-none shadow-sm">
              <div className="flex gap-1 items-center">
                {/* Animated dots */}
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                     style={{ animationDelay: "0ms" }} />
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                     style={{ animationDelay: "150ms" }} />
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                     style={{ animationDelay: "300ms" }} />
              </div>
            </div>
          </div>
        )}

        {/* Invisible div at bottom — scroll target */}
        <div ref={bottomRef} />
      </div>

      {/* ── Input Area ── */}
      <div className="bg-white border-t border-gray-200 px-6 py-4">
        <div className="flex gap-3 items-end">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask something about your PDF... (Enter to send)"
            rows={1}
            className="flex-1 border border-gray-300 rounded-xl px-4 py-3
                       text-sm focus:outline-none focus:ring-2
                       focus:ring-blue-500 resize-none"
          />
          <button
            onClick={sendMessage}
            disabled={loading || !input.trim()}
            className="bg-blue-600 text-white px-5 py-3 rounded-xl
                       hover:bg-blue-700 disabled:opacity-50
                       disabled:cursor-not-allowed transition-colors
                       text-sm font-medium whitespace-nowrap"
          >
            {loading ? "..." : "Send ➤"}
          </button>
        </div>
        <p className="text-xs text-gray-400 mt-2">
          Press Enter to send • Shift+Enter for new line
        </p>
      </div>

    </div>
  )
}