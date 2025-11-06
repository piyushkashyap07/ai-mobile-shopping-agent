import React from 'react'
import { Message } from '../services/api'
import './MessageBubble.css'

interface MessageBubbleProps {
  message: Message
}

// Format markdown-like text: **bold**, ### headings, etc.
const formatText = (text: string): React.ReactNode[] => {
  const parts: React.ReactNode[] = []
  const lines = text.split('\n')
  
  lines.forEach((line, lineIndex) => {
    // Check for headings first
    if (line.match(/^###\s+/)) {
      const match = line.match(/^###\s+(.+)$/)
      if (match) {
        parts.push(<h3 key={`h3-${lineIndex}`} className="markdown-h3">{match[1]}</h3>)
        return
      }
    }
    if (line.match(/^##\s+/)) {
      const match = line.match(/^##\s+(.+)$/)
      if (match) {
        parts.push(<h2 key={`h2-${lineIndex}`} className="markdown-h2">{match[1]}</h2>)
        return
      }
    }
    if (line.match(/^#\s+/)) {
      const match = line.match(/^#\s+(.+)$/)
      if (match) {
        parts.push(<h1 key={`h1-${lineIndex}`} className="markdown-h1">{match[1]}</h1>)
        return
      }
    }
    
    // Process bold and italic within the line
    let processedLine: React.ReactNode[] = []
    let lineText = line
    
    // Process bold text (**text**)
    const boldPattern = /\*\*(.+?)\*\*/g
    let boldMatch
    const boldMatches: Array<{ start: number; end: number; text: string }> = []
    
    while ((boldMatch = boldPattern.exec(lineText)) !== null) {
      boldMatches.push({
        start: boldMatch.index,
        end: boldMatch.index + boldMatch[0].length,
        text: boldMatch[1]
      })
    }
    
    // Process italic text (*text*) - but not **text**
    const italicPattern = /(?<!\*)\*([^*]+?)\*(?!\*)/g
    let italicMatch
    const italicMatches: Array<{ start: number; end: number; text: string }> = []
    
    while ((italicMatch = italicPattern.exec(lineText)) !== null) {
      // Check if it's not part of a bold pattern
      const isInsideBold = boldMatches.some(bm => 
        italicMatch.index >= bm.start && italicMatch.index <= bm.end
      )
      if (!isInsideBold) {
        italicMatches.push({
          start: italicMatch.index,
          end: italicMatch.index + italicMatch[0].length,
          text: italicMatch[1]
        })
      }
    }
    
    // Combine and sort all matches
    const allMatches = [
      ...boldMatches.map(m => ({ ...m, type: 'bold' as const })),
      ...italicMatches.map(m => ({ ...m, type: 'italic' as const }))
    ].sort((a, b) => a.start - b.start)
    
    // Build the line with formatted parts
    let currentPos = 0
    allMatches.forEach((match, idx) => {
      // Add text before the match
      if (match.start > currentPos) {
        processedLine.push(<span key={`text-${lineIndex}-${idx}-before`}>{lineText.substring(currentPos, match.start)}</span>)
      }
      
      // Add the formatted match
      if (match.type === 'bold') {
        processedLine.push(<strong key={`bold-${lineIndex}-${idx}`}>{match.text}</strong>)
      } else {
        processedLine.push(<em key={`italic-${lineIndex}-${idx}`}>{match.text}</em>)
      }
      
      currentPos = match.end
    })
    
    // Add remaining text
    if (currentPos < lineText.length) {
      processedLine.push(<span key={`text-${lineIndex}-end`}>{lineText.substring(currentPos)}</span>)
    }
    
    // If no matches, just add the line as is
    if (processedLine.length === 0) {
      processedLine.push(<span key={`text-${lineIndex}`}>{lineText}</span>)
    }
    
    parts.push(
      <p key={`line-${lineIndex}`}>
        {processedLine}
      </p>
    )
  })
  
  return parts
}

const MessageBubble = ({ message }: MessageBubbleProps) => {
  const isUser = message.role === 'user'

  return (
    <div className={`message-bubble ${isUser ? 'user' : 'assistant'}`}>
      <div className="message-content">
        {formatText(message.content)}
      </div>
    </div>
  )
}

export default MessageBubble
