"""
============================================
🗺️ الخريطة: 03_logic/logic_flow.py
📌 الربط:
    - يستقبل من vision_processor.py (الصور المحللة)
    - يرسل إلى video_engine.py (مخططات فيديو)
============================================
"""

# المتطلبات: networkx, mermaid-py, json

import networkx as nx
import json
from typing import Dict, Any, List
import asyncio
from datetime import datetime

class LogicSchematics:
    """مولد المخططات المنهجية والهياكل المنطقية"""
    
    def __init__(self):
        self.status = "🟢 نشط"
        self.graphs = {}
        print("🟢 Logic Schematics - جاهز لتوليد المخططات")
    
    async def generate(self, description: str) -> Dict:
        """توليد مخطط منطقي من وصف نصي"""
        try:
            # إنشاء رسم بياني جديد
            G = nx.DiGraph()
            
            # تحليل الوصف وتوليد العقد
            words = description.split()
            for i, word in enumerate(words[:10]):  # حد أقصى 10 عقد
                G.add_node(i, label=word, type="concept")
            
            # ربط العقد
            for i in range(len(G.nodes) - 1):
                G.add_edge(i, i + 1, weight=0.5)
            
            # تحويل إلى صيغة Mermaid
            mermaid_code = "graph TD\n"
            for node in G.nodes(data=True):
                mermaid_code += f"    N{node[0]}[{node[1]['label']}]\n"
            for edge in G.edges():
                mermaid_code += f"    N{edge[0]} --> N{edge[1]}\n"
            
            # حفظ المخطط
            graph_id = f"flow_{datetime.now().timestamp()}"
            self.graphs[graph_id] = {
                "graph": G,
                "mermaid": mermaid_code,
                "description": description
            }
            
            return {
                "status": "success",
                "graph_id": graph_id,
                "mermaid": mermaid_code,
                "nodes": len(G.nodes),
                "edges": len(G.edges),
                "structure": {
                    "nodes": [{"id": n, "label": d["label"]} for n, d in G.nodes(data=True)],
                    "edges": [{"from": e[0], "to": e[1]} for e in G.edges()]
                }
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    async def generate_from_image(self, image_analysis: Dict) -> Dict:
        """توليد مخطط منطقي من تحليل صورة"""
        try:
            # استخراج خصائص الصورة
            features = image_analysis.get("analysis", {}).get("features", [])
            
            # إنشاء مخطط بناءً على خصائص الصورة
            G = nx.DiGraph()
            
            # إضافة عقد للخصائص
            for i, feature in enumerate(features[:5]):
                G.add_node(i, label=f"Feature_{i}", value=feature)
            
            # ربط الخصائص
            for i in range(len(G.nodes) - 1):
                G.add_edge(i, i + 1, weight=abs(features[i] - features[i + 1]))
            
            # توليد Mermaid
            mermaid_code = "graph LR\n"
            mermaid_code += "    style default fill:#f9f,stroke:#333,stroke-width:2px\n"
            for node in G.nodes(data=True):
                mermaid_code += f"    F{node[0]}[{node[1]['label']}: {node[1]['value']:.3f}]\n"
            for edge in G.edges():
                mermaid_code += f"    F{edge[0]} -->|{G[edge[0]][edge[1]]['weight']:.3f}| F{edge[1]}\n"
            
            return {
                "status": "success",
                "mermaid": mermaid_code,
                "graph_type": "feature_flow",
                "source": "vision_analysis"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    async def export_json(self, graph_id: str) -> Dict:
        """تصدير المخطط بصيغة JSON"""
        if graph_id not in self.graphs:
            return {"status": "error", "message": "Graph not found"}
        
        graph_data = self.graphs[graph_id]
        G = graph_data["graph"]
        
        return {
            "status": "success",
            "graph_id": graph_id,
            "format": "json",
            "data": {
                "nodes": [{"id": n, "data": d} for n, d in G.nodes(data=True)],
                "edges": [{"source": e[0], "target": e[1], "data": G[e[0]][e[1]]} for e in G.edges()],
                "metadata": {
                    "created": graph_id.split("_")[1],
                    "description": graph_data["description"]
                }
            }
        }