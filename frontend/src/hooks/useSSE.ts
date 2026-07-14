import { useState, useCallback, useRef } from 'react';

export interface SSEMessage {
  role: 'user' | 'ai';
  content: string;
  sources?: any[];
  isStreaming?: boolean;
}

export function useSSE(urlFn: (question: string) => string) {
  const [messages, setMessages] = useState<SSEMessage[]>([]);
  const [isStreaming, setIsStreaming] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  const abortControllerRef = useRef<AbortController | null>(null);

  const startStream = useCallback(async (question: string) => {
    // Add user message
    setMessages(prev => [...prev, { role: 'user', content: question }]);
    // Add empty AI message to stream into
    setMessages(prev => [...prev, { role: 'ai', content: '', isStreaming: true }]);
    
    setIsStreaming(true);
    setError(null);

    abortControllerRef.current = new AbortController();

    try {
      const response = await fetch(urlFn(question), {
        signal: abortControllerRef.current.signal,
      });

      if (!response.ok || !response.body) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let done = false;
      let buffer = '';

      while (!done) {
        const { value, done: readerDone } = await reader.read();
        done = readerDone;
        if (value) {
          buffer += decoder.decode(value, { stream: true });
          
          let parts = buffer.split('\n\n');
          buffer = parts.pop() || '';

          for (const part of parts) {
            if (part.startsWith('data: ')) {
              const dataStr = part.slice(6);
              try {
                const data = JSON.parse(dataStr);
                
                if (data.type === 'token') {
                  setMessages(prev => {
                    const newMessages = [...prev];
                    const lastMsg = { ...newMessages[newMessages.length - 1] };
                    if (lastMsg.role === 'ai') {
                      lastMsg.content += data.token;
                      newMessages[newMessages.length - 1] = lastMsg;
                    }
                    return newMessages;
                  });
                } else if (data.type === 'done') {
                  setMessages(prev => {
                    const newMessages = [...prev];
                    const lastMsg = { ...newMessages[newMessages.length - 1] };
                    if (lastMsg.role === 'ai') {
                      lastMsg.isStreaming = false;
                      lastMsg.sources = data.sources;
                      newMessages[newMessages.length - 1] = lastMsg;
                    }
                    return newMessages;
                  });
                  setIsStreaming(false);
                }
              } catch (e) {
                console.error("Error parsing SSE data", e, dataStr);
              }
            }
          }
        }
      }
    } catch (err: any) {
      if (err.name !== 'AbortError') {
        console.error("Fetch error", err);
        setError(err);
        setMessages(prev => {
           const newMessages = [...prev];
           const lastMsg = { ...newMessages[newMessages.length - 1] };
           if (lastMsg.role === 'ai') {
               lastMsg.isStreaming = false;
               newMessages[newMessages.length - 1] = lastMsg;
           }
           return newMessages;
        });
        setIsStreaming(false);
      }
    }
  }, [urlFn]);

  const stopStream = useCallback(() => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      abortControllerRef.current = null;
      setIsStreaming(false);
      setMessages(prev => {
        const newMessages = [...prev];
        const lastMsg = { ...newMessages[newMessages.length - 1] };
        if (lastMsg && lastMsg.role === 'ai') {
            lastMsg.isStreaming = false;
            newMessages[newMessages.length - 1] = lastMsg;
        }
        return newMessages;
      });
    }
  }, []);

  return { messages, isStreaming, error, startStream, stopStream };
}
