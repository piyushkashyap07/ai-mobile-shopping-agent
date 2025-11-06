import { Message } from '../services/api'
import MessageBubble from './MessageBubble'
import ProductCards from './ProductCards'
import './MessageList.css'

interface MessageListProps {
  messages: Message[]
}

const MessageList = ({ messages }: MessageListProps) => {
  return (
    <div className="message-list">
      {messages.map((message, index) => (
        <div key={index} className="message-wrapper">
          <MessageBubble message={message} />
          {message.output && message.output.results && (
            <ProductCards products={message.output.results} />
          )}
        </div>
      ))}
    </div>
  )
}

export default MessageList

