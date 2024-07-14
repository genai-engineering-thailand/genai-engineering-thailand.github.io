"use client";

import { useState, useRef, useEffect } from 'react';
import { v4 as uuidv4 } from 'uuid';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faThumbsDown } from '@fortawesome/free-solid-svg-icons';
import ReactMarkdown from 'react-markdown';
import { LangfuseWeb } from "langfuse";

import Modal from '../components/modal';

export default function Home() {
  const langfuseWeb = new LangfuseWeb({
    publicKey: process.env.NEXT_PUBLIC_LANGFUSE_PUBLIC_KEY,
    baseUrl: process.env.NEXT_PUBLIC_LANGFUSE_URL,
  });

  const [messages, setMessages] = useState<{ sender: string; text: string; id: number; traceId?: string }[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [feedback, setFeedback] = useState<{ messageId?: number; text: string; traceId?: string } | null>(null);
  const [username] = useState('User' + Math.floor(Math.random() * 1000));
  const [sessionId] = useState(uuidv4());
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const handleSendMessage = async () => {
    if (input.trim() === '') return;

    setLoading(true);

    const messageId = Date.now();
    const userMessage = { sender: username, text: input, id: messageId };
    setMessages([...messages, userMessage]);

    // Prepare request payload
    const payload = {
      name: username,
      session_id: sessionId,
      message_id: messageId.toString(),
      message: input
    };

    try {
      // Send the message to the API
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_CHAT}/chat/message`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      });

      const data = await response.json();

      if (data.success) {
        const botMessage = { sender: 'bot', text: data.data.answer, id: Date.now() + 1, traceId: data.data.trace_id };
        setMessages(prevMessages => [...prevMessages, botMessage]);
      } else {
        console.error('Failed to get a response from the bot');
      }
    } catch (error) {
      console.error('Error sending message:', error);
    }

    setInput('');
    setLoading(false);
  };

  const handleKeyPress = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === 'Enter') {
      handleSendMessage();
    }
  };

  const handleDislike = (messageId: number, traceId?: string) => {
    setFeedback({ messageId, text: '', traceId });
  };

  const handleFeedbackChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setFeedback({ ...feedback, text: event.target.value });
  };

  const handleFeedbackSubmit = async () => {
    if (feedback && feedback.text.trim() !== '') {
      await langfuseWeb.score({
        traceId: feedback.traceId || '',
        name: 'feedback',
        value: 0,
        comment: feedback.text
      });
      console.log(`Feedback for message ${feedback.messageId} from ${username} (session ${sessionId}): ${feedback.text}`);
      setFeedback(null);
    }
  };

  const closeModal = () => {
    setFeedback(null);
  };

  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  return (
    <div className="p-5 max-w-lg mx-auto h-screen flex flex-col bg-black text-white">
      <h1 className="text-2xl font-bold mb-2">Master Chef Bot</h1>
      <p className="mb-4"><strong>Username:</strong> {username}</p>
      <p className="mb-4"><strong>Session ID:</strong> {sessionId}</p>
      <div className="flex-grow border border-gray-300 p-4 overflow-y-scroll mb-4 bg-white text-black rounded">
        {messages.map((msg, index) => (
          <div key={index} className={`mb-2 ${msg.sender === username ? 'text-right' : 'text-left'}`}>
            <div className={`inline-block p-2 rounded-md ${msg.sender === username ? 'bg-blue-500 text-white' : 'bg-gray-200 text-black'}`}>
              <p className="text-xs text-black"><strong>ID:</strong> {msg.id}</p>
              <p className="text-xs text-black"><strong>Trace ID:</strong> {msg.traceId}</p>
              {msg.sender === 'bot' ? (
                <ReactMarkdown>{msg.text}</ReactMarkdown>
              ) : (
                <p>{msg.text}</p>
              )}
            </div>
            {msg.sender === 'bot' && (
              <div className="flex justify-start mt-1">
                <button
                  onClick={() => handleDislike(msg.id, msg.traceId)}
                  className="text-red-500"
                >
                  <FontAwesomeIcon icon={faThumbsDown} />
                </button>
              </div>
            )}
          </div>
        ))}
        <div ref={messagesEndRef}></div>
      </div>
      <div className="flex">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyPress}
          className="flex-grow border border-gray-300 p-2 rounded-md mr-2 text-black"
          disabled={loading}
        />
        <button onClick={handleSendMessage} className="bg-blue-500 text-white p-2 rounded-md" disabled={loading}>
          {loading ? 'Sending...' : 'Send'}
        </button>
      </div>

      <Modal isOpen={!!feedback} onClose={closeModal}>
        {feedback && (
          <>
            <h2 className="text-xl font-bold mb-2">Provide Feedback</h2>
            <input
              type="text"
              value={feedback.text}
              onChange={handleFeedbackChange}
              placeholder="Provide your feedback here"
              className="w-full border border-gray-300 p-2 rounded-md mb-2 text-black"
            />
            <button onClick={handleFeedbackSubmit} className="bg-blue-500 text-white p-2 rounded-md">
              Submit Feedback
            </button>
          </>
        )}
      </Modal>
    </div>
  );
}