import React from 'react';
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Separator } from "@/components/ui/separator";

const Header: React.FC = () => {
  return (
    <header className="bg-primary text-primary-foreground p-3 shadow-md">
      <div className="flex items-center gap-3">
        <Avatar className="h-10 w-10">
          <AvatarImage src="/logo.png" alt="Smart Travel Planner" />
          <AvatarFallback className="bg-primary-foreground text-primary font-semibold">STP</AvatarFallback>
        </Avatar>
        <div className="flex flex-col">
          <h1 className="text-lg font-bold">Smart Travel Planner</h1>
          <p className="text-xs opacity-80">Universität Graz</p>
        </div>
      </div>
      <Separator className="mt-3 bg-primary-foreground/20" />
    </header>
  );
};

export default Header;