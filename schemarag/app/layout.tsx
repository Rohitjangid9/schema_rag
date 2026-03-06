import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Schema RAG Chat",
  description: "A premium AI Chatbot interface for Database Schema queries.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className="antialiased bg-zinc-950 text-zinc-50 min-h-screen flex flex-col font-sans">
        {children}
      </body>
    </html>
  );
}
