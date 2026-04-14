from components.hurdle import Hurdle

class Idea:
    def __init__(self, title="", description="", target_customers="", minimal_deliverables="", future_extensions="", hurdles=None, notes=None):
        self.title = title
        self.description = description
        self.target_customers = target_customers
        self.minimal_deliverables = minimal_deliverables
        self.future_extensions = future_extensions
        self.hurdles = hurdles if hurdles is not None else []
        self.notes = notes if notes is not None else []

    def add_hurdle(self, hurdle):
        if isinstance(hurdle, Hurdle):
            self.hurdles.append(hurdle)
        else:
            raise ValueError("Object must be an instance of Hurdle")

    @classmethod
    def from_dict(cls, data):
        """Creates an Idea instance from a dictionary (e.g., a CSV row)."""
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
        
        return cls(
            title=data.get('title', ""),
            description=data.get('description', ""),
            target_customers=data.get('target_customers', ""),
            minimal_deliverables=data.get('minimal_deliverables', ""),
            future_extensions=data.get('future_extensions', ""),
            hurdles=hurdles,
            notes=notes
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
            'notes': self.notes
        }

    def to_csv_dict(self):
        """Serializes the Idea instance to a dictionary for CSV storage."""
        hurdles_str = ";;".join([h.serialize() for h in self.hurdles])
        notes_str = ";;".join(self.notes)
        return {
            'title': self.title,
            'description': self.description,
            'target_customers': self.target_customers,
            'minimal_deliverables': self.minimal_deliverables,
            'future_extensions': self.future_extensions,
            'hurdles': hurdles_str,
            'notes': notes_str
        }

    def __repr__(self):
        return f"Idea('{self.title}', {len(self.hurdles)} hurdles, {len(self.notes)} notes)"
