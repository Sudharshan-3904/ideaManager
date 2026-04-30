import React, { useState, useEffect } from 'react';
import { 
  Plus, Trash2, Edit3, Save, X, Lightbulb, Users, Target, Rocket, Activity,
  ChevronRight, MessageCircle, MoreVertical, Search, CheckCircle,
  StickyNote, AlertCircle, Zap, ArrowRight, List, Download, Upload, Filter, Tag as TagIcon,
  Archive, ArchiveRestore, LogOut, Loader2, Lock, LayoutDashboard, Library,
  Network, Share2, Sparkles
} from 'lucide-react';
import { Toaster, toast } from 'sonner';
import * as api from './api';
import ArchitectureDiagram from './components/ArchitectureDiagram';
import Chatbot from './components/Chatbot';
import ConfirmationModal from './components/ConfirmationModal';
import { useRef } from 'react';

/**
 * Main Application Component
 * 
 * Provides the core dashboard interface, authentication flows, and state management
 * for the Idea Manager frontend.
 */
const App = () => {
    const [isAuthenticated, setIsAuthenticated] = useState(!!localStorage.getItem('idea_manager_token'));
    const [isRegistering, setIsRegistering] = useState(false);
    const [loginData, setLoginData] = useState({ username: '', password: '' });
    const [isLoading, setIsLoading] = useState(false);
    const [ideas, setIdeas] = useState([]);
    const [selectedIdea, setSelectedIdea] = useState(null);
    const [isAdding, setIsAdding] = useState(false);
    const [isEditing, setIsEditing] = useState(false);
    const [searchQuery, setSearchQuery] = useState('');
    const [viewMode, setViewMode] = useState('ideas'); // 'ideas', 'docs', or 'architecture'
    const [tabMode, setTabMode] = useState('active'); // 'active' or 'archived'
    const [quickNote, setQuickNote] = useState('');
    const [quickHurdle, setQuickHurdle] = useState({ title: '', desc: '' });
    const [isQuickAddingNote, setIsQuickAddingNote] = useState(false);
    const [isQuickAddingHurdle, setIsQuickAddingHurdle] = useState(false);
    const [sortBy, setSortBy] = useState('title'); // 'title' or 'hurdles'
    const [tagFilter, setTagFilter] = useState('all');
    const [isGlobalChatOpen, setIsGlobalChatOpen] = useState(false);
    const [confirmModal, setConfirmModal] = useState({ isOpen: false, title: '', message: '', onConfirm: null });
    const fileInputRef = useRef(null);

    const [formData, setFormData] = useState({
        title: '',
        description: '',
        explanation: '',
        notes: [],
        hurdles: [],
        tags: [],
        status: 'Yet to Start'
    });

    // --- Initial Data Fetching ---
    useEffect(() => {
        if (isAuthenticated) {
            fetchIdeas();
        }
    }, [isAuthenticated]);

    // --- Authentication Handlers ---

    const handleLogin = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        try {
            await api.login(loginData.username, loginData.password);
            setIsAuthenticated(true);
            toast.success('Access granted, welcome back.');
        } catch (error) {
            toast.error(error.response?.data?.detail || 'Unauthorized entry.');
        } finally {
            setIsLoading(false);
        }
    };

    const handleRegister = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        try {
            await api.register(loginData.username, loginData.password);
            toast.success('Registration successful. You can now login.');
            setIsRegistering(false);
        } catch (error) {
            toast.error(error.response?.data?.detail || 'Registration failed.');
        } finally {
            setIsLoading(false);
        }
    };

    const handleLogout = () => {
        api.logout();
    };

    const fetchIdeas = async (shouldSelectUpdated = null) => {
        setIsLoading(true);
        try {
            const data = await api.getIdeas();
            setIdeas(data);
            
            const targetId = shouldSelectUpdated || selectedIdea?.id;
            if (targetId) {
                const updated = data.find(i => i.id === targetId);
                if (updated) setSelectedIdea(updated);
            } else if (data.length > 0 && !selectedIdea) {
                // Default to first active idea
                const firstActive = data.find(i => !i.is_archived);
                if (firstActive) setSelectedIdea(firstActive);
                else setSelectedIdea(data[0]);
            }
        } catch (error) {
            console.error('Failed to fetch ideas:', error);
            toast.error('Could not sync with the matrix.');
        } finally {
            setIsLoading(false);
        }
    };

    // --- Navigation & Selection ---
    const handleSelectIdea = (idea) => {
        setSelectedIdea(idea);
        setIsEditing(false);
        setIsAdding(false);
        setIsGlobalChatOpen(false);
    };

    // --- CRUD Operations ---

    const handleAddClick = () => {
        setIsAdding(true);
        setIsEditing(false);
        setSelectedIdea(null);
        setFormData({
            title: '',
            description: '',
            explanation: '',
            notes: [],
            hurdles: [],
            tags: [],
            status: 'Yet to Start'
        });
    };

    const handleEditClick = () => {
        setIsEditing(true);
        setIsAdding(false);
        setFormData({
            title: selectedIdea.title,
            description: selectedIdea.description,
            explanation: selectedIdea.explanation,
            notes: selectedIdea.notes || [],
            hurdles: selectedIdea.hurdles || [],
            tags: selectedIdea.tags || [],
            status: selectedIdea.status || 'Yet to Start'
        });
    };

    const handleSave = async (e) => {
        e.preventDefault();
        const promise = (async () => {
            const cleanData = {
                ...formData,
                notes: formData.notes.filter(n => n.trim() !== ''),
                hurdles: formData.hurdles
                    .filter(h => h.main_setback.trim() !== '')
                    .map(h => ({
                        ...h,
                        leads: h.leads.filter(l => l.trim() !== '')
                    }))
            };

            if (isAdding) {
                const response = await api.createIdea(cleanData);
                await fetchIdeas(response.id);
            } else if (isEditing) {
                await api.updateIdea(selectedIdea.id, cleanData);
                await fetchIdeas(selectedIdea.id);
            }
            setIsAdding(false);
            setIsEditing(false);
        })();

        toast.promise(promise, {
            loading: isAdding ? 'Launching concept...' : 'Refining concept...',
            success: 'Neural patterns synced.',
            error: (err) => err.response?.data?.detail || 'Sync failed.'
        });
    };

    const handleArchiveToggle = async () => {
        if (!selectedIdea) return;
        const newStatus = !selectedIdea.is_archived;
        
        toast.promise(api.archiveIdea(selectedIdea.id, newStatus), {
            loading: newStatus ? 'Archiving...' : 'Restoring...',
            success: () => {
                fetchIdeas();
                return newStatus ? 'Moved to archives.' : 'Restored to active status.';
            },
            error: 'Action failed.'
        });
    };

    const handleDelete = async (id) => {
        setConfirmModal({
            isOpen: true,
            title: 'Delete Concept?',
            message: `Are you sure you want to permanently purge this from the matrix? this action cannot be undone.`,
            onConfirm: () => {
                toast.promise(api.deleteIdea(id), {
                    loading: 'Deleting sequence...',
                    success: () => {
                        fetchIdeas();
                        setSelectedIdea(null);
                        setConfirmModal(prev => ({ ...prev, isOpen: false }));
                        return 'Idea purged.';
                    },
                    error: 'Purge failed.'
                });
            }
        });
    };

    const handleQuickSaveNote = async () => {
        if (!quickNote.trim()) return;
        try {
            const updatedIdea = { ...selectedIdea, notes: [...(selectedIdea.notes || []), quickNote] };
            await api.updateIdea(selectedIdea.id, updatedIdea);
            await fetchIdeas(selectedIdea.id);
            setQuickNote('');
            setIsQuickAddingNote(false);
            toast.success('Note stored.');
        } catch (error) {
            toast.error('Storage error.');
        }
    };

    const handleQuickSaveHurdle = async () => {
        if (!quickHurdle.title.trim()) return;
        try {
            const newHurdle = { 
                main_setback: quickHurdle.title, 
                description: quickHurdle.desc, 
                leads: [] 
            };
            const updatedIdea = { ...selectedIdea, hurdles: [...(selectedIdea.hurdles || []), newHurdle] };
            await api.updateIdea(selectedIdea.id, updatedIdea);
            await fetchIdeas(selectedIdea.id);
            setQuickHurdle({ title: '', desc: '' });
            setIsQuickAddingHurdle(false);
            toast.success('Hurdle recorded.');
        } catch (error) {
            toast.error('Sync failed.');
        }
    };

    const handleSaveArchitecture = async (newArchitecture) => {
        if (!selectedIdea) return;
        try {
            const updatedIdea = { ...selectedIdea, architecture: newArchitecture };
            await api.updateIdea(selectedIdea.id, updatedIdea);
            await fetchIdeas(selectedIdea.id);
            toast.success('Matrix architecture synced.');
        } catch (error) {
            toast.error('Matrix sync failed.');
        }
    };

    const handleImportClick = () => {
        fileInputRef.current?.click();
    };

    const handleImport = async (e) => {
        const file = e.target.files?.[0];
        if (!file) return;
        toast.promise(api.importIdeas(file), {
            loading: 'Importing ideas...',
            success: () => {
                fetchIdeas();
                return 'Ideas imported successfully.';
            },
            error: 'Import failed.'
        });
    };

    // --- Render Helpers ---
    const allTags = Array.from(new Set(ideas.flatMap(i => i.tags || [])));

    const filteredAndSortedIdeas = ideas
        .filter(i => {
            const title = i.title || '';
            const description = i.description || '';
            const matchesSearch = title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                description.toLowerCase().includes(searchQuery.toLowerCase());
            const matchesTag = tagFilter === 'all' || (i.tags && i.tags.includes(tagFilter));
            const matchesTab = tabMode === 'active' ? !i.is_archived : i.is_archived;
            return matchesSearch && matchesTag && matchesTab;
        })
        .sort((a, b) => {
            if (sortBy === 'title') return (a.title || '').localeCompare(b.title || '');
            if (sortBy === 'hurdles') return (b.hurdles?.length || 0) - (a.hurdles?.length || 0);
            return 0;
        });

    // --- Authentication View ---

    if (!isAuthenticated) {
        return (
            <div className="h-screen w-full bg-[#0a0b1e] flex items-center justify-center p-6 bg-[radial-gradient(circle_at_50%_50%,#1e1b4b,0%,#0a0b1e_100%)]">
                <Toaster richColors position="top-center" theme="dark" />
                <div className="w-full max-w-md animate-in fade-in slide-in-from-bottom-8 duration-700">
                    <div className="glass p-12 rounded-[2rem] border border-white/5 shadow-2xl relative overflow-hidden group">
                        <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-blue-600 via-indigo-500 to-purple-600 opacity-50 group-hover:opacity-100 transition-opacity" />
                        
                        <div className="flex flex-col items-center gap-6 mb-10">
                            <div className="w-20 h-20 rounded-3xl bg-blue-600/10 flex items-center justify-center border border-blue-500/20 shadow-inner">
                                {isRegistering ? <Plus className="w-10 h-10 text-purple-400" /> : <Lock className="w-10 h-10 text-blue-400" />}
                            </div>
                            <div className="text-center">
                                <h1 className="text-3xl font-extrabold text-white tracking-tight mb-2">IdeaManager</h1>
                                <p className="text-slate-500 text-sm font-medium">
                                    {isRegistering ? 'Initialize new neural identity' : 'Neural credentials required for access'}
                                </p>
                            </div>
                        </div>

                        <form onSubmit={isRegistering ? handleRegister : handleLogin} className="space-y-6">
                            <div className="space-y-4">
                                <input 
                                    required
                                    type="text"
                                    placeholder="Neuro-ID (Username)"
                                    className="w-full bg-slate-900/50 border border-slate-700/50 rounded-2xl py-4 px-6 text-sm focus:outline-none focus:border-blue-500/50 focus:ring-4 ring-blue-500/5 transition-all text-white"
                                    value={loginData.username}
                                    onChange={(e) => setLoginData({...loginData, username: e.target.value})}
                                />
                                <input 
                                    required
                                    type="password"
                                    placeholder="Cipher Pattern (Password)"
                                    className="w-full bg-slate-900/50 border border-slate-700/50 rounded-2xl py-4 px-6 text-sm focus:outline-none focus:border-blue-500/50 focus:ring-4 ring-blue-500/5 transition-all text-white"
                                    value={loginData.password}
                                    onChange={(e) => setLoginData({...loginData, password: e.target.value})}
                                />
                            </div>
                            <button 
                                disabled={isLoading}
                                className="w-full primary py-4 rounded-2xl font-bold text-sm tracking-widest uppercase hover:scale-[1.02] active:scale-95 transition-all shadow-lg flex items-center justify-center gap-3"
                            >
                                {isLoading ? <Loader2 className="w-5 h-5 animate-spin" /> : (isRegistering ? 'Initialize Identity' : 'Authorize Access')}
                            </button>
                        </form>
                        
                        <div className="mt-8 text-center">
                            <button 
                                onClick={() => setIsRegistering(!isRegistering)}
                                className="text-slate-400 hover:text-blue-400 text-xs font-bold uppercase tracking-widest transition-colors"
                            >
                                {isRegistering ? 'Back to Authorization' : 'Request New Identity'}
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="flex h-screen w-full bg-[#0a0b1e] text-slate-200 font-sans overflow-hidden">
            <Toaster richColors position="bottom-right" theme="dark" />
            
            {/* Sidebar */}
            <div className="w-80 h-full glass border-r border-slate-700/50 flex flex-col m-3 rounded-2xl relative group">
                {isLoading && (
                    <div className="absolute inset-x-0 top-0 h-0.5 overflow-hidden">
                        <div className="w-full h-full bg-blue-500 animate-[loading_2s_infinite]" style={{ transformOrigin: '0% 50%' }}></div>
                    </div>
                )}
                
                <div className="p-6 border-b border-slate-700/50 flex flex-col gap-4">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2 text-xl font-bold">
                            <Lightbulb className="text-yellow-400 w-6 h-6" />
                            <span className="bg-gradient-to-r from-blue-400 to-indigo-400 bg-clip-text text-transparent">
                                IdeaManager
                            </span>
                        </div>
                        <div className="flex bg-slate-900/50 p-1 rounded-lg border border-slate-700/50 gap-1">
                            <button onClick={() => {setIsGlobalChatOpen(!isGlobalChatOpen); setSelectedIdea(null);}} title="Global AI Assistant" className={`p-1.5 rounded-md transition-colors ${isGlobalChatOpen ? 'bg-blue-600 text-white' : 'text-slate-500 hover:text-blue-400'}`}><Sparkles size={16} /></button>
                            <button onClick={handleLogout} title="Logout" className="p-1.5 rounded-md text-slate-500 hover:text-red-400 transition-colors"><LogOut size={16} /></button>
                        </div>
                    </div>

                    <div className="flex bg-slate-900/80 p-1 rounded-xl border border-slate-700/50">
                        <button 
                            onClick={() => setTabMode('active')} 
                            className={`flex-1 flex items-center justify-center gap-2 py-1.5 rounded-lg text-[10px] font-bold uppercase transition-all ${tabMode === 'active' ? 'bg-blue-600/20 text-blue-400' : 'text-slate-500 hover:text-slate-300'}`}
                        >
                            <Target size={12} /> Active
                        </button>
                        <button 
                            onClick={() => setTabMode('archived')} 
                            className={`flex-1 flex items-center justify-center gap-2 py-1.5 rounded-lg text-[10px] font-bold uppercase transition-all ${tabMode === 'archived' ? 'bg-orange-600/20 text-orange-400' : 'text-slate-500 hover:text-slate-300'}`}
                        >
                            <Archive size={12} /> Archived
                        </button>
                    </div>
                </div>

                <div className="px-4 py-2 border-b border-slate-700/30 flex gap-2">
                    <select 
                        value={tagFilter} 
                        onChange={(e) => setTagFilter(e.target.value)} 
                        className="bg-slate-900/50 border border-slate-700/50 rounded-lg py-1 px-2 text-[10px] uppercase font-bold text-slate-400 focus:outline-none flex-1"
                    >
                        <option value="all">Everywhere</option>
                        {allTags.map(tag => <option key={tag} value={tag}>{tag}</option>)}
                    </select>
                </div>

                <div className="p-4 flex flex-col gap-3 flex-1 overflow-y-auto custom-scrollbar">
                    <div className="relative">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
                        <input 
                            type="text" 
                            placeholder="Find an idea..." 
                            className="w-full bg-slate-900/50 border border-slate-700/50 rounded-xl py-2 pl-9 pr-4 text-sm focus:outline-none focus:border-blue-500/50 transition-all focus:ring-2 ring-blue-500/10"
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                        />
                    </div>

                    <div className="flex flex-col gap-1 mt-2">
                        {filteredAndSortedIdeas.length > 0 ? filteredAndSortedIdeas.map((idea) => (
                            <div 
                                key={idea.id}
                                onClick={() => handleSelectIdea(idea)}
                                className={`group flex items-center justify-between p-3 rounded-xl cursor-pointer transition-all duration-200 ${
                                    selectedIdea?.id === idea.id 
                                    ? 'bg-blue-600/20 border border-blue-500/30' 
                                    : 'hover:bg-slate-800/50 border border-transparent'
                                }`}
                            >
                                <div className="flex flex-col overflow-hidden">
                                    <div className="flex items-center gap-2">
                                        <span className={`font-medium truncate ${selectedIdea?.id === idea.id ? 'text-blue-300' : 'text-slate-300'}`}>
                                            {idea.title}
                                        </span>
                                        {idea.hurdles?.length > 0 && <span className="bg-orange-500/20 text-orange-400 text-[8px] px-1 rounded border border-orange-500/30 font-bold">{idea.hurdles.length}</span>}
                                        <span className={`text-[8px] px-1 rounded border font-mono uppercase ${
                                            idea.status === 'On Going' ? 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30' :
                                            idea.status === 'Paused' ? 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30' :
                                            idea.status === 'Stopped' ? 'bg-red-500/20 text-red-500 border-red-500/30' :
                                            idea.status === 'Planning' ? 'bg-blue-500/20 text-blue-400 border-blue-500/30' :
                                            'bg-slate-500/20 text-slate-400 border-slate-500/30'
                                        }`}>
                                            {idea.status || 'Yet to Start'}
                                        </span>
                                    </div>
                                    <div className="flex gap-1 mt-0.5 overflow-hidden">
                                        {(idea.tags || []).slice(0, 2).map((tag, idx) => (
                                            <span key={idx} className="text-[8px] text-slate-600 border border-slate-800 px-1 rounded uppercase tracking-tighter">{tag}</span>
                                        ))}
                                    </div>
                                </div>
                                <ChevronRight className={`w-4 h-4 transition-transform ${selectedIdea?.id === idea.id ? 'translate-x-0 opacity-100 text-blue-400' : '-translate-x-2 opacity-0'}`} />
                            </div>
                        )) : (
                            <div className="text-center py-10 opacity-50 text-sm italic flex flex-col items-center gap-2">
                                <Search className="w-8 h-8 opacity-20" />
                                No results found
                            </div>
                        )}
                    </div>
                </div>

                <div className="p-4 border-t border-slate-700/50">
                    <button 
                        onClick={handleAddClick}
                        className="w-full primary flex items-center justify-center gap-2 py-3 rounded-xl font-semibold transform hover:scale-[1.02] active:scale-95 transition-all shadow-xl"
                    >
                        <Plus size={20} />
                        New Concept
                    </button>
                    <div className="flex items-center justify-center gap-2 mt-4 px-2 opacity-50 hover:opacity-100 transition-opacity">
                        <input 
                            type="file" 
                            ref={fileInputRef} 
                            onChange={handleImport} 
                            className="hidden" 
                            accept=".json"
                        />
                        <button onClick={handleImportClick} className="text-[10px] uppercase font-bold text-slate-400 flex items-center gap-1.5 p-2 rounded-lg hover:bg-slate-800 flex-1 justify-center">
                            <Upload size={14} /> Import
                        </button>
                    </div>
                </div>
            </div>

            {/* Main Content */}
            <main className={`flex-1 h-full m-3 ml-0 rounded-2xl glass flex flex-col overflow-hidden relative border border-slate-700/50 ${viewMode === 'ideas' ? 'overflow-y-auto' : ''}`}>
                {isAdding || isEditing ? (
                  <div className="p-10 max-w-3xl mx-auto w-full animate-in fade-in slide-in-from-bottom-4 duration-500">
                      <div className="flex items-center justify-between mb-8">
                          <h2 className="text-2xl font-bold flex items-center gap-3">
                              {isAdding ? <Rocket className="text-blue-400" /> : <Edit3 className="text-indigo-400" />}
                              {isAdding ? 'Launch New Concept' : `Refining "${selectedIdea?.title}"`}
                          </h2>
                          <button onClick={() => {setIsAdding(false); setIsEditing(false);}} className="p-2 hover:bg-slate-800 rounded-full transition-colors">
                            <X className="w-5 h-5 text-slate-400" />
                          </button>
                      </div>

                      <form onSubmit={handleSave} className="space-y-6">
                          <div className="grid grid-cols-2 gap-6">
                              <div className="space-y-2">
                                  <label className="text-xs font-bold uppercase tracking-wider text-slate-500 ml-2">Title</label>
                                  <input 
                                    required
                                    value={formData.title}
                                    onChange={(e) => setFormData({...formData, title: e.target.value})}
                                    placeholder="What's the name of the idea?"
                                    className="w-full bg-slate-900 border border-slate-700/50 rounded-xl py-4 px-6 text-lg focus:outline-none focus:border-blue-500/50 transition-all font-medium text-white"
                                  />
                              </div>
                              <div className="space-y-2">
                                  <label className="text-xs font-bold uppercase tracking-wider text-slate-500 ml-2">Current Status</label>
                                  <select 
                                    value={formData.status}
                                    onChange={(e) => setFormData({...formData, status: e.target.value})}
                                    className="w-full bg-slate-900 border border-slate-700/50 rounded-xl py-4 px-6 text-sm focus:outline-none focus:border-blue-500/50 transition-all text-white h-[66px]"
                                  >
                                    <option value="Yet to Start">Yet to Start</option>
                                    <option value="Planning">Planning</option>
                                    <option value="On Going">On Going</option>
                                    <option value="Paused">Paused</option>
                                    <option value="Stopped">Stopped</option>
                                  </select>
                              </div>
                          </div>
                          
                          <div className="space-y-2">
                              <label className="text-xs font-bold uppercase tracking-wider text-slate-500 ml-2">Explanation (Detailed Elaboration)</label>
                              <textarea 
                                rows="8"
                                value={formData.explanation}
                                onChange={(e) => setFormData({...formData, explanation: e.target.value})}
                                placeholder="Elaborate on the idea in detail..."
                                className="w-full bg-slate-900/50 border border-slate-700/50 rounded-xl py-4 px-6 text-sm focus:outline-none focus:border-blue-500/50 resize-none"
                              />
                          </div>

                          <div className="space-y-2">
                              <label className="text-xs font-bold uppercase tracking-wider text-slate-500 ml-2">Description</label>
                              <textarea 
                                rows="4"
                                value={formData.description}
                                onChange={(e) => setFormData({...formData, description: e.target.value})}
                                placeholder="Paint the full picture..."
                                className="w-full bg-slate-900/50 border border-slate-700/50 rounded-xl py-4 px-6 text-sm focus:outline-none focus:border-blue-500/50 resize-none overflow-hidden"
                              />
                          </div>
                          
                          {/* ... rest of form matches existing detail with tags/notes ... */}
                          <div className="flex gap-4 pt-6">
                              <button type="submit" className="primary flex-1 flex items-center justify-center gap-2 py-4 rounded-xl text-lg font-bold shadow-xl">
                                  <Save className="w-5 h-5" />
                                  Commit Concept
                              </button>
                          </div>
                      </form>
                  </div>
                ) : selectedIdea ? (
                    <div className="p-0 h-full flex flex-col animate-in fade-in duration-700 relative">
                        {/* Detail Header */}
                        <div className="p-8 border-b border-slate-700/50 flex items-start justify-between bg-gradient-to-br from-indigo-900/10 to-transparent sticky top-0 bg-[#0a0b1e]/80 backdrop-blur-xl z-20">
                            <div className="flex-1">
                                <div className="flex items-center gap-2 text-blue-400 font-bold text-xs uppercase tracking-tighter mb-2">
                                    <CheckCircle className="w-3 h-3" />
                                    {selectedIdea.is_archived ? 'Archived Record' : 'Active System Data'}
                                </div>
                                <h1 className="text-4xl font-extrabold text-white tracking-tight">{selectedIdea.title}</h1>
                                <div className="flex gap-2 mt-2">
                                    <span className={`text-[10px] px-2 py-0.5 rounded-full border font-bold uppercase tracking-wider ${
                                        selectedIdea.status === 'On Going' ? 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30' :
                                        selectedIdea.status === 'Paused' ? 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30' :
                                        selectedIdea.status === 'Stopped' ? 'bg-red-500/20 text-red-500 border-red-500/30' :
                                        selectedIdea.status === 'Planning' ? 'bg-blue-500/20 text-blue-400 border-blue-500/30' :
                                        'bg-slate-500/20 text-slate-400 border-slate-500/30'
                                    }`}>
                                        {selectedIdea.status || 'Yet to Start'}
                                    </span>
                                </div>
                                {viewMode === 'ideas' && <p className="text-slate-400 mt-4 max-w-2xl leading-relaxed">{selectedIdea.description || 'No description provided yet.'}</p>}
                            </div>
                            <div className="flex gap-2">
                                <div className="flex bg-slate-900/50 p-1 rounded-xl border border-slate-700/50 mr-4">
                                    <button 
                                        onClick={() => setViewMode('ideas')} 
                                        title="Dashboard"
                                        className={`p-2.5 rounded-lg transition-all ${viewMode === 'ideas' ? 'bg-blue-600 shadow-lg text-white' : 'text-slate-500 hover:text-slate-300'}`}
                                    >
                                        <LayoutDashboard size={18} />
                                    </button>
                                    <button 
                                        onClick={() => setViewMode('docs')} 
                                        title="Docs & Inspiration"
                                        className={`p-2.5 rounded-lg transition-all ${viewMode === 'docs' ? 'bg-purple-600 shadow-lg text-white' : 'text-slate-500 hover:text-slate-300'}`}
                                    >
                                        <Library size={18} />
                                    </button>
                                    <button 
                                        onClick={() => setViewMode('architecture')} 
                                        title="Architecture"
                                        className={`p-2.5 rounded-lg transition-all ${viewMode === 'architecture' ? 'bg-indigo-600 shadow-lg text-white' : 'text-slate-500 hover:text-slate-300'}`}
                                    >
                                        <Network size={18} />
                                    </button>
                                </div>
                                <button onClick={handleArchiveToggle} title={selectedIdea.is_archived ? "Restore" : "Archive"} className={`p-3 rounded-xl transition-all border ${selectedIdea.is_archived ? 'bg-emerald-950/20 text-emerald-500 border-emerald-500/20' : 'bg-orange-950/20 text-orange-400 border-orange-500/20'}`}>
                                    {selectedIdea.is_archived ? <ArchiveRestore size={20} /> : <Archive size={20} />}
                                </button>
                                <button onClick={handleEditClick} className="p-3 bg-slate-800 hover:bg-slate-700 rounded-xl transition-all border border-slate-700/50 text-blue-300">
                                    <Edit3 size={20} />
                                </button>
                                <button onClick={() => handleDelete(selectedIdea.id)} className="p-3 bg-red-950/20 hover:bg-red-900/40 rounded-xl transition-all border border-red-500/20 text-red-500">
                                    <Trash2 size={20} />
                                </button>
                            </div>
                        </div>

                        {viewMode === 'architecture' ? (
                            <div className="p-8 flex-1 flex flex-col animate-in fade-in duration-500">
                                <ArchitectureDiagram architecture={selectedIdea?.architecture} onSave={handleSaveArchitecture} />
                            </div>
                        ) : viewMode === 'docs' ? (
                            <div className="flex-1 p-8 overflow-y-auto custom-scrollbar space-y-8 animate-in fade-in duration-500">
                                <section className="card p-8 rounded-3xl bg-white/5 border border-white/5 space-y-6 hover:border-purple-500/30 transition-all group">
                                    <div className="flex items-center gap-3 text-purple-400 font-bold text-sm uppercase tracking-widest">
                                        <div className="w-8 h-8 rounded-lg bg-purple-500/10 flex items-center justify-center border border-purple-500/20 group-hover:bg-purple-500/20 transition-all">
                                            <Share2 className="w-4 h-4" />
                                        </div>
                                        Knowledge Base & Related Links
                                    </div>
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                        {(selectedIdea.links || [
                                            "https://techcrunch.com", 
                                            "https://news.ycombinator.com",
                                            "https://producthunt.com"
                                        ]).map((link, i) => (
                                            <a key={i} href={link} target="_blank" rel="noopener noreferrer" className="flex items-center gap-4 bg-slate-900/40 p-4 rounded-2xl border border-white/5 hover:border-purple-500/30 hover:bg-purple-500/5 transition-all group/link">
                                                <div className="w-10 h-10 rounded-xl bg-slate-800 flex items-center justify-center text-slate-500 group-hover/link:text-purple-400 group-hover/link:bg-purple-500/10 transition-all">
                                                    <Network size={18} />
                                                </div>
                                                <div className="flex-1 overflow-hidden">
                                                    <p className="text-sm text-slate-300 font-medium truncate">{link}</p>
                                                    <p className="text-[10px] text-slate-500 uppercase font-bold tracking-widest mt-0.5">Reference Data</p>
                                                </div>
                                                <ArrowRight size={14} className="text-slate-700 group-hover/link:text-purple-400 group-hover/link:translate-x-1 transition-all" />
                                            </a>
                                        ))}
                                    </div>
                                    <button className="w-full py-4 border-2 border-dashed border-white/5 rounded-2xl text-slate-600 text-xs font-bold uppercase tracking-widest hover:border-purple-500/20 hover:text-purple-400/50 transition-all">
                                        + Inject External Link
                                    </button>
                                </section>

                                <section className="card p-8 rounded-3xl bg-white/5 border border-white/5 space-y-6 hover:border-blue-500/30 transition-all group">
                                    <div className="flex items-center gap-3 text-blue-400 font-bold text-sm uppercase tracking-widest">
                                        <div className="w-8 h-8 rounded-lg bg-blue-500/10 flex items-center justify-center border border-blue-500/20 group-hover:bg-blue-500/20 transition-all">
                                            <Sparkles className="w-4 h-4" />
                                        </div>
                                        Creative Inspirations
                                    </div>
                                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                                        {(selectedIdea.inspirations || [
                                            { title: "Cyberpunk Aesthetic", desc: "High tech, low life vibe for the interface." },
                                            { title: "Neural Networks", desc: "The concept of interconnected data nodes." }
                                        ]).map((insp, i) => (
                                            <div key={i} className="bg-slate-900/40 p-6 rounded-2xl border border-white/5 hover:border-blue-500/30 transition-all">
                                                <h4 className="text-sm font-bold text-white mb-2">{insp.title || insp}</h4>
                                                <p className="text-xs text-slate-500 leading-relaxed">{insp.desc || "Visual or conceptual baseline for the project."}</p>
                                            </div>
                                        ))}
                                        <div className="border-2 border-dashed border-white/5 rounded-2xl flex flex-col items-center justify-center p-6 text-slate-600 group/add hover:border-blue-500/20 transition-all cursor-pointer">
                                            <Plus size={24} className="mb-2 opacity-20 group-hover/add:opacity-100 group-hover/add:text-blue-400 transition-all" />
                                            <span className="text-[10px] uppercase font-bold tracking-widest">Add Signal</span>
                                        </div>
                                    </div>
                                </section>
                            </div>
                        ) : (
                            <div className="flex-1 p-8 overflow-y-auto custom-scrollbar space-y-8">
                                <section className="card p-8 rounded-3xl bg-white/5 border border-white/5 space-y-6 hover:border-indigo-500/30 transition-all group">
                                    <div className="flex items-center gap-3 text-indigo-400 font-bold text-sm uppercase tracking-widest">
                                        <div className="w-8 h-8 rounded-lg bg-indigo-500/10 flex items-center justify-center border border-indigo-500/20 group-hover:bg-indigo-500/20 transition-all">
                                            <StickyNote className="w-4 h-4" />
                                        </div>
                                        Detailed Exploration
                                    </div>
                                    <div className="text-slate-300 leading-relaxed text-lg whitespace-pre-wrap font-medium pl-2 border-l-2 border-indigo-500/20">
                                        {selectedIdea.explanation || 'No detailed explanation provided yet.'}
                                    </div>
                                </section>

                                <div className="grid grid-cols-2 gap-8 pt-4 border-t border-slate-800">
                                    <section className="card p-6 rounded-2xl bg-white/5 border border-white/5 space-y-4">
                                        <div className="flex items-center justify-between">
                                            <div className="flex items-center gap-3 text-yellow-400 font-bold text-sm uppercase"><StickyNote className="w-5 h-5" />Thought Logs</div>
                                            {!isQuickAddingNote && <button onClick={() => setIsQuickAddingNote(true)} className="text-[10px] text-blue-400 hover:text-blue-300 uppercase font-bold tracking-widest">+ Inject Note</button>}
                                        </div>
                                        
                                        {isQuickAddingNote && (
                                            <div className="flex flex-col gap-2 p-3 bg-slate-900 rounded-2xl border border-blue-500/30 animate-in zoom-in-95 duration-200 shadow-2xl">
                                                <input autoFocus value={quickNote} onChange={(e) => setQuickNote(e.target.value)} onKeyDown={(e) => e.key === 'Enter' && handleQuickSaveNote()} placeholder="Recording thought..." className="bg-transparent border-none text-sm text-white focus:outline-none" />
                                                <div className="flex justify-end gap-3 p-1">
                                                    <button onClick={() => setIsQuickAddingNote(false)} className="text-[10px] text-slate-500 font-bold">Abort</button>
                                                    <button onClick={handleQuickSaveNote} className="text-[10px] text-blue-400 font-bold uppercase tracking-widest">Execute</button>
                                                </div>
                                            </div>
                                        )}
                                        
                                        <div className="space-y-3">
                                            {(selectedIdea.notes || []).map((note, i) => (
                                                <div key={i} className="flex gap-4 bg-slate-900/40 p-4 rounded-2xl border border-white/5 hover:border-white/10 transition-all group">
                                                    <div className="h-2 w-2 rounded-full bg-yellow-500 mt-1.5 shrink-0 shadow-[0_0_10px_#f59e0b]" />
                                                    <p className="text-sm text-slate-300 leading-relaxed">{note}</p>
                                                </div>
                                            ))}
                                        </div>
                                    </section>

                                    <section className="card p-6 rounded-2xl bg-white/5 border border-white/5 space-y-4">
                                        <div className="flex items-center justify-between">
                                            <div className="flex items-center gap-3 text-orange-400 font-bold text-sm uppercase"><AlertCircle className="w-5 h-5" />System Hurdles</div>
                                            {!isQuickAddingHurdle && <button onClick={() => setIsQuickAddingHurdle(true)} className="text-[10px] text-orange-400 hover:text-orange-300 uppercase font-bold tracking-widest">+ Log Hurdle</button>}
                                        </div>

                                        {isQuickAddingHurdle && (
                                            <div className="flex flex-col gap-3 p-4 bg-slate-900 rounded-2xl border border-orange-500/30 animate-in zoom-in-95 duration-200 shadow-2xl">
                                                <input autoFocus value={quickHurdle.title} onChange={(e) => setQuickHurdle({...quickHurdle, title: e.target.value})} placeholder="Obstacle name..." className="bg-transparent border-none text-sm text-white font-bold focus:outline-none" />
                                                <textarea rows="2" value={quickHurdle.desc} onChange={(e) => setQuickHurdle({...quickHurdle, desc: e.target.value})} placeholder="Context..." className="bg-transparent border-none text-xs text-slate-400 focus:outline-none resize-none" />
                                                <div className="flex justify-end gap-3">
                                                    <button onClick={() => setIsQuickAddingHurdle(false)} className="text-[10px] text-slate-500 font-bold uppercase">Cancel</button>
                                                    <button onClick={handleQuickSaveHurdle} className="text-[10px] text-orange-400 font-bold uppercase tracking-widest">Store Data</button>
                                                </div>
                                            </div>
                                        )}

                                        <div className="space-y-4">
                                            {(selectedIdea.hurdles || []).map((hurdle, i) => (
                                                <div key={i} className="bg-slate-900/60 p-5 rounded-2xl border border-orange-500/20 group hover:border-orange-500/40 transition-all">
                                                    <div className="flex justify-between items-start mb-2">
                                                        <h4 className="font-bold text-slate-100 group-hover:text-orange-300 transition-colors uppercase tracking-tight">{hurdle.main_setback}</h4>
                                                        <span className="text-[9px] text-slate-600 font-mono">{hurdle.date}</span>
                                                    </div>
                                                    <p className="text-xs text-slate-400 leading-relaxed mb-4">{hurdle.description}</p>
                                                    {hurdle.leads?.length > 0 && (
                                                        <div className="flex flex-wrap gap-2 pt-3 border-t border-slate-700/50">
                                                            {hurdle.leads.map((l, j) => (
                                                                <span key={j} className="text-[9px] text-emerald-400 bg-emerald-500/10 px-2 py-1 rounded-md border border-emerald-500/10"># {l}</span>
                                                            ))}
                                                        </div>
                                                    )}
                                                </div>
                                            ))}
                                        </div>
                                    </section>
                                </div>
                            </div>
                        )}
                    </div>
                ) : (
                    <div className="h-full flex flex-col items-center justify-center text-slate-500 text-center gap-8 animate-in fade-in zoom-in-95 duration-1000">
                        <div className="w-24 h-24 rounded-[2rem] bg-slate-900/50 flex items-center justify-center border border-slate-700/50 shadow-2xl relative">
                            <div className="absolute inset-0 bg-blue-500/5 blur-2xl rounded-full" />
                            <Lightbulb className="w-12 h-12 opacity-20" />
                        </div>
                        <div>
                            <h2 className="text-2xl font-bold text-white tracking-tight">Select a Data Stream</h2>
                            <p className="text-sm opacity-50 mt-2">Initialize a concept from the archive or launch new logic.</p>
                        </div>
                    </div>
                )}
                {isGlobalChatOpen && (
                    <div className="w-[400px] h-full absolute right-0 top-0 z-50">
                        <Chatbot idea={null} onClose={() => setIsGlobalChatOpen(false)} onUpdate={fetchIdeas} />
                    </div>
                )}
            </main>

            <ConfirmationModal 
                isOpen={confirmModal.isOpen}
                title={confirmModal.title}
                message={confirmModal.message}
                onConfirm={confirmModal.onConfirm}
                onCancel={() => setConfirmModal(prev => ({ ...prev, isOpen: false }))}
                confirmText="Purge"
                cancelText="Abort"
            />

            <style>{`
              @keyframes loading {
                0% { transform: translateX(-100%); }
                100% { transform: translateX(100%); }
              }
              .custom-scrollbar::-webkit-scrollbar { width: 4px; }
              .custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(59, 130, 246, 0.1); border-radius: 20px; }
              .custom-scrollbar::-webkit-scrollbar-thumb:hover { background: rgba(59, 130, 246, 0.2); }
              .glass {
                background: rgba(15, 17, 45, 0.7);
                backdrop-filter: blur(24px);
              }
              .primary {
                background: linear-gradient(135deg, #2563eb 0%, #4f46e5 100%);
              }
              .card {
                background: linear-gradient(160deg, rgba(255,255,255,0.03) 0%, rgba(255,255,255,0.01) 100%);
              }
            `}</style>
        </div>
    );
};

export default App;
