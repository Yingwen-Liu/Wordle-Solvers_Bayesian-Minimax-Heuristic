import sqlite3

class TreeDB:
    """A decision tree using SQLite for storage"""
    def __init__(self, name, path='tree.db'):
        self.name = name
        self.id = 0

        self.conn = sqlite3.connect(path)
        self.c = self.conn.cursor()

        # Create the main table if it doesn't exist
        self.c.execute(f'''
        CREATE TABLE IF NOT EXISTS "{self.name}" (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            feedback TEXT,
            guess TEXT,
            pid INTEGER,
            FOREIGN KEY (pid) REFERENCES "{self.name}"(id)
        );
        ''')
        self.conn.commit()
    
    def get_node(self, make_guess, feedback):
        if feedback:
            # Convert feedback to a string for easier querying
            feedback = ''.join(map(str, feedback))
            self.c.execute(f'SELECT id, guess FROM "{self.name}" WHERE pid = ? AND feedback = ?', (self.id, feedback))
        else:
            # If no feedback, we are at the root node
            self.c.execute(f'SELECT id, guess FROM "{self.name}" WHERE id = 1')

        if result := self.c.fetchone():
            # If a result is found, update the id and return the guess
            self.id = result[0]
            return result[1]

        # If no result is found, insert the new guess into the database        
        guess = make_guess()

        self.c.execute(f'INSERT INTO "{self.name}" (feedback, guess, pid) VALUES (?, ?, ?)', (feedback, guess, self.id))
        self.conn.commit()

        self.id = self.c.lastrowid

        return guess
    
    def close(self):
        # Close the database connection
        self.conn.close()

