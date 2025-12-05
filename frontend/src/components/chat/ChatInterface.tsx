import React, { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { apiClient } from '../../services/api';
import { WorkflowRequest, WorkflowStatus, TaskStatus, WorkflowStage } from '../../types/api';

const ChatInterface: React.FC = () => {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<Array<{ role: 'user' | 'assistant'; content: string }>>([
    { role: 'assistant', content: 'Welcome to SPARTA! Describe your hardware design and I\'ll help you create it.' }
  ]);
  const [currentWorkflow, setCurrentWorkflow] = useState<WorkflowStatus | null>(null);

  const createWorkflowMutation = useMutation({
    mutationFn: (request: WorkflowRequest) => apiClient.createWorkflow(request),
    onSuccess: (data) => {
      setCurrentWorkflow(data);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: `Workflow started! ID: ${data.workflow_id}\nStatus: ${data.status}\nCurrent stage: ${data.current_stage}`
      }]);
    },
    onError: (error: any) => {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: `Error: ${error.message}`
      }]);
    }
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    // Add user message
    setMessages(prev => [...prev, { role: 'user', content: input }]);

    // Create workflow
    createWorkflowMutation.mutate({
      user_input: input,
      stages: [],
      parameters: {},
      metadata: {}
    });

    setInput('');
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-gray-800 rounded-lg shadow-xl p-6 mb-4">
        <h2 className="text-xl font-semibold mb-4 text-blue-300">Hardware Design Chat</h2>
        
        <div className="space-y-4 mb-4 h-96 overflow-y-auto">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                  msg.role === 'user'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-700 text-gray-100'
                }`}
              >
                <p className="whitespace-pre-wrap">{msg.content}</p>
              </div>
            </div>
          ))}
        </div>

        <form onSubmit={handleSubmit} className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Describe your hardware design..."
            className="flex-1 px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={createWorkflowMutation.isPending}
          />
          <button
            type="submit"
            disabled={createWorkflowMutation.isPending}
            className="px-6 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 rounded-lg font-semibold transition-colors"
          >
            {createWorkflowMutation.isPending ? 'Processing...' : 'Send'}
          </button>
        </form>
      </div>

      {currentWorkflow && (
        <div className="bg-gray-800 rounded-lg shadow-xl p-6">
          <h3 className="text-lg font-semibold mb-3 text-blue-300">Workflow Status</h3>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span className="text-gray-400">Workflow ID:</span>
              <span className="font-mono">{currentWorkflow.workflow_id}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Status:</span>
              <span className={`font-semibold ${
                currentWorkflow.status === TaskStatus.COMPLETED ? 'text-green-400' :
                currentWorkflow.status === TaskStatus.FAILED ? 'text-red-400' :
                'text-yellow-400'
              }`}>
                {currentWorkflow.status}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Current Stage:</span>
              <span>{currentWorkflow.current_stage}</span>
            </div>
            <div className="mt-2">
              <div className="flex justify-between text-xs mb-1">
                <span className="text-gray-400">Progress</span>
                <span>{currentWorkflow.progress_percentage.toFixed(0)}%</span>
              </div>
              <div className="w-full bg-gray-700 rounded-full h-2">
                <div
                  className="bg-blue-500 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${currentWorkflow.progress_percentage}%` }}
                />
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatInterface;
