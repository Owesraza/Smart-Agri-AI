// AI Chat bubble component
const AIChatBubble = ({ message }) => {
  const isAssistant = message.role === 'assistant'

  return (
    <div className={`flex items-end gap-3 ${isAssistant ? 'justify-start' : 'justify-end'}`}>
      {/* Avatar – only for assistant */}
      {isAssistant && (
        <div className="w-9 h-9 rounded-full bg-gradient-to-br from-[#2E7D32] to-[#81C784] flex items-center justify-center text-white text-sm font-bold flex-shrink-0 mb-1">
          🤖
        </div>
      )}

      <div
        className={`
          max-w-[75%] rounded-2xl px-4 py-3 text-sm leading-relaxed shadow-sm
          ${isAssistant
            ? 'bg-[#F8F9FA] text-[#333333] rounded-bl-md border border-gray-100'
            : 'bg-[#2E7D32] text-white rounded-br-md'
          }
        `}
      >
        <p className="whitespace-pre-wrap">{message.text}</p>
        <p className={`text-xs mt-1.5 ${isAssistant ? 'text-gray-400' : 'text-green-200'}`}>
          {message.time}
        </p>
      </div>

      {/* Avatar – only for user */}
      {!isAssistant && (
        <div className="w-9 h-9 rounded-full bg-gray-200 flex items-center justify-center text-gray-600 text-sm font-bold flex-shrink-0 mb-1">
          👤
        </div>
      )}
    </div>
  )
}

// Typing indicator
export const TypingIndicator = () => (
  <div className="flex items-end gap-3 justify-start">
    <div className="w-9 h-9 rounded-full bg-gradient-to-br from-[#2E7D32] to-[#81C784] flex items-center justify-center text-white text-sm flex-shrink-0">
      🤖
    </div>
    <div className="bg-[#F8F9FA] border border-gray-100 rounded-2xl rounded-bl-md px-4 py-3">
      <div className="flex gap-1.5 items-center h-4">
        {[0, 1, 2].map((i) => (
          <div
            key={i}
            className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
            style={{ animationDelay: `${i * 0.15}s` }}
          />
        ))}
      </div>
    </div>
  </div>
)

export default AIChatBubble
