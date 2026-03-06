"use client";

import React, { useState, useRef, useEffect } from "react";
import { SendHorizonal, Trash2 } from "lucide-react";
import { ChatMessage, MessageProps } from "./ChatMessage";
import { Input } from "@/components/ui/Input";
import { Button } from "@/components/ui/Button";

export default function ChatInterface() {
  const [messages, setMessages] = useState<MessageProps[]>([
    {
      id: "welcome",
      role: "bot",
      content: "Hello! I am Schema RAG. Ask me anything about your database schema, tables, or perform natural language queries over your data.",
    },
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMsg: MessageProps = { id: Date.now().toString(), role: "user", content: input };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setIsLoading(true);

    try {
      const response = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: userMsg.content }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Failed to fetch response");
      }

      // Check for errors returned in JSON structure
      if (data.status === "error" || data.status === "sql_validation_failed" || data.status === "execution_failed") {
          throw new Error(data.error || data.status);
      }

      let botResponseText = data.answer || "Query executed successfully, but no direct textual answer was provided.";
      
      // If we got tables used and SQL query, maybe format it nicely.
      if (data.tables_used && data.tables_used.length > 0) {
        botResponseText += `\n\n<span class="text-xs text-zinc-500">Sources: ${data.tables_used.join(', ')}</span>`;
      }

      setMessages((prev) => [
        ...prev,
        { id: Date.now().toString(), role: "bot", content: botResponseText },
      ]);
    } catch (err: any) {
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now().toString(),
          role: "bot",
          content: `⚠️ Error processing query: ${err.message}`,
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const clearChat = () => {
    setMessages([
      {
        id: "welcome",
        role: "bot",
        content: "Hello! I am Schema RAG. Ask me anything about your database schema.",
      },
    ]);
  };

  return (
    <div className="flex flex-col h-full w-full max-w-4xl mx-auto overflow-hidden rounded-[2rem] border border-white/10 bg-black/40 shadow-2xl relative glass-panel">
      {/* Header */}
      <div className="flex items-center justify-between px-6 py-4 border-b border-white/10 bg-zinc-950/50 backdrop-blur-md z-10 relative">
        <div className="flex items-center space-x-3">
          <div className="h-3 w-3 rounded-full bg-emerald-500 animate-pulse" />
          <h2 className="font-semibold text-lg text-zinc-100 tracking-tight">Schema RAG Agent</h2>
        </div>
        <Button onClick={clearChat} className="bg-transparent hover:bg-zinc-800 text-zinc-400 border-none shadow-none h-8 w-8 p-0 rounded-md">
          <Trash2 size={16} />
        </Button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-6 space-y-2 relative z-0">
        {messages.map((msg) => (
          <ChatMessage key={msg.id} {...msg} />
        ))}
        {isLoading && (
          <ChatMessage id="loading" role="bot" content="" isLoading={true} />
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input Area */}
      <div className="p-4 bg-zinc-950/50 backdrop-blur-md border-t border-white/10 relative z-10 w-full">
        <form onSubmit={handleSubmit} className="flex space-x-3 max-w-3xl mx-auto items-center">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about your database..."
            className="flex-1 rounded-full px-5 bg-zinc-900 border-zinc-800 focus:ring-zinc-700 text-zinc-100 placeholder:text-zinc-500/80 shadow-inner"
            disabled={isLoading}
          />
          <Button type="submit" disabled={!input.trim() || isLoading} className="rounded-full h-10 w-10 p-0 shadow-lg">
            <SendHorizonal size={18} />
          </Button>
        </form>
      </div>
    </div>
  );
}
