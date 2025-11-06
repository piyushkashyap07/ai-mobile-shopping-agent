import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

export interface Message {
  role: 'user' | 'assistant'
  content: string
  timestamp: string
  output?: any
}

export interface Product {
  'Company Name': string
  'Model Name': string
  'Mobile Weight': string
  RAM: string
  'Front Camera': string
  'Back Camera': string
  Processor: string
  'Battery Capacity': string
  'Screen Size': string
  'Launched Price (India)': string
  'Launched Year': number
  Price_INR?: number
  RAM_GB?: number
  Battery_mAh?: number
  Weight_g?: number
  Screen_Size_inches?: number
}

export interface ConversationResponse {
  conversation_id: string
  email: string
  created_at: string
}

export interface MessageResponse {
  conversation_id: string
  timestamp: string
  response: string
  output?: {
    results?: Product[]
    success?: boolean
  }
  predicted_sql_query?: string
  user_query?: string
}

export const createConversation = async (email: string): Promise<ConversationResponse> => {
  const response = await axios.post<ConversationResponse>(`${API_BASE_URL}/conversation/`, {
    email,
  })
  return response.data
}

export const sendMessage = async (
  conversationId: string,
  message: string
): Promise<MessageResponse> => {
  const response = await axios.post<MessageResponse>(`${API_BASE_URL}/conversation/message`, {
    conversation_id: conversationId,
    user_message: message,
  })
  return response.data
}

