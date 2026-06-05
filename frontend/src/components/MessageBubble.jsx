// MessageBubble.jsx
// Displays a single chat message
// Looks different depending on who sent it (user or bot)

export default function MessageBubble({ message }) {
  // { message } is destructuring props
  // same as: function MessageBubble(props) { const message = props.message }

  // Check who sent this message
  const isUser = message.role === "user"

  return (
    <div className={`flex mb-3 ${isUser ? "justify-end" : "justify-start"}`}>
      {/* justify-end  → user messages appear on RIGHT */}
      {/* justify-start → bot messages appear on LEFT  */}

      {/* Bot avatar — only show for bot messages */}
      {!isUser && (
        <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center
                        justify-center text-white text-sm font-bold mr-2 mt-1">
          AI
        </div>
      )}

      {/* Message bubble */}
      <div className={`max-w-xs lg:max-w-md px-4 py-3 rounded-2xl text-sm
                       leading-relaxed
        ${isUser
          ? "bg-blue-600 text-white rounded-br-none"
          : "bg-white text-gray-800 rounded-bl-none shadow-sm border"
        }`}>

        {/* Split by newline so code blocks display properly */}
        {message.text.split("\n").map((line, i) => (
          <span key={i}>
            {line}
            <br />
          </span>
        ))}
      </div>

      {/* User avatar — only show for user messages */}
      {isUser && (
        <div className="w-8 h-8 rounded-full bg-gray-400 flex items-center
                        justify-center text-white text-sm font-bold ml-2 mt-1">
          You
        </div>
      )}
    </div>
  )
}