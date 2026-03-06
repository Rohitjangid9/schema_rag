import React from "react";
import { motion } from "framer-motion";
import { Bot, User } from "lucide-react";
import { cn } from "@/lib/utils";

export type MessageRole = "user" | "bot";

export interface MessageProps {
  id: string;
  role: MessageRole;
  content: string;
  isLoading?: boolean;
}

export const ChatMessage = ({ role, content, isLoading }: MessageProps) => {
  const isUser = role === "user";

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, scale: 0.95 }}
      transition={{ duration: 0.2 }}
      className={cn("flex w-full space-x-4 py-4", isUser ? "justify-end" : "justify-start")}
    >
      {!isUser && (
        <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-zinc-800 text-zinc-50">
          <Bot size={16} />
        </div>
      )}

      <div
        className={cn(
          "max-w-[80%] rounded-2xl px-4 py-3 leading-relaxed",
          isUser
            ? "bg-zinc-50 text-zinc-950 rounded-tr-sm"
            : "glass-panel text-zinc-100 rounded-tl-sm shadow-sm"
        )}
      >
        {isLoading ? (
          <div className="flex space-x-1 items-center h-5">
            <motion.div animate={{ opacity: [0.4, 1, 0.4] }} transition={{ repeat: Infinity, duration: 1.5 }} className="h-1.5 w-1.5 bg-zinc-400 rounded-full" />
            <motion.div animate={{ opacity: [0.4, 1, 0.4] }} transition={{ repeat: Infinity, duration: 1.5, delay: 0.2 }} className="h-1.5 w-1.5 bg-zinc-400 rounded-full" />
            <motion.div animate={{ opacity: [0.4, 1, 0.4] }} transition={{ repeat: Infinity, duration: 1.5, delay: 0.4 }} className="h-1.5 w-1.5 bg-zinc-400 rounded-full" />
          </div>
        ) : (
          <div 
            className="whitespace-pre-wrap break-words format-tables"
            dangerouslySetInnerHTML={{ __html: formatContent(content) }}
          />
        )}
      </div>

      {isUser && (
        <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-zinc-700 text-zinc-50">
          <User size={16} />
        </div>
      )}
    </motion.div>
  );
};

// Simple formatter to handle newlines, bold text and very simple tables
function formatContent(text: string) {
  if (!text) return "";
  let formatted = text
    .replace(/\\n/g, "<br>")
    .replace(/\n/g, "<br>")
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
    
  return formatted;
}
