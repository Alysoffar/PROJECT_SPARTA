"""Memory Manager - Vector memory and design storage"""
import json
import os
from typing import Dict, Any, List
from datetime import datetime


class MemoryManager:
    """Manages short-term and long-term memory for design sessions"""
    
    def __init__(self, memory_file="backend/memory/local_memory.json"):
        self.memory_file = memory_file
        self.session_memory: Dict[str, List[Dict]] = {}  # Short-term RAM
        self.design_library: List[Dict] = []  # Long-term storage
    
    async def initialize(self):
        """Load existing memory from disk"""
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
        
        if os.path.exists(self.memory_file):
            with open(self.memory_file, "r") as f:
                data = json.load(f)
                self.design_library = data.get("designs", [])
        print("✅ Memory manager initialized")
    
    async def load_recent_messages(self, session_id: str, n: int = 5) -> List[Dict]:
        """Load recent messages for context"""
        return self.session_memory.get(session_id, [])[-n:]
    
    async def save_design(self, session_id: str, design_data: Dict[str, Any]):
        """Save completed design to long-term memory"""
        design_entry = {
            "session_id": session_id,
            "timestamp": datetime.utcnow().isoformat(),
            **design_data
        }
        
        self.design_library.append(design_entry)
        
        # Persist to disk
        with open(self.memory_file, "w") as f:
            json.dump({"designs": self.design_library}, f, indent=2)
    
    async def search(self, query: str, limit: int = 5) -> List[Dict]:
        """
        Search design library for similar designs
        Simple keyword matching - could be upgraded to embeddings
        """
        query_lower = query.lower()
        results = []
        
        for design in self.design_library:
            spec = design.get("spec", {})
            component = spec.get("component", "")
            description = spec.get("description", "")
            
            if query_lower in component.lower() or query_lower in description.lower():
                results.append(design)
        
        return results[:limit]
    
    def add_message_to_session(self, session_id: str, role: str, content: str):
        """Add message to session memory"""
        if session_id not in self.session_memory:
            self.session_memory[session_id] = []
        
        self.session_memory[session_id].append({
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat()
        })
