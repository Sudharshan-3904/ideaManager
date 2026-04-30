import sqlite3
import json
from datetime import datetime

class DBHandler:
    """
    Main database interface for the Idea Manager.
    Handles SQLite connection management, table creation, and CRUD operations.
    """
    def __init__(self, db_path):
        self.db_path = db_path
        self._create_tables()

    def _get_connection(self):
        """Creates and returns a SQLite connection with Row factory enabled."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _create_tables(self):
        """Initializes the database schema if it doesn't already exist."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Enforce referential integrity
        cursor.execute("PRAGMA foreign_keys = ON;")

        # Ideas Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ideas (
                id TEXT PRIMARY KEY,
                title TEXT,
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
                idea_id TEXT,
                main_setback TEXT NOT NULL,
                description TEXT,
                date TEXT,
                FOREIGN KEY (idea_id) REFERENCES ideas (id) ON DELETE CASCADE
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
                idea_id TEXT,
                note TEXT NOT NULL,
                FOREIGN KEY (idea_id) REFERENCES ideas (id) ON DELETE CASCADE
            )
        ''')

        # Tags Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS idea_tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                idea_id TEXT,
                tag TEXT NOT NULL,
                FOREIGN KEY (idea_id) REFERENCES ideas (id) ON DELETE CASCADE
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
                idea_id TEXT,
                username TEXT,
                role TEXT,
                PRIMARY KEY (idea_id, username),
                FOREIGN KEY (idea_id) REFERENCES ideas (id) ON DELETE CASCADE,
                FOREIGN KEY (username) REFERENCES users (username) ON DELETE CASCADE
            )
        ''')

        # Idea Activities Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS idea_activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                idea_id TEXT,
                username TEXT,
                action TEXT,
                details TEXT,
                created_at TEXT,
                FOREIGN KEY (idea_id) REFERENCES ideas (id) ON DELETE CASCADE
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
                related_idea_id TEXT,
                created_at TEXT,
                FOREIGN KEY (username) REFERENCES users (username) ON DELETE CASCADE,
                FOREIGN KEY (related_idea_id) REFERENCES ideas (id) ON DELETE CASCADE
            )
        ''')

        # Idea Embeddings Table (Semantic Search)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS idea_embeddings (
                idea_id TEXT PRIMARY KEY,
                embedding_json TEXT,
                updated_at TEXT,
                FOREIGN KEY (idea_id) REFERENCES ideas (id) ON DELETE CASCADE
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
        """Fetches a single row from the database and returns it as a dict."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    # --- Idea-Specific Operations ---
    def read_all_ideas(self, username=None):
        # Fetch basic idea info
        if username:
            query = """
                SELECT i.* FROM ideas i
                JOIN idea_roles r ON i.id = r.idea_id
                WHERE r.username = ?
            """
            ideas_rows = self.fetchall(query, (username,))
        else:
            ideas_rows = self.fetchall("SELECT * FROM ideas")
            
        results = []
        
        for row in ideas_rows:
            idea_id = row['id']
            # Fetch related data
            hurdles = self.fetchall("SELECT * FROM hurdles WHERE idea_id = ?", (idea_id,))
            for h in hurdles:
                leads = self.fetchall("SELECT lead FROM hurdle_leads WHERE hurdle_id = ?", (h['id'],))
                h['leads'] = [l['lead'] for l in leads]
            
            notes = self.fetchall("SELECT note FROM idea_notes WHERE idea_id = ?", (idea_id,))
            tags = self.fetchall("SELECT tag FROM idea_tags WHERE idea_id = ?", (idea_id,))
            
            idea_data = dict(row)
            idea_data['hurdles'] = hurdles
            idea_data['notes'] = [n['note'] for n in notes]
            idea_data['tags'] = [t['tag'] for t in tags]
            results.append(idea_data)
            
        return results

    def save_idea(self, idea_dict):
        """
        Saves or updates an idea and its related entities (hurdles, notes, tags) in a single transaction.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            # Start transaction to ensure data integrity
            cursor.execute("BEGIN TRANSACTION;")
            
            # Insert or Replace base idea
            cursor.execute('''
                INSERT OR REPLACE INTO ideas (id, title, description, explanation, architecture, status, is_archived, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                idea_dict['id'],
                idea_dict.get('title', ''),
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
                    INSERT OR IGNORE INTO idea_roles (idea_id, username, role)
                    VALUES (?, ?, 'Owner')
                ''', (idea_dict['id'], username))

            # Clear and re-add related data
            cursor.execute("DELETE FROM hurdles WHERE idea_id = ?", (idea_dict['id'],))
            cursor.execute("DELETE FROM idea_notes WHERE idea_id = ?", (idea_dict['id'],))
            cursor.execute("DELETE FROM idea_tags WHERE idea_id = ?", (idea_dict['id'],))

            for hurdle in idea_dict.get('hurdles', []):
                cursor.execute('''
                    INSERT INTO hurdles (idea_id, main_setback, description, date)
                    VALUES (?, ?, ?, ?)
                ''', (idea_dict['id'], hurdle['main_setback'], hurdle.get('description', ''), hurdle.get('date', '')))
                
                hurdle_id = cursor.lastrowid
                for lead in hurdle.get('leads', []):
                    cursor.execute("INSERT INTO hurdle_leads (hurdle_id, lead) VALUES (?, ?)", (hurdle_id, lead))

            for note in idea_dict.get('notes', []):
                cursor.execute("INSERT INTO idea_notes (idea_id, note) VALUES (?, ?)", (idea_dict['id'], note))

            for tag in idea_dict.get('tags', []):
                cursor.execute("INSERT INTO idea_tags (idea_id, tag) VALUES (?, ?)", (idea_dict['id'], tag))

            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def delete_idea(self, idea_id):
        self.execute("DELETE FROM ideas WHERE id = ?", (idea_id,))

    def log_activity(self, idea_id, username, action, details=""):
        self.execute('''
            INSERT INTO idea_activities (idea_id, username, action, details, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (idea_id, username, action, details, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    def get_activities(self, idea_id):
        return self.fetchall("SELECT * FROM idea_activities WHERE idea_id = ? ORDER BY created_at DESC", (idea_id,))

    def log_audit(self, table_name, record_id, action, username, details=""):
        self.execute('''
            INSERT INTO audit_logs (table_name, record_id, action, username, details, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (table_name, record_id, action, username, details, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    def add_notification(self, username, message, related_idea_id=""):
        self.execute('''
            INSERT INTO notifications (username, message, related_idea_id, created_at)
            VALUES (?, ?, ?, ?)
        ''', (username, message, related_idea_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    def get_notifications(self, username):
        return self.fetchall("SELECT * FROM notifications WHERE username = ? ORDER BY created_at DESC", (username,))

    def mark_notification_read(self, notification_id, username):
        self.execute("UPDATE notifications SET is_read = 1 WHERE id = ? AND username = ?", (notification_id, username))
        
    def share_idea(self, idea_id, owner_username, target_username, role):
        # Validate target user exists
        user = self.fetchone("SELECT * FROM users WHERE username = ?", (target_username,))
        if not user:
            return False, "Target user not found"
            
        # Optional: check if sharing user is Owner
        is_owner = self.fetchone("SELECT 1 FROM idea_roles WHERE idea_id = ? AND username = ? AND role = 'Owner'", (idea_id, owner_username))
        if not is_owner:
            return False, "Only Owner can share the idea"
            
        self.execute('''
            INSERT OR REPLACE INTO idea_roles (idea_id, username, role)
            VALUES (?, ?, ?)
        ''', (idea_id, target_username, role))
        
        self.add_notification(target_username, f"'{owner_username}' shared an idea with you as {role}.", idea_id)
        self.log_activity(idea_id, owner_username, "Shared", f"Shared with {target_username} as {role}")
        self.log_audit("idea_roles", f"{idea_id}_{target_username}", "GRANT", owner_username, f"Role: {role}")
        return True, "Idea shared successfully"

    def save_embedding(self, idea_id, embedding):
        self.execute('''
            INSERT OR REPLACE INTO idea_embeddings (idea_id, embedding_json, updated_at)
            VALUES (?, ?, ?)
        ''', (idea_id, json.dumps(embedding), datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    def get_all_embeddings(self):
        return self.fetchall("SELECT * FROM idea_embeddings")