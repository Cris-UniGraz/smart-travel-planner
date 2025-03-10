import React from 'react';

interface ChatMessageProps {
  message: string;
  isUser: boolean;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message, isUser }) => {
  // Función para formatear mensaje y resaltar texto entre corchetes
  const formatMessage = (text: string) => {
    const parts = text.split(/(\[.*?\])/g);
    
    return parts.map((part, index) => {
      // Si el texto está entre corchetes, extraer el contenido y aplicar estilo
      if (part.match(/^\[.*\]$/)) {
        const content = part.substring(1, part.length - 1);
        return <span key={index} className="highlight">{content}</span>;
      }
      return part;
    });
  };

  return (
    <div className={`flex w-full mb-4 ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`max-w-[80%] rounded-lg px-4 py-2 ${
          isUser
            ? 'bg-blue-600 text-white'
            : 'bg-gray-200 text-gray-800'
        }`}
      >
        <p className="whitespace-pre-wrap">{formatMessage(message)}</p>
      </div>
    </div>
  );
};

export default ChatMessage;