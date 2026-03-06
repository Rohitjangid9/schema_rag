import ChatInterface from "@/components/chat/ChatInterface";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-4 md:p-8 relative bg-black isolate">
      {/* Background gradients for premium aesthetic */}
      <div className="absolute inset-0 -z-10 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-zinc-900 via-zinc-950 to-black"></div>
      <div className="absolute top-0 left-1/2 w-full -translate-x-1/2 h-[500px] opacity-20 pointer-events-none">
        <div className="absolute inset-0 bg-gradient-to-r from-emerald-500/20 via-blue-500/20 to-purple-500/20 blur-[100px] -z-10 rounded-full"></div>
      </div>
      
      <div className="w-full h-[85vh] max-h-[900px]">
        <ChatInterface />
      </div>
    </main>
  );
}
