import React from 'react';
import { AlertTriangle, X } from 'lucide-react';

const ConfirmationModal = ({ isOpen, title, message, onConfirm, onCancel, confirmText = "Confirm", cancelText = "Cancel" }) => {
    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-[100] flex items-center justify-center p-6 bg-black/60 backdrop-blur-sm animate-in fade-in duration-300">
            <div className="w-full max-w-md glass border border-white/10 rounded-[2rem] shadow-2xl overflow-hidden animate-in zoom-in-95 duration-300">
                <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-orange-500 to-red-600 opacity-50" />
                
                <div className="p-8">
                    <div className="flex items-start justify-between mb-6">
                        <div className="w-12 h-12 rounded-2xl bg-orange-500/10 flex items-center justify-center border border-orange-500/20">
                            <AlertTriangle className="w-6 h-6 text-orange-400" />
                        </div>
                        <button onClick={onCancel} className="p-2 hover:bg-white/5 rounded-full transition-colors text-slate-500">
                            <X size={20} />
                        </button>
                    </div>

                    <h3 className="text-xl font-bold text-white mb-2">{title}</h3>
                    <p className="text-slate-400 text-sm leading-relaxed mb-8">
                        {message}
                    </p>

                    <div className="flex gap-3">
                        <button 
                            onClick={onCancel}
                            className="flex-1 py-3 px-4 rounded-xl border border-white/5 bg-white/5 text-white text-sm font-semibold hover:bg-white/10 transition-all"
                        >
                            {cancelText}
                        </button>
                        <button 
                            onClick={onConfirm}
                            className="flex-1 py-3 px-4 rounded-xl bg-gradient-to-r from-orange-600 to-red-600 text-white text-sm font-semibold hover:shadow-lg hover:shadow-orange-600/20 transition-all active:scale-95"
                        >
                            {confirmText}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ConfirmationModal;
