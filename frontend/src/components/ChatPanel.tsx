"use client";

import { useEffect, useRef, useState } from "react";
import { useI18n } from "@/lib/i18n";
import { useSSE } from "@/hooks/useSSE";
import { getStreamUrl } from "@/lib/api";
import { Send, StopCircle, Bot } from "lucide-react";
import { Button } from "./ui/button";
import { Textarea } from "./ui/textarea";
import { ScrollArea } from "./ui/scroll-area";
import ReactMarkdown from "react-markdown";

export function ChatPanel({ docId }: { docId: string }) {
  const { t } = useI18n();
  const [input, setInput] = useState("");
  const { messages, isStreaming, startStream, stopStream } = useSSE((q) => getStreamUrl(docId, q));
  const bottomRef = useRef<HTMLDivElement>(null);

  // Auto scroll
  useEffect(() => {
    bottomRef.current?.scrollIntoView(); // Removed smooth scrolling to fix jumpy behavior during streaming
  }, [messages]);

  const handleSend = () => {
    if (!input.trim() || isStreaming) return;
    startStream(input);
    setInput("");
  };

  const onKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex flex-col h-full bg-card border-r border-border">
      <div className="px-6 py-4 border-b border-border bg-muted/30">
        <h2 className="font-semibold flex items-center gap-2">
          <Bot className="w-5 h-5 text-primary" /> Document Chat
        </h2>
      </div>

      <ScrollArea className="flex-1 p-6">
        <div className="space-y-6">
          {messages.length === 0 && (
             <div className="text-center text-muted-foreground mt-10">
               <p>Ask a question about the document.</p>
               <div className="flex flex-wrap gap-2 justify-center mt-6">
                 {["What is the invoice total?", "Summarize this document", "Extract all parties"].map(chip => (
                   <Button key={chip} variant="outline" size="sm" onClick={() => startStream(chip)} className="rounded-full">
                     {chip}
                   </Button>
                 ))}
               </div>
             </div>
          )}
          
          {messages.map((msg, i) => (
            <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div 
                className={`max-w-[85%] rounded-2xl px-5 py-3 ${
                  msg.role === 'user' 
                    ? 'bg-primary text-primary-foreground rounded-tr-sm' 
                    : 'bg-muted border border-border rounded-tl-sm'
                }`}
              >
                <div className={`prose prose-sm dark:prose-invert max-w-none break-words overflow-x-auto ${msg.role === 'user' ? 'text-primary-foreground' : ''}`}>
                  <ReactMarkdown>{msg.content}</ReactMarkdown>
                </div>
                
                {msg.isStreaming && (
                  <span className="inline-block w-1.5 h-4 bg-primary animate-pulse ml-1 align-middle"></span>
                )}
                
                {msg.sources && msg.sources.length > 0 && (
                  <div className="mt-3 pt-3 border-t border-border/50 flex flex-wrap gap-2">
                    {msg.sources.map((src, idx) => (
                      <span key={idx} className="text-xs bg-background/50 px-2 py-1 rounded text-muted-foreground border border-border/50 cursor-pointer hover:bg-background" title={src.text_snippet}>
                        [Page {src.page}]
                      </span>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}
          <div ref={bottomRef} />
        </div>
      </ScrollArea>

      <div className="p-4 bg-background border-t border-border">
        <div className="relative">
          <Textarea 
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={onKeyDown}
            placeholder={t("chat_placeholder")}
            className="min-h-12 resize-none pr-12 rounded-xl bg-card border-muted focus-visible:ring-primary/50"
            rows={1}
          />
          <div className="absolute right-2 bottom-2">
            {isStreaming ? (
              <Button size="icon" variant="ghost" onClick={stopStream} className="h-8 w-8 text-destructive hover:text-destructive hover:bg-destructive/10">
                <StopCircle className="w-5 h-5" />
              </Button>
            ) : (
              <Button size="icon" onClick={handleSend} disabled={!input.trim()} className="h-8 w-8 rounded-lg bg-primary hover:bg-primary/90">
                <Send className="w-4 h-4" />
              </Button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
