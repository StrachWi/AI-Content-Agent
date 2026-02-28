import sqlite3

def add_columns_to_history():
    db_path = 'sql_app.db'
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("PRAGMA table_info(histories)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'template_name' not in columns:
            cursor.execute("ALTER TABLE histories ADD COLUMN template_name VARCHAR(100)")
            print("Added template_name column")
        else:
            print("template_name column already exists")
        
        if 'topic' not in columns:
            cursor.execute("ALTER TABLE histories ADD COLUMN topic VARCHAR(200)")
            print("Added topic column")
        else:
            print("topic column already exists")
        
        if 'platform' not in columns:
            cursor.execute("ALTER TABLE histories ADD COLUMN platform VARCHAR(50)")
            print("Added platform column")
        else:
            print("platform column already exists")
        
        conn.commit()
        conn.close()
        print("Database schema updated successfully!")
        
    except Exception as e:
        print(f"Error updating database schema: {e}")

if __name__ == "__main__":
    add_columns_to_history()