import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface ChatMessage {
  role: string;
  content: string;
}

export interface ChatRequest {
  message: string;
  conversation_id?: string;
}

export interface ChatResponse {
  message: string;
  extracted_entities: string[];
  conversation_id: string;
}

export interface Conversation {
  id: string;
  messages: ChatMessage[];
}

export const sendMessage = async (request: ChatRequest): Promise<ChatResponse> => {
  try {
    const response = await api.post<ChatResponse>('/chat', request);
    return response.data;
  } catch (error) {
    console.error('Error sending message:', error);
    throw error;
  }
};

export const getConversation = async (conversationId: string): Promise<Conversation> => {
  try {
    const response = await api.get<Conversation>(`/conversations/${conversationId}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching conversation:', error);
    throw error;
  }
};

export default api;