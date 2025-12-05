import React, { useState } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import ChatInterface from './components/chat/ChatInterface';
import './App.css';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <div className="App min-h-screen bg-gray-900 text-white">
        <header className="bg-gray-800 p-4 shadow-lg">
          <div className="container mx-auto">
            <h1 className="text-3xl font-bold text-blue-400">
              SPARTA
            </h1>
            <p className="text-sm text-gray-400">
              Superhuman PRAgmatic Technology Accelerator
            </p>
          </div>
        </header>
        
        <main className="container mx-auto p-4">
          <ChatInterface />
        </main>
        
        <footer className="bg-gray-800 p-4 mt-8">
          <div className="container mx-auto text-center text-gray-400 text-sm">
            <p>&copy; 2025 SPARTA Platform v0.1.0</p>
          </div>
        </footer>
      </div>
    </QueryClientProvider>
  );
}

export default App;
