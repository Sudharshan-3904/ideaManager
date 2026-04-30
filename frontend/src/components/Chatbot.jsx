import React, { useState, useEffect, useRef } from 'react';
import { Send, X, MessageSquare, Sparkles, Loader2, User, Bot, Plus, HelpCircle } from 'lucide-react';
import * as api from '../api';

const Chatbot = ({ idea, onClose, onUpdate }) => {
    const isGeneral = !idea;
    const [messages, setMessages] = useState([
        { 
            role: 'assistant', 
            content: isGeneral 
                ? "Hello! I'm your global startup assistant. I can help you brainstorm new ideas or review your current portfolio. What's on your mind?" 
                : `Hello! I'm your startup consultant. How can I help you refine "${idea.title}" today?` 
        }
    ]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [activeQuestions, setActiveQuestions] = useState([]);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    // Extract questions from the latest message whenever messages update
    useEffect(() => {
        const lastMessage = messages[messages.length - 1];
        if (lastMessage && lastMessage.role === 'assistant') {
            const questionRegex = /<questions>(.*?)<\/questions>/s;
            const match = lastMessage.content.match(questionRegex);
            if (match) {
                try {
                    const questions = JSON.parse(match[1]);
                    setActiveQuestions(questions);
                } catch (e) {
                    console.error("Failed to parse questions:", e);
                    setActiveQuestions([]);
                }
            } else {
                setActiveQuestions([]);
            }
        }
    }, [messages]);

    const handleSend = async (e) => {
        if (e) e.preventDefault();
        if (!input.trim() || isLoading) return;

        const userMessage = { role: 'user', content: input };
        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setActiveQuestions([]); // Clear questions once answered
        setIsLoading(true);

        try {
            const response = isGeneral 
                ? await api.generalChat([...messages, userMessage])
                : await api.chatWithIdea(idea.title, [...messages, userMessage]);
            
            setMessages(prev => [...prev, { role: 'assistant', content: response.response }]);
            
            if (response.didUpdate && onUpdate) {
                onUpdate();
            }
        } catch (error) {
            setMessages(prev => [...prev, { role: 'assistant', content: 'Sorry, I encountered an error connecting to my neural network.' }]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleQuestionClick = (q) => {
        setInput(q);
        // We don't auto-send so the user can refine if needed, 
        // but often in these UIs it's nice if it feels like a selection.
    };

    const renderMessageContent = (content) => {
        const questionRegex = /<questions>(.*?)<\/questions>/s;
        const textPart = content.replace(questionRegex, '').trim();
        return <p className="whitespace-pre-wrap">{textPart}</p>;
    };

    return (
        <div className="flex flex-col h-full bg-[#0d1117] border-l border-white/10 shadow-2xl animate-in slide-in-from-right duration-500 overflow-hidden relative">
            <div className="p-6 border-b border-white/5 bg-gradient-to-r from-blue-600/10 to-purple-600/10 flex items-center justify-between">
                <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-xl bg-blue-500/20 flex items-center justify-center border border-blue-500/30">
                        <Sparkles className="w-5 h-5 text-blue-400" />
                    </div>
                    <div>
                        <h3 className="font-bold text-white tracking-tight">{isGeneral ? 'Global Assistant' : 'Idea Consultant'}</h3>
                        <p className="text-[10px] text-blue-400 font-bold uppercase tracking-widest">{isGeneral ? 'Portfolio Mode' : 'Refinement Mode'}</p>
                    </div>
                </div>
                <button onClick={onClose} className="p-2 hover:bg-white/5 rounded-full transition-colors text-slate-500">
                    <X size={20} />
                </button>
            </div>

            <div className="flex-1 overflow-y-auto p-6 space-y-6 custom-scrollbar">
                {messages.map((m, i) => (
                    <div key={i} className={`flex gap-4 ${m.role === 'user' ? 'flex-row-reverse' : ''} animate-in fade-in slide-in-from-bottom-2 duration-300`}>
                        <div className={`w-8 h-8 rounded-lg shrink-0 flex items-center justify-center border ${
                            m.role === 'user' 
                            ? 'bg-purple-500/20 border-purple-500/30 text-purple-400' 
                            : 'bg-blue-500/20 border-blue-500/30 text-blue-400'
                        }`}>
                            {m.role === 'user' ? <User size={16} /> : <Bot size={16} />}
                        </div>
                        <div className={`max-w-[80%] p-4 rounded-2xl text-sm leading-relaxed ${
                            m.role === 'user' 
                            ? 'bg-purple-600/10 border border-purple-500/20 text-slate-200 rounded-tr-none' 
                            : 'bg-white/5 border border-white/5 text-slate-300 rounded-tl-none'
                        }`}>
                            {renderMessageContent(m.content)}
                        </div>
                    </div>
                ))}
                {isLoading && (
                    <div className="flex gap-4 animate-pulse">
                        <div className="w-8 h-8 rounded-lg bg-blue-500/20 border border-blue-500/30 flex items-center justify-center">
                            <Loader2 size={16} className="text-blue-400 animate-spin" />
                        </div>
                        <div className="p-4 rounded-2xl bg-white/5 border border-white/5 text-slate-500 text-xs italic">
                            Visionary is thinking...
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            {/* Questions Extension */}
            {activeQuestions.length > 0 && (
                <div className="px-6 py-4 bg-[#0a0d12] border-t border-white/5 animate-in slide-in-from-bottom-4 duration-300">
                    <div className="flex items-center gap-2 mb-3 text-[10px] font-bold uppercase tracking-widest text-blue-400/60">
                        <HelpCircle size={12} /> Clarification Requests
                    </div>
                    <div className="flex flex-wrap gap-2">
                        {activeQuestions.map((q, idx) => (
                            <button 
                                key={idx}
                                onClick={() => handleQuestionClick(q)}
                                className="px-4 py-2 rounded-xl bg-blue-600/5 border border-blue-500/20 text-blue-300 text-[11px] hover:bg-blue-600/10 hover:border-blue-500/40 transition-all flex items-center gap-2 group whitespace-nowrap"
                            >
                                {q}
                                <Plus size={12} className="opacity-40 group-hover:opacity-100" />
                            </button>
                        ))}
                    </div>
                </div>
            )}

            <form onSubmit={handleSend} className="p-6 border-t border-white/5 bg-[#0d1117]">
                <div className="relative">
                    <input 
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Type your response or select a question above..."
                        className="w-full bg-white/5 border border-white/10 rounded-2xl py-4 pl-6 pr-14 text-sm text-white focus:outline-none focus:border-blue-500/50 transition-all"
                    />
                    <button 
                        type="submit"
                        disabled={!input.trim() || isLoading}
                        className={`absolute right-2 top-1/2 -translate-y-1/2 p-2.5 rounded-xl transition-all ${
                            input.trim() && !isLoading 
                            ? 'bg-blue-600 text-white shadow-lg shadow-blue-600/20 hover:scale-105 active:scale-95' 
                            : 'text-slate-600'
                        }`}
                    >
                        <Send size={18} />
                    </button>
                </div>
            </form>
        </div>
    );
};

export default Chatbot;
