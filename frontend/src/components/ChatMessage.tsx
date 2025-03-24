import React from 'react';
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { cn } from "@/lib/utils";

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
        return <span key={index} className="highlight font-medium">{content}</span>;
      }
      return part;
    });
  };

  return (
    <div className={cn(
      "flex w-full mb-3 items-end gap-2",
      isUser ? "justify-end" : "justify-start"
    )}>
      {!isUser && (
        <Avatar className="h-8 w-8 mb-1">
          <AvatarFallback className="bg-primary text-primary-foreground text-xs">STP</AvatarFallback>
        </Avatar>
      )}
      <div
        className={cn(
          "max-w-[80%] px-3 py-2 shadow-sm whitespace-pre-wrap",
          isUser 
            ? "bg-primary text-primary-foreground rounded-t-lg rounded-l-lg" 
            : "bg-secondary text-secondary-foreground rounded-t-lg rounded-r-lg"
        )}
      >
        <p className="text-sm">{formatMessage(message)}</p>
        <div className={cn(
          "text-[10px] mt-1 opacity-70 text-right",
          isUser ? "text-primary-foreground/70" : "text-secondary-foreground/70"
        )}>
          {new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
        </div>
      </div>
    </div>
  );
};

export default ChatMessage;