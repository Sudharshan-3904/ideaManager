import React, { useCallback, useState, useEffect } from 'react';
import {
  ReactFlow,
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  addEdge,
  MarkerType,
} from '@xyflow/react';
import { Plus, Save, Trash2 } from 'lucide-react';

import '@xyflow/react/dist/style.css';

/**
 * ArchitectureDiagram Component
 * 
 * Provides an interactive node-based diagram editor for visualizing idea architectures.
 * Powered by React Flow.
 */
const nodeStyles = {
  default: { 
    background: 'rgba(56, 189, 248, 0.1)', 
    color: '#38bdf8', 
    border: '1px solid #38bdf8',
    borderRadius: '8px',
    padding: '10px',
    fontWeight: 'bold',
    width: 200,
  },
  server: {
    background: 'rgba(16, 185, 129, 0.1)', 
    color: '#10b981', 
    border: '1px solid #10b981',
    borderRadius: '8px',
    padding: '10px',
    fontWeight: 'bold',
    width: 200,
  },
  ai: {
    background: 'rgba(236, 72, 153, 0.1)', 
    color: '#ec4899', 
    border: '1px solid #ec4899',
    borderRadius: '8px',
    padding: '10px',
    fontWeight: 'bold',
    width: 200,
    borderStyle: 'dashed',
  }
};

export default function ArchitectureDiagram({ architecture, onSave }) {
  const [nodes, setNodes, onNodesChange] = useNodesState(architecture?.nodes || []);
  const [edges, setEdges, onEdgesChange] = useEdgesState(architecture?.edges || []);
  const [selectedElement, setSelectedElement] = useState(null);

  useEffect(() => {
    setNodes(architecture?.nodes || []);
    setEdges(architecture?.edges || []);
  }, [architecture, setNodes, setEdges]);

  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge({
      ...params,
      animated: true,
      style: { stroke: '#94a3b8' },
      markerEnd: { type: MarkerType.ArrowClosed, color: '#94a3b8' },
    }, eds)),
    [setEdges],
  );

  const onNodeClick = (_, element) => setSelectedElement({ type: 'node', element });
  const onEdgeClick = (_, element) => setSelectedElement({ type: 'edge', element });
  const onPaneClick = () => setSelectedElement(null);

  const addNode = (styleType = 'default') => {
    const id = `${nodes.length + 1}`;
    const newNode = {
      id,
      data: { label: `New Node ${id}` },
      position: { x: Math.random() * 400, y: Math.random() * 400 },
      style: nodeStyles[styleType] || nodeStyles.default,
    };
    setNodes((nds) => nds.concat(newNode));
  };

  const deleteSelected = () => {
    if (!selectedElement) return;
    if (selectedElement.type === 'node') {
      setNodes((nds) => nds.filter((n) => n.id !== selectedElement.element.id));
      setEdges((eds) => eds.filter((e) => e.source !== selectedElement.element.id && e.target !== selectedElement.element.id));
    } else {
      setEdges((eds) => eds.filter((e) => e.id !== selectedElement.element.id));
    }
    setSelectedElement(null);
  };

  const updateLabel = (label) => {
    if (!selectedElement) return;
    if (selectedElement.type === 'node') {
      setNodes((nds) =>
        nds.map((node) => {
          if (node.id === selectedElement.element.id) {
            return { ...node, data: { ...node.data, label } };
          }
          return node;
        })
      );
    } else {
      setEdges((eds) =>
        eds.map((edge) => {
          if (edge.id === selectedElement.element.id) {
            return { ...edge, label };
          }
          return edge;
        })
      );
    }
  };

  const handleSave = () => {
    onSave({ nodes, edges });
  };

  return (
    <div className="relative flex-1 flex flex-col h-full bg-[#0f172a] rounded-2xl overflow-hidden border border-slate-700/50">
      {/* Toolbar */}
      <div className="absolute top-4 left-4 z-10 flex gap-2">
        <button onClick={() => addNode('default')} className="p-2 bg-slate-800 hover:bg-slate-700 text-blue-400 rounded-lg border border-slate-700 transition-all flex items-center gap-2 text-xs font-bold shadow-xl">
          <Plus size={16} /> UI/Component
        </button>
        <button onClick={() => addNode('server')} className="p-2 bg-slate-800 hover:bg-slate-700 text-emerald-400 rounded-lg border border-slate-700 transition-all flex items-center gap-2 text-xs font-bold shadow-xl">
          <Plus size={16} /> Backend/DB
        </button>
        <button onClick={() => addNode('ai')} className="p-2 bg-slate-800 hover:bg-slate-700 text-pink-400 rounded-lg border border-slate-700 transition-all flex items-center gap-2 text-xs font-bold shadow-xl">
          <Plus size={16} /> AI/External
        </button>
      </div>

      <div className="absolute top-4 right-4 z-10 flex gap-4">
        {selectedElement && (
          <div className="bg-slate-900/90 border border-slate-700 p-2 rounded-xl flex items-center gap-3 shadow-2xl backdrop-blur-md animate-in slide-in-from-right duration-300">
            <input 
              className="bg-slate-800 border-none rounded-lg px-3 py-1 text-xs text-white focus:ring-1 focus:ring-blue-500 w-32 focus:outline-none"
              placeholder="Edit label..."
              value={selectedElement.type === 'node' 
                ? nodes.find(n => n.id === selectedElement.element.id)?.data.label || ''
                : edges.find(e => e.id === selectedElement.element.id)?.label || ''}
              onChange={(e) => updateLabel(e.target.value)}
            />
            <button onClick={deleteSelected} className="p-1.5 bg-red-900/30 hover:bg-red-900/50 text-red-500 rounded-lg transition-colors">
              <Trash2 size={14} />
            </button>
          </div>
        )}
        <button onClick={handleSave} className="flex items-center gap-2 px-6 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-xl shadow-lg shadow-blue-500/20 transition-all font-bold active:scale-95">
          <Save size={18} />
          Sync Diagram
        </button>
      </div>

      <div style={{ flex: 1 }}>
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          onNodeClick={onNodeClick}
          onEdgeClick={onEdgeClick}
          onPaneClick={onPaneClick}
          fitView
        >
          <Controls />
          <MiniMap nodeStrokeWidth={3} zoomable pannable maskColor="rgba(0,0,0,0.3)" />
          <Background variant="dots" gap={12} size={1} color="#334155" />
        </ReactFlow>
      </div>
    </div>
  );
}
