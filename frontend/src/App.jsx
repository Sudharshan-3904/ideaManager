import React, { useState, useEffect } from 'react';
import { 
  Plus, Trash2, Edit3, Save, X, Lightbulb, Users, Target, Rocket, Activity,
  ChevronRight, MessageCircle, MoreVertical, Search, CheckCircle,
  StickyNote, AlertCircle, Zap, ArrowRight, List
} from 'lucide-react';
import * as api from './api';
import ArchitectureDiagram from './components/ArchitectureDiagram';
import { Network, Share2 } from 'lucide-react';


const App = () => {
    const [ideas, setIdeas] = useState([]);
    const [selectedIdea, setSelectedIdea] = useState(null);
    const [isAdding, setIsAdding] = useState(false);
    const [isEditing, setIsEditing] = useState(false);
    const [searchQuery, setSearchQuery] = useState('');
    const [viewMode, setViewMode] = useState('ideas'); // 'ideas' or 'architecture'
    const [quickNote, setQuickNote] = useState('');
    const [quickHurdle, setQuickHurdle] = useState({ title: '', desc: '' });
    const [isQuickAddingNote, setIsQuickAddingNote] = useState(false);
    const [isQuickAddingHurdle, setIsQuickAddingHurdle] = useState(false);

    
    // New Idea Form State
    const [formData, setFormData] = useState({
        title: '',
        description: '',
        target_customers: '',
        minimal_deliverables: '',
        future_extensions: '',
        notes: [],
        hurdles: []
    });

    useEffect(() => {
        fetchIdeas();
    }, []);

    const fetchIdeas = async (shouldSelectUpdated = null) => {
        try {
            const data = await api.getIdeas();
            setIdeas(data);
            
            if (shouldSelectUpdated) {
                const updated = data.find(i => i.title.trim().toLowerCase() === shouldSelectUpdated.trim().toLowerCase());
                if (updated) setSelectedIdea(updated);
            } else if (data.length > 0 && !selectedIdea) {
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
            future_extensions: '',
            notes: [],
            hurdles: []
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
            future_extensions: selectedIdea.future_extensions,
            notes: selectedIdea.notes || [],
            hurdles: selectedIdea.hurdles || []
        });
    };

    const handleAddNote = () => {
        setFormData({ ...formData, notes: [...formData.notes, ''] });
    };

    const handleNoteChange = (index, value) => {
        const newNotes = [...formData.notes];
        newNotes[index] = value;
        setFormData({ ...formData, notes: newNotes });
    };

    const handleRemoveNote = (index) => {
        setFormData({ ...formData, notes: formData.notes.filter((_, i) => i !== index) });
    };

    const handleAddHurdle = () => {
        setFormData({ 
            ...formData, 
            hurdles: [...formData.hurdles, { main_setback: '', description: '', leads: [] }] 
        });
    };

    const handleHurdleChange = (index, field, value) => {
        const newHurdles = [...formData.hurdles];
        newHurdles[index] = { ...newHurdles[index], [field]: value };
        setFormData({ ...formData, hurdles: newHurdles });
    };

    const handleRemoveHurdle = (index) => {
        setFormData({ ...formData, hurdles: formData.hurdles.filter((_, i) => i !== index) });
    };

    const handleAddLead = (hurdleIndex) => {
        const newHurdles = [...formData.hurdles];
        newHurdles[hurdleIndex].leads = [...newHurdles[hurdleIndex].leads, ''];
        setFormData({ ...formData, hurdles: newHurdles });
    };

    const handleLeadChange = (hurdleIndex, leadIndex, value) => {
        const newHurdles = [...formData.hurdles];
        newHurdles[hurdleIndex].leads[leadIndex] = value;
        setFormData({ ...formData, hurdles: newHurdles });
    };

    const handleRemoveLead = (hurdleIndex, leadIndex) => {
        const newHurdles = [...formData.hurdles];
        newHurdles[hurdleIndex].leads = newHurdles[hurdleIndex].leads.filter((_, i) => i !== leadIndex);
        setFormData({ ...formData, hurdles: newHurdles });
    };

    const handleSave = async (e) => {
        e.preventDefault();
        
        // Clean up empty entries
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

        try {
            if (isAdding) {
                await api.createIdea(cleanData);
            } else if (isEditing) {
                await api.updateIdea(selectedIdea.title, cleanData);
            }
            await fetchIdeas();
            setIsAdding(false);
            setIsEditing(false);
            // Re-select if updated
            const updated = await api.getIdea(cleanData.title);
            setSelectedIdea(updated);
        } catch (error) {
            alert('Error saving idea: ' + error.message);
        }
    };

    const handleSaveArchitecture = async (newArchitecture) => {
        if (!selectedIdea) return;
        
        try {
            const updatedIdea = {
                ...selectedIdea,
                architecture: newArchitecture
            };
            await api.updateIdea(selectedIdea.title, updatedIdea);
            await fetchIdeas();
            setSelectedIdea(updatedIdea);
        } catch (error) {
            alert('Error saving architecture: ' + error.message);
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

    const handleQuickSaveNote = async () => {
        if (!quickNote.trim()) return;
        try {
            const updatedIdea = { ...selectedIdea, notes: [...(selectedIdea.notes || []), quickNote] };
            await api.updateIdea(selectedIdea.title, updatedIdea);
            await fetchIdeas(selectedIdea.title);
            setQuickNote('');
            setIsQuickAddingNote(false);
        } catch (error) {
            alert('Error adding note: ' + error.message);
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
            await api.updateIdea(selectedIdea.title, updatedIdea);
            await fetchIdeas(selectedIdea.title);
            setQuickHurdle({ title: '', desc: '' });
            setIsQuickAddingHurdle(false);
        } catch (error) {
            alert('Error adding hurdle: ' + error.message);
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
                        <div className="flex bg-slate-900/50 p-1 rounded-lg border border-slate-700/50 invisible">
                            <button className="p-1.5 rounded-md text-slate-500"><List size={16} /></button>
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
                          {/* ... form content same as before ... */}
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

                          <div className="space-y-4">
                              <div className="flex items-center justify-between ml-2">
                                  <label className="text-xs font-bold uppercase tracking-wider text-slate-500">Thought Notes</label>
                                  <button type="button" onClick={handleAddNote} className="text-xs text-blue-400 hover:text-blue-300 flex items-center gap-1 font-bold">
                                      <Plus size={14} /> Add Note
                                  </button>
                              </div>
                              <div className="space-y-2">
                                  {formData.notes.map((note, idx) => (
                                      <div key={idx} className="flex gap-2">
                                          <input 
                                              value={note}
                                              onChange={(e) => handleNoteChange(idx, e.target.value)}
                                              placeholder="Random thought or jotdown..."
                                              className="flex-1 bg-slate-900/50 border border-slate-700/50 rounded-xl py-2 px-4 text-sm focus:outline-none focus:border-blue-500/50"
                                          />
                                          <button type="button" onClick={() => handleRemoveNote(idx)} className="p-2 text-red-500 hover:bg-red-500/10 rounded-lg">
                                              <Trash2 size={16} />
                                          </button>
                                      </div>
                                  ))}
                              </div>
                          </div>

                          <div className="space-y-4 pt-4 border-t border-slate-800">
                              <div className="flex items-center justify-between ml-2">
                                  <label className="text-xs font-bold uppercase tracking-wider text-slate-500">Hurdles & Blockers</label>
                                  <button type="button" onClick={handleAddHurdle} className="text-xs text-orange-400 hover:text-orange-300 flex items-center gap-1 font-bold">
                                      <Plus size={14} /> Add Hurdle
                                  </button>
                              </div>
                              <div className="space-y-6">
                                  {formData.hurdles.map((hurdle, hIdx) => (
                                      <div key={hIdx} className="p-4 bg-slate-900/30 rounded-2xl border border-slate-800 space-y-4">
                                          <div className="flex gap-2">
                                              <input 
                                                  value={hurdle.main_setback}
                                                  onChange={(e) => handleHurdleChange(hIdx, 'main_setback', e.target.value)}
                                                  placeholder="The main setback..."
                                                  className="flex-1 bg-slate-900/50 border border-slate-700/50 rounded-xl py-2 px-4 text-sm font-bold focus:outline-none focus:border-orange-500/50"
                                              />
                                              <button type="button" onClick={() => handleRemoveHurdle(hIdx)} className="p-2 text-red-500 hover:bg-red-500/10 rounded-lg">
                                                  <Trash2 size={16} />
                                              </button>
                                          </div>
                                          <textarea 
                                              value={hurdle.description}
                                              onChange={(e) => handleHurdleChange(hIdx, 'description', e.target.value)}
                                              placeholder="Detailed description of the blocker..."
                                              className="w-full bg-slate-900/50 border border-slate-700/50 rounded-xl py-2 px-4 text-sm focus:outline-none focus:border-orange-500/50 resize-none"
                                              rows="2"
                                          />
                                          <div className="pl-4 border-l-2 border-slate-800 space-y-2">
                                              {hurdle.leads.map((lead, lIdx) => (
                                                  <div key={lIdx} className="flex gap-2">
                                                      <input value={lead} onChange={(e) => handleLeadChange(hIdx, lIdx, e.target.value)} className="flex-1 bg-slate-900/50 border border-slate-700/50 rounded-xl py-1 px-3 text-xs focus:outline-none" />
                                                  </div>
                                              ))}
                                          </div>
                                      </div>
                                  ))}
                              </div>
                          </div>

                          <div className="flex gap-4 pt-6">
                              <button type="submit" className="primary flex-1 flex items-center justify-center gap-2 py-4 rounded-xl text-lg font-bold">
                                  <Save className="w-5 h-5" />
                                  Commit Concept
                              </button>
                          </div>
                      </form>
                  </div>
                ) : selectedIdea ? (
                    <div className="p-0 h-full flex flex-col animate-in fade-in duration-700 relative">
                        {/* Detail Header - Persistent */}
                        <div className="p-8 border-b border-slate-700/50 flex items-start justify-between bg-gradient-to-br from-indigo-900/10 to-transparent sticky top-0 bg-[#0a0b1e]/80 backdrop-blur-xl z-20">
                            <div className="flex-1">
                                <div className="flex items-center gap-2 text-blue-400 font-bold text-xs uppercase tracking-tighter mb-2">
                                    <CheckCircle className="w-3 h-3" />
                                    Active Project Data
                                </div>
                                <h1 className="text-4xl font-extrabold text-white tracking-tight">{selectedIdea.title}</h1>
                                {viewMode === 'ideas' && <p className="text-slate-400 mt-3 max-w-2xl leading-relaxed">{selectedIdea.description || 'No description provided yet.'}</p>}
                            </div>
                            <div className="flex gap-2">
                                <div className="flex bg-slate-900/50 p-1 rounded-xl border border-slate-700/50 mr-2">
                                    <button onClick={() => setViewMode('ideas')} className={`px-4 py-2 rounded-lg flex items-center gap-2 text-sm font-bold transition-all ${viewMode === 'ideas' ? 'bg-blue-600 shadow-lg text-white' : 'text-slate-400 hover:text-slate-200'}`}>
                                        <List size={16} /> Dashboard
                                    </button>
                                    <button onClick={() => setViewMode('architecture')} className={`px-4 py-2 rounded-lg flex items-center gap-2 text-sm font-bold transition-all ${viewMode === 'architecture' ? 'bg-indigo-600 shadow-lg text-white' : 'text-slate-400 hover:text-slate-200'}`}>
                                        <Network size={16} /> Architecture
                                    </button>
                                </div>
                                <button onClick={handleEditClick} className="p-3 bg-slate-800 hover:bg-slate-700 rounded-xl transition-all border border-slate-700/50 text-blue-300">
                                    <Edit3 size={20} />
                                </button>
                                <button onClick={() => handleDelete(selectedIdea.title)} className="p-3 bg-red-950/20 hover:bg-red-900/40 rounded-xl transition-all border border-red-500/20 text-red-500">
                                    <Trash2 size={20} />
                                </button>
                            </div>
                        </div>

                        {viewMode === 'architecture' ? (
                            <div className="p-8 flex-1 flex flex-col animate-in fade-in duration-500">
                                <div className="flex-1 min-h-[500px]">
                                    <ArchitectureDiagram architecture={selectedIdea?.architecture} onSave={handleSaveArchitecture} />
                                </div>
                            </div>
                        ) : (
                            <div className="flex-1 p-8 overflow-y-auto custom-scrollbar space-y-8">
                                {/* Dashboard View Sections - Info panels and Side-by-Side bottom */}
                                <div className="grid grid-cols-3 gap-8 content-start">
                                    <section className="card p-6 rounded-2xl bg-white/5 border border-white/5 space-y-4 hover:bg-white/10 transition-colors">
                                        <div className="flex items-center gap-3 text-indigo-400 font-bold text-sm uppercase"><Users className="w-5 h-5" />Target Market</div>
                                        <p className="text-slate-300 leading-relaxed font-medium">{selectedIdea.target_customers || 'Who will derive value?'}</p>
                                    </section>
                                    <section className="card p-6 rounded-2xl bg-white/5 border border-white/5 space-y-4 hover:bg-white/10 transition-colors"><div className="flex items-center gap-3 text-emerald-400 font-bold text-sm uppercase"><Rocket className="w-5 h-5" />MVP Roadmap</div><p className="text-slate-300 leading-relaxed">{selectedIdea.minimal_deliverables || 'Define MVP'}</p></section>
                                    <section className="card p-6 rounded-2xl bg-white/5 border border-white/5 space-y-4 hover:bg-white/10 transition-colors"><div className="flex items-center gap-3 text-purple-400 font-bold text-sm uppercase"><MoreVertical className="w-5 h-5" />Visionary Extensions</div><p className="text-slate-300 leading-relaxed">{selectedIdea.future_extensions || 'Expansion opportunities'}</p></section>
                                </div>

                                <div className="grid grid-cols-2 gap-8 pt-4 border-t border-slate-800">
                                    <section className="card p-6 rounded-2xl bg-white/5 border border-white/5 space-y-4 hover:bg-white/10 transition-colors">
                                        <div className="flex items-center justify-between">
                                            <div className="flex items-center gap-3 text-yellow-400 font-bold text-sm uppercase"><StickyNote className="w-5 h-5" />Thought Notes</div>
                                            {!isQuickAddingNote && <button onClick={() => setIsQuickAddingNote(true)} className="text-[10px] text-blue-400 hover:text-blue-300 uppercase font-bold">+ Quick Add</button>}
                                        </div>
                                        
                                        {isQuickAddingNote && (
                                            <div className="flex flex-col gap-2 p-3 bg-slate-900 rounded-xl border border-blue-500/30 animate-in zoom-in-95 duration-200">
                                                <input autoFocus value={quickNote} onChange={(e) => setQuickNote(e.target.value)} onKeyDown={(e) => e.key === 'Enter' && handleQuickSaveNote()} placeholder="Compose thought..." className="bg-transparent border-none text-sm text-white focus:outline-none" />
                                                <div className="flex justify-end gap-2">
                                                    <button onClick={() => setIsQuickAddingNote(false)} className="text-[10px] text-slate-500">Cancel</button>
                                                    <button onClick={handleQuickSaveNote} className="text-[10px] text-blue-400 font-bold">Save</button>
                                                </div>
                                            </div>
                                        )}
                                        
                                        <div className="space-y-3">
                                            {selectedIdea.notes && selectedIdea.notes.length > 0 ? selectedIdea.notes.map((note, i) => (
                                                <div key={i} className="flex gap-3 bg-slate-900/40 p-3 rounded-xl border border-white/5 group"><div className="h-1.5 w-1.5 rounded-full bg-yellow-500 mt-1.5 shrink-0" /><p className="text-sm text-slate-300">{note}</p></div>
                                            )) : <p className="text-xs text-slate-500 italic">No notes recorded.</p>}
                                        </div>
                                    </section>

                                    <section className="card p-6 rounded-2xl bg-white/5 border border-white/5 space-y-4 hover:bg-white/10 transition-colors h-fit">
                                        <div className="flex items-center justify-between">
                                            <div className="flex items-center gap-3 text-orange-400 font-bold text-sm uppercase"><AlertCircle className="w-5 h-5" />Project Hurdles</div>
                                            {!isQuickAddingHurdle && <button onClick={() => setIsQuickAddingHurdle(true)} className="text-[10px] text-orange-400 hover:text-orange-300 uppercase font-bold">+ Quick Add</button>}
                                        </div>

                                        {isQuickAddingHurdle && (
                                            <div className="flex flex-col gap-3 p-3 bg-slate-900 rounded-xl border border-orange-500/30 animate-in zoom-in-95 duration-200">
                                                <input 
                                                    autoFocus 
                                                    value={quickHurdle.title} 
                                                    onChange={(e) => setQuickHurdle({...quickHurdle, title: e.target.value})} 
                                                    onKeyDown={(e) => e.key === 'Enter' && handleQuickSaveHurdle()}
                                                    placeholder="Setback name..." 
                                                    className="bg-transparent border-none text-sm text-white font-bold focus:outline-none" 
                                                />
                                                <textarea 
                                                    rows="2" 
                                                    value={quickHurdle.desc} 
                                                    onChange={(e) => setQuickHurdle({...quickHurdle, desc: e.target.value})} 
                                                    onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && (e.preventDefault(), handleQuickSaveHurdle())}
                                                    placeholder="Context..." 
                                                    className="bg-transparent border-none text-xs text-slate-400 focus:outline-none resize-none" 
                                                />
                                                <div className="flex justify-end gap-2">
                                                    <button onClick={() => setIsQuickAddingHurdle(false)} className="text-[10px] text-slate-500">Cancel</button>
                                                    <button onClick={handleQuickSaveHurdle} className="text-[10px] text-orange-400 font-bold">Save</button>
                                                </div>
                                            </div>
                                        )}

                                        <div className="space-y-4">
                                            {selectedIdea.hurdles && selectedIdea.hurdles.length > 0 ? selectedIdea.hurdles.map((hurdle, i) => (
                                                <div key={i} className="bg-slate-900/40 p-4 rounded-xl border border-orange-500/10 space-y-3">
                                                    <div className="flex justify-between items-start"><h4 className="font-bold text-slate-200">{hurdle.main_setback}</h4><span className="text-[10px] text-slate-600 font-mono tracking-tighter">{hurdle.date}</span></div>
                                                    <p className="text-xs text-slate-400 leading-relaxed">{hurdle.description}</p>
                                                    {hurdle.leads && hurdle.leads.length > 0 && <div className="pt-2 border-t border-slate-800 space-y-2"><div className="flex items-center gap-2 text-[10px] font-bold text-emerald-500 uppercase"><Zap className="w-3 h-3" />Potential Leads</div><div className="flex flex-wrap gap-1.5">{hurdle.leads.map((lead, j) => (<div key={j} className="flex items-center gap-2 text-[10px] text-emerald-200/70 bg-emerald-500/5 py-1 px-2 rounded-lg border border-emerald-500/10"><ArrowRight className="w-2.5 h-2.5" />{lead}</div>))}</div></div>}
                                                </div>
                                            )) : <p className="text-xs text-slate-500 italic">No hurdles identified.</p>}
                                        </div>
                                    </section>
                                </div>
                                
                                <section className="card p-6 rounded-2xl bg-blue-900/10 border border-blue-500/10 flex items-center justify-between">
                                    <div className="flex items-center gap-4">
                                        <div className="flex items-center gap-3 text-blue-400 font-bold text-sm uppercase"><Activity className="w-5 h-5" />System Insights</div>
                                        <div className="w-48 bg-slate-800 h-1.5 rounded-full overflow-hidden">
                                            <div className={`bg-blue-500 h-full shadow-[0_0_10px_#3b82f6] transition-all duration-1000 ${selectedIdea.hurdles?.length > 0 ? 'w-2/3' : 'w-1/3'}`}></div>
                                        </div>
                                    </div>
                                    <div className="flex gap-8 text-xs">
                                        <div className="flex flex-col"><span className="text-slate-500 uppercase font-bold tracking-tighter">Current Status</span><span className="text-blue-400 font-bold uppercase">{selectedIdea.hurdles?.length > 0 ? 'Blocked / Solving' : 'Clear / Analysis'}</span></div>
                                        <div className="flex flex-col"><span className="text-slate-500 uppercase font-bold tracking-tighter">Hurdles</span><span className="text-white font-bold">{selectedIdea.hurdles?.length || 0}</span></div>
                                        <div className="flex flex-col"><span className="text-slate-500 uppercase font-bold tracking-tighter">Notes</span><span className="text-white font-bold">{selectedIdea.notes?.length || 0}</span></div>
                                    </div>
                                </section>
                            </div>
                        )}
                    </div>
                ) : (
                    <div className="h-full flex flex-col items-center justify-center text-slate-500 text-center gap-6 animate-pulse">
                        <div className="w-20 h-20 rounded-3xl bg-slate-900 flex items-center justify-center border border-slate-800 shadow-xl"><Lightbulb className="w-10 h-10 opacity-30" /></div>
                        <div><h2 className="text-xl font-medium">Select an idea to visualize</h2><p className="text-sm opacity-60">or launch a brand new concept from the sidebar</p></div>
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
