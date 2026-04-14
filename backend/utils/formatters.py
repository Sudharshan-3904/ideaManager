from datetime import datetime

def format_date(dt):
    """Formats a datetime object as a string."""
    if isinstance(dt, datetime):
        return dt.strftime('%Y-%m-%d %H:%M')
    return dt

def truncate_text(text, limit=100):
    """Truncates text to a certain length with an ellipsis."""
    if len(text) > limit:
        return text[:limit] + "..."
    return text
