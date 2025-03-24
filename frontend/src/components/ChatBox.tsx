import React, { useState, useEffect, useRef } from 'react';
import { v4 as uuidv4 } from 'uuid';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';
import { sendMessage, ChatResponse, ChatMessage as ChatMessageType } from '@/services/api';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Loader2 } from 'lucide-react';

const ChatBox: React.FC = () => {
  const [messages, setMessages] = useState<{ text: string; isUser: boolean }[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Mensaje de bienvenida inicial
  useEffect(() => {
    setMessages([
      {
        text: 'Willkommen beim smart travel planner der Universität Graz!' + '\n' + 'Um zu beginnen, geben Sie mir bitte Ihren Namen.',
        isUser: false,
      },
    ]);
  }, []);

  // Desplazamiento automático al último mensaje
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = async (text: string) => {
    try {
      setError(null);
      setIsLoading(true);
      
      // Añadir el mensaje del usuario a la interfaz
      setMessages((prev) => [...prev, { text, isUser: true }]);

      // Enviar el mensaje a la API
      const response = await sendMessage({
        message: text,
        conversation_id: conversationId || undefined,
      });

      // Guardar el ID de la conversación
      if (!conversationId) {
        setConversationId(response.conversation_id);
      }

      // Añadir la respuesta del asistente a la interfaz
      setMessages((prev) => [
        ...prev,
        { text: response.message, isUser: false },
      ]);
    } catch (err) {
      console.error('Error al enviar mensaje:', err);
      setError('Error al comunicarse con el servidor. Por favor, inténtalo de nuevo.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full bg-[#f0f2f5]">
      <ScrollArea className="flex-grow px-4 py-3">
        <div className="max-w-3xl mx-auto">
          <div className="flex flex-col space-y-1 py-2">
            {messages.map((message, index) => (
              <ChatMessage
                key={index}
                message={message.text}
                isUser={message.isUser}
              />
            ))}
            {error && (
              <div className="text-destructive text-center text-sm mt-2 mb-2 py-2 px-3 rounded-md bg-destructive/10">
                {error}
              </div>
            )}
            {isLoading && (
              <div className="flex items-center gap-2 justify-center mt-2 mb-2 text-muted-foreground">
                <Loader2 className="h-4 w-4 animate-spin" />
                <span className="text-sm">Der Assistent schreibt...</span>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        </div>
      </ScrollArea>
      <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading} />
    </div>
  );
};

export default ChatBox;