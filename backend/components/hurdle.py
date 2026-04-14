from datetime import datetime

class Hurdle:
    def __init__(self, date=None, main_setback="", description="", leads=None):
        self.date = date if date else datetime.now()
        self.main_setback = main_setback
        self.description = description
        self.leads = leads if leads is not None else []

    @classmethod
    def loadFromStr(cls, hurdle_str):
        """
        Parses a hurdle from a string formatted as 'date|main_setback|description|leads'.
        Uses '|' as a separator instead of ',' to avoid CSV conflicts.
        Leads are separated by '::'.
        """
        if not hurdle_str:
            return None
        try:
            parts = hurdle_str.split('|')
            if len(parts) >= 3:
                date_obj = datetime.strptime(parts[0], '%Y-%m-%d %H:%M:%S')
                leads = []
                if len(parts) > 3 and parts[3]:
                    leads = parts[3].split('::')
                return cls(date=date_obj, main_setback=parts[1], description=parts[2], leads=leads)
        except Exception as e:
            print(f"Error parsing hurdle string: {hurdle_str} -> {e}")
        return None

    def serialize(self):
        """Serializes the hurdle to a string for storage."""
        date_str = self.date.strftime('%Y-%m-%d %H:%M:%S')
        leads_str = "::".join(self.leads)
        return f"{date_str}|{self.main_setback}|{self.description}|{leads_str}"

    def __repr__(self):
        return f"Hurdle({self.date.strftime('%Y-%m-%d')}, {self.main_setback}, {len(self.leads)} leads)"
