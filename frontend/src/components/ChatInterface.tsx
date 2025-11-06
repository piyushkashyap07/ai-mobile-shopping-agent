import { useState, useRef, useEffect } from 'react'
import { sendMessage, createConversation, Message } from '../services/api'
import MessageList from './MessageList'
import InputArea from './InputArea'
import './ChatInterface.css'

const ChatInterface = () => {
  const [messages, setMessages] = useState<Message[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [conversationId, setConversationId] = useState<string | null>(null)
  const [email, setEmail] = useState('')
  const [showEmailInput, setShowEmailInput] = useState(true)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleEmailSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!email.trim()) return

    try {
      const response = await createConversation(email)
      setConversationId(response.conversation_id)
      setShowEmailInput(false)
      setMessages([{
        role: 'assistant',
        content: 'Hi! I\'m your mobile phone shopping assistant for the Indian market. I can help you find the perfect phone based on your budget, preferences, and needs. All prices are in Indian Rupees (₹). How can I help you today?',
        timestamp: new Date().toISOString()
      }])
    } catch (error) {
      console.error('Failed to create conversation:', error)
      alert('Failed to start conversation. Please try again.')
    }
  }

  const handleSendMessage = async (text: string) => {
    if (!text.trim() || !conversationId) return

    const userMessage: Message = {
      role: 'user',
      content: text,
      timestamp: new Date().toISOString()
    }

    setMessages(prev => [...prev, userMessage])
    setIsLoading(true)

    try {
      const response = await sendMessage(conversationId, text)
      const assistantMessage: Message = {
        role: 'assistant',
        content: response.response,
        timestamp: response.timestamp,
        output: response.output
      }
      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      console.error('Failed to send message:', error)
      const errorMessage: Message = {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toISOString()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  if (showEmailInput) {
    return (
      <div className="chat-container">
        <div className="email-input-container">
          <div className="welcome-card">
            <h1>📱 Mobile Shopping Chat Agent</h1>
            <p className="subtitle">India Market - All Prices in ₹ (INR)</p>
            <form onSubmit={handleEmailSubmit} className="email-form">
              <input
                type="email"
                placeholder="Enter your email to start"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="email-input"
                required
              />
              <button type="submit" className="start-button">
                Start Chatting
              </button>
            </form>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h1>📱 Mobile Shopping Assistant</h1>
        <p className="market-indicator">🇮🇳 India Market | Currency: ₹ (INR)</p>
      </div>
      <div className="messages-container">
        <MessageList messages={messages} />
        {isLoading && (
          <div className="loading-indicator">
            <div className="typing-dots">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      <InputArea onSendMessage={handleSendMessage} disabled={isLoading} />
    </div>
  )
}

export default ChatInterface

