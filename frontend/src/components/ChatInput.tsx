import React, { useState } from 'react';
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { Separator } from "@/components/ui/separator";
import { SendIcon, Loader2 } from "lucide-react";

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  isLoading: boolean;
}

const ChatInput: React.FC<ChatInputProps> = ({ onSendMessage, isLoading }) => {
  const [message, setMessage] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim() && !isLoading) {
      onSendMessage(message);
      setMessage('');
    }
  };

  return (
    <div className="border-t bg-background p-3">
      <Separator className="mb-3" />
      <form onSubmit={handleSubmit} className="flex items-center gap-2">
        <Input
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Schreibe deine Nachricht..."
          disabled={isLoading}
          className={cn(
            "flex-grow border-muted text-sm rounded-full py-5 px-4 shadow-sm",
            "focus-visible:ring-primary focus-visible:ring-offset-0"
          )}
        />
        <Button 
          type="submit" 
          size="icon"
          disabled={isLoading || !message.trim()} 
          className="rounded-full h-10 w-10 flex-shrink-0 shadow-md"
        >
          {isLoading ? (
            <Loader2 className="h-5 w-5 animate-spin" />
          ) : (
            <SendIcon className="h-5 w-5" />
          )}
        </Button>
      </form>
    </div>
  );
};

export default ChatInput;