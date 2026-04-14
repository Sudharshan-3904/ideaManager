from components.hurdle import Hurdle

class Idea:
    def __init__(self, title="", description="", target_customers="", minimal_deliverables="", future_extensions="", hurdles=None):
        self.title = title
        self.description = description
        self.target_customers = target_customers
        self.minimal_deliverables = minimal_deliverables
        self.future_extensions = future_extensions
        self.hurdles = hurdles if hurdles is not None else []

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
            # Assuming hurdles are separated by ';;' in the CSV string
            hurdle_strings = hurdles_str.split(';;')
            for h_str in hurdle_strings:
                h = Hurdle.loadFromStr(h_str)
                if h:
                    hurdles.append(h)
        
        return cls(
            title=data.get('title', ""),
            description=data.get('description', ""),
            target_customers=data.get('target_customers', ""),
            minimal_deliverables=data.get('minimal_deliverables', ""),
            future_extensions=data.get('future_extensions', ""),
            hurdles=hurdles
        )

    def to_dict(self):
        """Serializes the Idea instance to a dictionary for CSV storage."""
        hurdles_str = ";;".join([h.serialize() for h in self.hurdles])
        return {
            'title': self.title,
            'description': self.description,
            'target_customers': self.target_customers,
            'minimal_deliverables': self.minimal_deliverables,
            'future_extensions': self.future_extensions,
            'hurdles': hurdles_str
        }

    def __repr__(self):
        return f"Idea('{self.title}', {len(self.hurdles)} hurdles)"
