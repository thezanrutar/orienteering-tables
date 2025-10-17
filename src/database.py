import sqlite3
import json
import os

# Database path
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'orienteering.db')

# Connection holder
_connection = None

def get_connection():
    """Get or create database connection."""
    global _connection
    if _connection is None:
        _connection = sqlite3.connect(DB_PATH)
        _connection.row_factory = sqlite3.Row
    return _connection

def init_db():
    """Initialize database schema."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create competitions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS competitions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            location TEXT NOT NULL,
            categories TEXT NOT NULL,
            ideal_times TEXT NOT NULL
        )
    ''')
    
    # Create teams table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            competition_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            name TEXT NOT NULL,
            members_count INTEGER NOT NULL,
            women_count INTEGER NOT NULL,
            children_count INTEGER NOT NULL,
            elderly_count INTEGER NOT NULL,
            leader_name TEXT NOT NULL,
            member_names TEXT NOT NULL,
            phone TEXT,
            FOREIGN KEY (competition_id) REFERENCES competitions(id) ON DELETE CASCADE
        )
    ''')
    
    conn.commit()
    print("Database initialized successfully")

def insert_competition(date, location, categories, ideal_times):
    """Insert a new competition into the database.
    
    Args:
        date: str - Competition date in YYYY-MM-DD format
        location: str - Competition location
        categories: list - List of selected categories
        ideal_times: dict - Dictionary mapping category to ideal time
    
    Returns:
        int - ID of the inserted competition
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    categories_str = ','.join(categories)
    ideal_times_str = json.dumps(ideal_times)
    
    cursor.execute('''
        INSERT INTO competitions (date, location, categories, ideal_times)
        VALUES (?, ?, ?, ?)
    ''', (date, location, categories_str, ideal_times_str))
    
    conn.commit()
    competition_id = cursor.lastrowid
    print(f"Competition inserted with ID: {competition_id}")
    return competition_id

def insert_team(competition_id, category, name, members_count, women_count, 
                children_count, elderly_count, leader_name, member_names, phone=None):
    """Insert a new team into the database.
    
    Args:
        competition_id: int - ID of the competition
        category: str - Team category
        name: str - Team name
        members_count: int - Total number of members
        women_count: int - Number of women
        children_count: int - Number of children
        elderly_count: int - Number of elderly
        leader_name: str - Name of team leader
        member_names: list - List of all member names
        phone: str - Phone number (optional)
    
    Returns:
        int - ID of the inserted team
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    member_names_str = json.dumps(member_names)
    
    cursor.execute('''
        INSERT INTO teams (competition_id, category, name, members_count, 
                          women_count, children_count, elderly_count, 
                          leader_name, member_names, phone)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (competition_id, category, name, members_count, women_count, 
          children_count, elderly_count, leader_name, member_names_str, phone))
    
    conn.commit()
    team_id = cursor.lastrowid
    print(f"Team inserted with ID: {team_id}")
    return team_id

def get_competitions():
    """Get all competitions from the database.
    
    Returns:
        list - List of competition dictionaries
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM competitions ORDER BY date DESC')
    rows = cursor.fetchall()
    
    competitions = []
    for row in rows:
        comp = {
            'id': row['id'],
            'date': row['date'],
            'location': row['location'],
            'categories': row['categories'].split(','),
            'ideal_times': json.loads(row['ideal_times'])
        }
        competitions.append(comp)
    
    return competitions

def get_competition_by_id(competition_id):
    """Get a specific competition by ID.
    
    Args:
        competition_id: int - ID of the competition
    
    Returns:
        dict - Competition data or None if not found
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM competitions WHERE id = ?', (competition_id,))
    row = cursor.fetchone()
    
    if row:
        return {
            'id': row['id'],
            'date': row['date'],
            'location': row['location'],
            'categories': row['categories'].split(','),
            'ideal_times': json.loads(row['ideal_times'])
        }
    return None

def get_teams_by_competition(competition_id):
    """Get all teams for a specific competition.
    
    Args:
        competition_id: int - ID of the competition
    
    Returns:
        list - List of team dictionaries
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM teams 
        WHERE competition_id = ? 
        ORDER BY category, name
    ''', (competition_id,))
    rows = cursor.fetchall()
    
    teams = []
    for row in rows:
        team = {
            'id': row['id'],
            'competition_id': row['competition_id'],
            'category': row['category'],
            'name': row['name'],
            'members_count': row['members_count'],
            'women_count': row['women_count'],
            'children_count': row['children_count'],
            'elderly_count': row['elderly_count'],
            'leader_name': row['leader_name'],
            'member_names': json.loads(row['member_names']),
            'phone': row['phone']
        }
        teams.append(team)
    
    return teams

def get_team_count_by_competition(competition_id):
    """Get the number of teams in a competition.
    
    Args:
        competition_id: int - ID of the competition
    
    Returns:
        int - Number of teams
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) as count FROM teams WHERE competition_id = ?', 
                   (competition_id,))
    row = cursor.fetchone()
    return row['count'] if row else 0

def close_connection():
    """Close the database connection."""
    global _connection
    if _connection:
        _connection.close()
        _connection = None
        print("Database connection closed")
