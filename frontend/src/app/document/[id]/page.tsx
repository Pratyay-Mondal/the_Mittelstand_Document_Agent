import { ChatPanel } from "@/components/ChatPanel";
import { ExtractionPanel } from "@/components/ExtractionPanel";
import { Navbar } from "@/components/Navbar";

export default async function DocumentWorkspace({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;

  return (
    <div className="h-screen w-full flex flex-col overflow-hidden bg-background">
      <Navbar />
      
      <main className="flex-1 min-h-0 flex flex-col md:flex-row overflow-hidden relative">
        {/* Left Side: Chat Interface */}
        <div className="w-full md:w-[60%] min-w-0 flex flex-col h-[50vh] md:h-full z-10 shadow-xl border-b md:border-b-0 border-border min-h-0">
           <ChatPanel docId={id} />
        </div>
        
        {/* Right Side: Structured Extraction HITL */}
        <div className="w-full md:w-[40%] min-w-0 flex flex-col h-[50vh] md:h-full md:border-l border-border bg-muted/10 relative min-h-0">
           <div className="hidden md:block absolute inset-y-0 left-0 w-px bg-gradient-to-b from-transparent via-border to-transparent"></div>
           <ExtractionPanel docId={id} />
        </div>
      </main>
    </div>
  )
}
