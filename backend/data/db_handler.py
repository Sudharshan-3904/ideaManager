import sqlite3
import json
from datetime import datetime

class DBHandler:
    def __init__(self, db_path):
        self.db_path = db_path
        self.create_tables()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def create_tables(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Enable Foreign Keys
        cursor.execute("PRAGMA foreign_keys = ON;")

        # Ideas Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ideas (
                title TEXT PRIMARY KEY,
                description TEXT,
                explanation TEXT,
                architecture TEXT,
                status TEXT DEFAULT 'Yet to Start',
                is_archived INTEGER DEFAULT 0,
                created_at TEXT
            )
        ''')

        # Hurdles Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS hurdles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                idea_title TEXT,
                main_setback TEXT NOT NULL,
                description TEXT,
                date TEXT,
                FOREIGN KEY (idea_title) REFERENCES ideas (title) ON DELETE CASCADE
            )
        ''')

        # Hurdle Leads
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS hurdle_leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hurdle_id INTEGER,
                lead TEXT NOT NULL,
                FOREIGN KEY (hurdle_id) REFERENCES hurdles (id) ON DELETE CASCADE
            )
        ''')

        # Notes Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS idea_notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                idea_title TEXT,
                note TEXT NOT NULL,
                FOREIGN KEY (idea_title) REFERENCES ideas (title) ON DELETE CASCADE
            )
        ''')

        # Tags Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS idea_tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                idea_title TEXT,
                tag TEXT NOT NULL,
                FOREIGN KEY (idea_title) REFERENCES ideas (title) ON DELETE CASCADE
            )
        ''')

        # Users Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        ''')

        # Idea Roles Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS idea_roles (
                idea_title TEXT,
                username TEXT,
                role TEXT,
                PRIMARY KEY (idea_title, username),
                FOREIGN KEY (idea_title) REFERENCES ideas (title) ON DELETE CASCADE,
                FOREIGN KEY (username) REFERENCES users (username) ON DELETE CASCADE
            )
        ''')

        # Idea Activities Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS idea_activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                idea_title TEXT,
                username TEXT,
                action TEXT,
                details TEXT,
                created_at TEXT,
                FOREIGN KEY (idea_title) REFERENCES ideas (title) ON DELETE CASCADE
            )
        ''')

        # Audit Logs Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                table_name TEXT,
                record_id TEXT,
                action TEXT,
                username TEXT,
                details TEXT,
                timestamp TEXT
            )
        ''')

        # Notifications Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                message TEXT,
                is_read INTEGER DEFAULT 0,
                related_idea TEXT,
                created_at TEXT,
                FOREIGN KEY (username) REFERENCES users (username) ON DELETE CASCADE
            )
        ''')

        # Idea Embeddings Table (Semantic Search)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS idea_embeddings (
                idea_title TEXT PRIMARY KEY,
                embedding_json TEXT,
                updated_at TEXT,
                FOREIGN KEY (idea_title) REFERENCES ideas (title) ON DELETE CASCADE
            )
        ''')

        conn.commit()
        conn.close()

    def execute(self, query, params=()):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        conn.close()

    def fetchall(self, query, params=()):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return rows

    def fetchone(self, query, params=()):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    # High-level methods for IdeaRepository
    def read_all_ideas(self, username=None):
        # Fetch basic idea info
        if username:
            query = """
                SELECT i.* FROM ideas i
                JOIN idea_roles r ON i.title = r.idea_title
                WHERE r.username = ?
            """
            ideas_rows = self.fetchall(query, (username,))
        else:
            ideas_rows = self.fetchall("SELECT * FROM ideas")
            
        results = []
        
        for row in ideas_rows:
            title = row['title']
            # Fetch related data
            hurdles = self.fetchall("SELECT * FROM hurdles WHERE idea_title = ?", (title,))
            for h in hurdles:
                leads = self.fetchall("SELECT lead FROM hurdle_leads WHERE hurdle_id = ?", (h['id'],))
                h['leads'] = [l['lead'] for l in leads]
            
            notes = self.fetchall("SELECT note FROM idea_notes WHERE idea_title = ?", (title,))
            tags = self.fetchall("SELECT tag FROM idea_tags WHERE idea_title = ?", (title,))
            
            idea_data = dict(row)
            idea_data['hurdles'] = hurdles
            idea_data['notes'] = [n['note'] for n in notes]
            idea_data['tags'] = [t['tag'] for t in tags]
            results.append(idea_data)
            
        return results

    def save_idea(self, idea_dict):
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            # Delete existing related records first (if update)
            # Or just use the cascade + delete idea if title changed, but usually we just update
            # For simplicity in this personal tool, we use a single transactional save per idea
            
            # Start transaction
            cursor.execute("BEGIN TRANSACTION;")
            
            # Insert or Replace base idea
            cursor.execute('''
                INSERT OR REPLACE INTO ideas (title, description, explanation, architecture, status, is_archived, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                idea_dict['title'],
                idea_dict.get('description', ''),
                idea_dict.get('explanation', ''),
                json.dumps(idea_dict.get('architecture', {"nodes": [], "edges": []})),
                idea_dict.get('status', 'Yet to Start'),
                1 if idea_dict.get('is_archived', False) else 0,
                idea_dict.get('created_at', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            ))
            
            username = idea_dict.get('owner_username')
            if username:
                # Ensure owner role exists
                cursor.execute('''
                    INSERT OR IGNORE INTO idea_roles (idea_title, username, role)
                    VALUES (?, ?, 'Owner')
                ''', (idea_dict['title'], username))

            # Clear and re-add related data
            cursor.execute("DELETE FROM hurdles WHERE idea_title = ?", (idea_dict['title'],))
            cursor.execute("DELETE FROM idea_notes WHERE idea_title = ?", (idea_dict['title'],))
            cursor.execute("DELETE FROM idea_tags WHERE idea_title = ?", (idea_dict['title'],))

            for hurdle in idea_dict.get('hurdles', []):
                cursor.execute('''
                    INSERT INTO hurdles (idea_title, main_setback, description, date)
                    VALUES (?, ?, ?, ?)
                ''', (idea_dict['title'], hurdle['main_setback'], hurdle.get('description', ''), hurdle.get('date', '')))
                
                hurdle_id = cursor.lastrowid
                for lead in hurdle.get('leads', []):
                    cursor.execute("INSERT INTO hurdle_leads (hurdle_id, lead) VALUES (?, ?)", (hurdle_id, lead))

            for note in idea_dict.get('notes', []):
                cursor.execute("INSERT INTO idea_notes (idea_title, note) VALUES (?, ?)", (idea_dict['title'], note))

            for tag in idea_dict.get('tags', []):
                cursor.execute("INSERT INTO idea_tags (idea_title, tag) VALUES (?, ?)", (idea_dict['title'], tag))

            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def delete_idea(self, title):
        self.execute("DELETE FROM ideas WHERE title = ?", (title,))

    def log_activity(self, idea_title, username, action, details=""):
        self.execute('''
            INSERT INTO idea_activities (idea_title, username, action, details, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (idea_title, username, action, details, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    def get_activities(self, idea_title):
        return self.fetchall("SELECT * FROM idea_activities WHERE idea_title = ? ORDER BY created_at DESC", (idea_title,))

    def log_audit(self, table_name, record_id, action, username, details=""):
        self.execute('''
            INSERT INTO audit_logs (table_name, record_id, action, username, details, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (table_name, record_id, action, username, details, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    def add_notification(self, username, message, related_idea=""):
        self.execute('''
            INSERT INTO notifications (username, message, related_idea, created_at)
            VALUES (?, ?, ?, ?)
        ''', (username, message, related_idea, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    def get_notifications(self, username):
        return self.fetchall("SELECT * FROM notifications WHERE username = ? ORDER BY created_at DESC", (username,))

    def mark_notification_read(self, notification_id, username):
        self.execute("UPDATE notifications SET is_read = 1 WHERE id = ? AND username = ?", (notification_id, username))
        
    def share_idea(self, idea_title, owner_username, target_username, role):
        # Validate target user exists
        user = self.fetchone("SELECT * FROM users WHERE username = ?", (target_username,))
        if not user:
            return False, "Target user not found"
            
        # Optional: check if sharing user is Owner
        is_owner = self.fetchone("SELECT 1 FROM idea_roles WHERE idea_title = ? AND username = ? AND role = 'Owner'", (idea_title, owner_username))
        if not is_owner:
            return False, "Only Owner can share the idea"
            
        self.execute('''
            INSERT OR REPLACE INTO idea_roles (idea_title, username, role)
            VALUES (?, ?, ?)
        ''', (idea_title, target_username, role))
        
        self.add_notification(target_username, f"'{owner_username}' shared idea '{idea_title}' with you as {role}.", idea_title)
        self.log_activity(idea_title, owner_username, "Shared", f"Shared with {target_username} as {role}")
        self.log_audit("idea_roles", f"{idea_title}_{target_username}", "GRANT", owner_username, f"Role: {role}")
        return True, "Idea shared successfully"

    def save_embedding(self, title, embedding):
        self.execute('''
            INSERT OR REPLACE INTO idea_embeddings (idea_title, embedding_json, updated_at)
            VALUES (?, ?, ?)
        ''', (title, json.dumps(embedding), datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    def get_all_embeddings(self):
        return self.fetchall("SELECT * FROM idea_embeddings")