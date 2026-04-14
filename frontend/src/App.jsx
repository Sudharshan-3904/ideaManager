import React, { useState, useEffect } from 'react';
import { 
  Plus, Trash2, Edit3, Save, X, Lightbulb, Users, Target, Rocket, Activity,
  ChevronRight, MessageCircle, MoreVertical, Search, CheckCircle
} from 'lucide-react';
import * as api from './api';

const App = () => {
    const [ideas, setIdeas] = useState([]);
    const [selectedIdea, setSelectedIdea] = useState(null);
    const [isAdding, setIsAdding] = useState(false);
    const [isEditing, setIsEditing] = useState(false);
    const [searchQuery, setSearchQuery] = useState('');
    
    // New Idea Form State
    const [formData, setFormData] = useState({
        title: '',
        description: '',
        target_customers: '',
        minimal_deliverables: '',
        future_extensions: ''
    });

    useEffect(() => {
        fetchIdeas();
    }, []);

    const fetchIdeas = async () => {
        try {
            const data = await api.getIdeas();
            setIdeas(data);
            if (data.length > 0 && !selectedIdea) {
                setSelectedIdea(data[0]);
            }
        } catch (error) {
            console.error('Failed to fetch ideas:', error);
        }
    };

    const handleSelectIdea = (idea) => {
        setSelectedIdea(idea);
        setIsEditing(false);
        setIsAdding(false);
    };

    const handleAddClick = () => {
        setIsAdding(true);
        setIsEditing(false);
        setSelectedIdea(null);
        setFormData({
            title: '',
            description: '',
            target_customers: '',
            minimal_deliverables: '',
            future_extensions: ''
        });
    };

    const handleEditClick = () => {
        setIsEditing(true);
        setIsAdding(false);
        setFormData({
            title: selectedIdea.title,
            description: selectedIdea.description,
            target_customers: selectedIdea.target_customers,
            minimal_deliverables: selectedIdea.minimal_deliverables,
            future_extensions: selectedIdea.future_extensions
        });
    };

    const handleSave = async (e) => {
        e.preventDefault();
        try {
            if (isAdding) {
                await api.createIdea(formData);
            } else if (isEditing) {
                await api.updateIdea(selectedIdea.title, formData);
            }
            await fetchIdeas();
            setIsAdding(false);
            setIsEditing(false);
            // Re-select if updated
            const updated = await api.getIdea(formData.title);
            setSelectedIdea(updated);
        } catch (error) {
            alert('Error saving idea: ' + error.message);
        }
    };

    const handleDelete = async (title) => {
        if (window.confirm(`Are you sure you want to delete "${title}"?`)) {
            try {
                await api.deleteIdea(title);
                fetchIdeas();
                setSelectedIdea(null);
            } catch (error) {
                alert('Error deleting idea: ' + error.message);
            }
        }
    };

    const filteredIdeas = ideas.filter(i => 
        i.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        i.description.toLowerCase().includes(searchQuery.toLowerCase())
    );

    return (
        <div className="flex h-screen w-full bg-[#0a0b1e] text-slate-200 font-sans overflow-hidden">
            {/* Sidebar */}
            <div className="w-80 h-full glass border-r border-slate-700/50 flex flex-col m-3 rounded-2xl">
                <div className="p-6 border-b border-slate-700/50 flex flex-col gap-4">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2 text-xl font-bold">
                            <Lightbulb className="text-yellow-400 w-6 h-6" />
                            <span className="bg-gradient-to-r from-blue-400 to-indigo-400 bg-clip-text text-transparent">
                                IdeaManager
                            </span>
                        </div>
                    </div>
                </div>

                <div className="p-4 flex flex-col gap-3 flex-1 overflow-y-auto custom-scrollbar">
                    <div className="relative">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
                        <input 
                            type="text" 
                            placeholder="Find an idea..." 
                            className="w-full bg-slate-900/50 border border-slate-700/50 rounded-xl py-2 pl-9 pr-4 text-sm focus:outline-none focus:border-blue-500/50 transition-all"
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                        />
                    </div>

                    <div className="flex flex-col gap-1 mt-2">
                        {filteredIdeas.length > 0 ? filteredIdeas.map((idea) => (
                            <div 
                                key={idea.title}
                                onClick={() => handleSelectIdea(idea)}
                                className={`group flex items-center justify-between p-3 rounded-xl cursor-pointer transition-all duration-200 ${
                                    selectedIdea?.title === idea.title 
                                    ? 'bg-blue-600/20 border border-blue-500/30' 
                                    : 'hover:bg-slate-800/50 border border-transparent'
                                }`}
                            >
                                <div className="flex flex-col overflow-hidden">
                                    <span className={`font-medium truncate ${selectedIdea?.title === idea.title ? 'text-blue-300' : 'text-slate-300'}`}>
                                        {idea.title}
                                    </span>
                                    <span className="text-xs text-slate-500 truncate mt-0.5">
                                        {idea.target_customers || 'No target profile'}
                                    </span>
                                </div>
                                <ChevronRight className={`w-4 h-4 transition-transform ${selectedIdea?.title === idea.title ? 'translate-x-0 opacity-100 text-blue-400' : '-translate-x-2 opacity-0'}`} />
                            </div>
                        )) : (
                            <div className="text-center py-10 opacity-50 text-sm italic">
                                No ideas found...
                            </div>
                        )}
                    </div>
                </div>

                <div className="p-4">
                    <button 
                        onClick={handleAddClick}
                        className="w-full primary flex items-center justify-center gap-2 py-3 rounded-xl font-semibold transform hover:scale-[1.02] active:scale-95 transition-all"
                    >
                        <Plus size={20} />
                        New Concept
                    </button>
                </div>
            </div>

            {/* Main Content */}
            <main className="flex-1 h-full m-3 ml-0 rounded-2xl glass flex flex-col overflow-hidden relative border border-slate-700/50 overflow-y-auto">
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
                          <div className="space-y-2">
                              <label className="text-xs font-bold uppercase tracking-wider text-slate-500 ml-2">Title</label>
                              <input 
                                required
                                value={formData.title}
                                onChange={(e) => setFormData({...formData, title: e.target.value})}
                                placeholder="What's the name of the idea?"
                                className="w-full bg-slate-900 border border-slate-700/50 rounded-xl py-4 px-6 text-lg focus:outline-none focus:border-blue-500/50 transition-all font-medium"
                              />
                          </div>
                          
                          <div className="grid grid-cols-2 gap-6">
                            <div className="space-y-2">
                                <label className="text-xs font-bold uppercase tracking-wider text-slate-500 ml-2">Target Market</label>
                                <input 
                                  value={formData.target_customers}
                                  onChange={(e) => setFormData({...formData, target_customers: e.target.value})}
                                  placeholder="Who is this for?"
                                  className="w-full bg-slate-900/50 border border-slate-700/50 rounded-xl py-3 px-4 text-sm focus:outline-none focus:border-blue-500/50"
                                />
                            </div>
                            <div className="space-y-2">
                                <label className="text-xs font-bold uppercase tracking-wider text-slate-500 ml-2">Minimal Deliverables</label>
                                <input 
                                  value={formData.minimal_deliverables}
                                  onChange={(e) => setFormData({...formData, minimal_deliverables: e.target.value})}
                                  placeholder="Core features for MVP"
                                  className="w-full bg-slate-900/50 border border-slate-700/50 rounded-xl py-3 px-4 text-sm focus:outline-none focus:border-blue-500/50"
                                />
                            </div>
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

                          <div className="space-y-2">
                              <label className="text-xs font-bold uppercase tracking-wider text-slate-500 ml-2">Future Extensions</label>
                              <textarea 
                                rows="3"
                                value={formData.future_extensions}
                                onChange={(e) => setFormData({...formData, future_extensions: e.target.value})}
                                placeholder="Where could this go next?"
                                className="w-full bg-slate-900/50 border border-slate-700/50 rounded-xl py-4 px-6 text-sm focus:outline-none focus:border-blue-500/50 resize-none"
                              />
                          </div>

                          <div className="flex gap-4 pt-6">
                              <button type="submit" className="primary flex-1 flex items-center justify-center gap-2 py-4 rounded-xl text-lg tracking-wide hover:shadow-[0_0_30px_rgba(37,117,252,0.3)]">
                                  <Save className="w-5 h-5" />
                                  Commit Concept
                              </button>
                          </div>
                      </form>
                  </div>
                ) : selectedIdea ? (
                    <div className="p-0 h-full flex flex-col animate-in fade-in duration-700">
                        {/* Detail Header */}
                        <div className="p-8 border-b border-slate-700/50 flex items-start justify-between bg-gradient-to-br from-indigo-900/10 to-transparent">
                            <div className="flex-1">
                                <div className="flex items-center gap-2 text-blue-400 font-bold text-xs uppercase tracking-tighter mb-2">
                                    <CheckCircle className="w-3 h-3" />
                                    Active Project Data
                                </div>
                                <h1 className="text-4xl font-extrabold text-white tracking-tight">{selectedIdea.title}</h1>
                                <p className="text-slate-400 mt-3 max-w-2xl leading-relaxed">{selectedIdea.description || 'No description provided yet.'}</p>
                            </div>
                            <div className="flex gap-2">
                                <button onClick={handleEditClick} className="p-3 bg-slate-800 hover:bg-slate-700 rounded-xl transition-all border border-slate-700/50 hover:border-blue-500/50 text-blue-300">
                                    <Edit3 size={20} />
                                </button>
                                <button onClick={() => handleDelete(selectedIdea.title)} className="p-3 bg-red-950/20 hover:bg-red-900/40 rounded-xl transition-all border border-red-500/20 hover:border-red-500/50 text-red-500">
                                    <Trash2 size={20} />
                                </button>
                            </div>
                        </div>

                        {/* Panels */}
                        <div className="flex-1 p-8 grid grid-cols-2 gap-8 content-start overflow-y-auto custom-scrollbar">
                            <div className="space-y-8">
                                <section className="card p-6 rounded-2xl bg-white/5 border border-white/5 space-y-4 hover:bg-white/10 transition-colors">
                                    <div className="flex items-center gap-3 text-indigo-400 font-bold text-sm uppercase">
                                        <Users className="w-5 h-5" />
                                        Target Market
                                    </div>
                                    <p className="text-slate-300 leading-relaxed font-medium">
                                        {selectedIdea.target_customers || 'Who will derive value from this solution? Profile them here.'}
                                    </p>
                                </section>

                                <section className="card p-6 rounded-2xl bg-white/5 border border-white/5 space-y-4 hover:bg-white/10 transition-colors">
                                    <div className="flex items-center gap-3 text-emerald-400 font-bold text-sm uppercase">
                                        <Rocket className="w-5 h-5" />
                                        MVP Roadmap
                                    </div>
                                    <p className="text-slate-300 leading-relaxed">
                                        {selectedIdea.minimal_deliverables || 'Define the smallest possible version that provides value.'}
                                    </p>
                                </section>
                            </div>

                            <div className="space-y-8">
                                <section className="card p-6 rounded-2xl bg-white/5 border border-white/5 space-y-4 hover:bg-white/10 transition-colors">
                                    <div className="flex items-center gap-3 text-purple-400 font-bold text-sm uppercase">
                                        <MoreVertical className="w-5 h-5" />
                                        Visionary Extensions
                                    </div>
                                    <p className="text-slate-300 leading-relaxed">
                                        {selectedIdea.future_extensions || 'Log future expansion opportunities beyond the initial launch.'}
                                    </p>
                                </section>

                                <section className="card p-6 rounded-2xl bg-blue-900/10 border border-blue-500/10 space-y-4">
                                    <div className="flex items-center gap-3 text-blue-400 font-bold text-sm uppercase">
                                        <Activity className="w-5 h-5" />
                                        System Insights
                                    </div>
                                    <div className="flex justify-between text-xs text-slate-500">
                                        <span>Status</span>
                                        <span className="text-blue-400 font-bold uppercase">Draft Analysis</span>
                                    </div>
                                    <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden mt-2">
                                        <div className="bg-blue-500 h-full w-1/3 shadow-[0_0_10px_#3b82f6]"></div>
                                    </div>
                                </section>
                            </div>
                        </div>
                    </div>
                ) : (
                    <div className="h-full flex flex-col items-center justify-center text-slate-500 text-center gap-6 animate-pulse">
                        <div className="w-20 h-20 rounded-3xl bg-slate-900 flex items-center justify-center border border-slate-800 shadow-xl">
                            <Lightbulb className="w-10 h-10 opacity-30" />
                        </div>
                        <div>
                            <h2 className="text-xl font-medium">Select an idea to visualize</h2>
                            <p className="text-sm opacity-60">or launch a brand new concept from the sidebar</p>
                        </div>
                    </div>
                )}
            </main>

            <style>{`
              .custom-scrollbar::-webkit-scrollbar { width: 4px; }
              .custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 20px; }
              .custom-scrollbar::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.2); }
              .primary {
                background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
              }
            `}</style>
        </div>
    );
};

export default App;
