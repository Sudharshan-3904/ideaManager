from components.hurdle import Hurdle
import json

class Idea:
    def __init__(self, title="", description="", target_customers="", minimal_deliverables="", future_extensions="", hurdles=None, notes=None, architecture=None, tags=None, is_archived=False, created_at=None, owner_username=None):
        self.title = title
        self.description = description
        self.target_customers = target_customers
        self.minimal_deliverables = minimal_deliverables
        self.future_extensions = future_extensions
        self.hurdles = hurdles if hurdles is not None else []
        self.notes = notes if notes is not None else []
        self.architecture = architecture if architecture is not None else {"nodes": [], "edges": []}
        self.tags = tags if tags is not None else []
        self.is_archived = is_archived
        self.created_at = created_at
        self.owner_username = owner_username

    def add_hurdle(self, hurdle):
        if isinstance(hurdle, Hurdle):
            self.hurdles.append(hurdle)
        else:
            raise ValueError("Object must be an instance of Hurdle")

    @classmethod
    def from_dict(cls, data):
        """Creates an Idea instance from a dictionary (e.g., a CSV row)."""
        # Note: This is legacy CSV fallback
        hurdles_str = data.get('hurdles', "")
        hurdles = []
        if hurdles_str:
            hurdle_strings = hurdles_str.split(';;')
            for h_str in hurdle_strings:
                h = Hurdle.loadFromStr(h_str)
                if h:
                    hurdles.append(h)
        
        notes_str = data.get('notes', "")
        notes = notes_str.split(';;') if notes_str else []
        
        arch_str = data.get('architecture', "")
        architecture = json.loads(arch_str) if arch_str else {"nodes": [], "edges": []}
        
        tags_str = data.get('tags', "")
        tags = tags_str.split(';;') if tags_str else []

        return cls(
            title=data.get('title', ""),
            description=data.get('description', ""),
            target_customers=data.get('target_customers', ""),
            minimal_deliverables=data.get('minimal_deliverables', ""),
            future_extensions=data.get('future_extensions', ""),
            hurdles=hurdles,
            notes=notes,
            architecture=architecture,
            tags=tags,
            is_archived=bool(int(data.get('is_archived', 0)))
        )

    @classmethod
    def from_db_row(cls, data):
        """Creates an Idea instance from a database dictionary row (already joined)."""
        hurdles = [Hurdle.from_db_dict(h) for h in data.get('hurdles', [])]
        
        arch_data = data.get('architecture', '{"nodes": [], "edges": []}')
        if isinstance(arch_data, str):
            architecture = json.loads(arch_data)
        else:
            architecture = arch_data

        return cls(
            title=data.get('title', ""),
            description=data.get('description', ""),
            target_customers=data.get('target_customers', ""),
            minimal_deliverables=data.get('minimal_deliverables', ""),
            future_extensions=data.get('future_extensions', ""),
            hurdles=hurdles,
            notes=data.get('notes', []),
            architecture=architecture,
            tags=data.get('tags', []),
            is_archived=bool(data.get('is_archived', 0)),
            created_at=data.get('created_at'),
            owner_username=data.get('owner_username')
        )

    def to_dict(self):
        """Serializes the Idea instance to a dictionary for API/JSON."""
        return {
            'title': self.title,
            'description': self.description,
            'target_customers': self.target_customers,
            'minimal_deliverables': self.minimal_deliverables,
            'future_extensions': self.future_extensions,
            'hurdles': [
                {
                    'date': h.date.strftime('%Y-%m-%d %H:%M:%S'),
                    'main_setback': h.main_setback,
                    'description': h.description,
                    'leads': h.leads
                } for h in self.hurdles
            ],
            'notes': self.notes,
            'architecture': self.architecture,
            'tags': self.tags,
            'is_archived': self.is_archived,
            'created_at': self.created_at
        }

    def to_db_dict(self):
        """Serializes the Idea instance for DB storage (nested dict)."""
        return {
            'title': self.title,
            'description': self.description,
            'target_customers': self.target_customers,
            'minimal_deliverables': self.minimal_deliverables,
            'future_extensions': self.future_extensions,
            'architecture': self.architecture,
            'is_archived': self.is_archived,
            'created_at': self.created_at,
            'owner_username': self.owner_username,
            'hurdles': [
                {
                    'date': h.date.strftime('%Y-%m-%d %H:%M:%S'),
                    'main_setback': h.main_setback,
                    'description': h.description,
                    'leads': h.leads
                } for h in self.hurdles
            ],
            'notes': self.notes,
            'tags': self.tags
        }

    def to_csv_dict(self):
        """Serializes the Idea instance to a dictionary for CSV storage."""
        hurdles_str = ";;".join([h.serialize() for h in self.hurdles])
        notes_str = ";;".join(self.notes)
        tags_str = ";;".join(self.tags)
        return {
            'title': self.title,
            'description': self.description,
            'target_customers': self.target_customers,
            'minimal_deliverables': self.minimal_deliverables,
            'future_extensions': self.future_extensions,
            'hurdles': hurdles_str,
            'notes': notes_str,
            'architecture': json.dumps(self.architecture),
            'tags': tags_str,
            'is_archived': 1 if self.is_archived else 0
        }

    def __repr__(self):
        return f"Idea('{self.title}', {len(self.hurdles)} hurdles, {len(self.notes)} notes, archived={self.is_archived})"
