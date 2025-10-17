# 🏃 Orienteering Tables

A complete PySide6 desktop application for managing orienteering competitions and tracking teams.

![Application Screenshot](https://github.com/user-attachments/assets/4094852a-3ea9-438c-acf5-1f7954835cbc)

## 🎯 Overview

Orienteering Tables is a desktop application built with PySide6 that allows users to create, view, and manage orienteering competitions and their teams. Each competition has metadata (date, location, categories, ideal times) and a list of teams with detailed member information.

## ✨ Features

- **SQLite Database** - Live database connection with immediate UI updates
- **Competition Management** - Create and view competitions with full details
- **Team Management** - Create and view teams with comprehensive member tracking
- **Typeform-style Wizards** - Intuitive step-by-step forms for data entry
- **Clean Modern UI** - Built with PySide6 (Qt for Python)
- **Grid Layout** - Visual tile-based competition overview
- **Dashboard View** - Detailed competition information with team listing
- **Category Support** - Categories A through O with conditional fields
- **Member Demographics** - Track women, children, and elderly counts
- **Conditional Fields** - Context-aware forms based on category selection

## 📋 Requirements

- Python 3.x
- PySide6 >= 6.0.0

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/thezanrutar/orienteering-tables.git
cd orienteering-tables
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## 💻 Usage

Run the application:
```bash
python src/main.py
```

Or alternatively:
```bash
cd src
python main.py
```

## 🏗️ Application Structure

```
orienteering-tables/
├── src/
│   ├── main.py              # Entry point
│   ├── app.py               # Application setup
│   ├── main_window.py       # Competition grid view (main screen)
│   ├── competition_form.py  # Typeform-style wizard for adding competitions
│   ├── dashboard.py         # Competition dashboard (details, team list)
│   ├── team_form.py         # Typeform-style wizard for adding teams
│   ├── database.py          # SQLite connection, schema, CRUD operations
│   └── models.py            # Data models and constants
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 📊 Database Schema

### Competitions Table
| Field       | Type    | Description                                    |
|-------------|---------|------------------------------------------------|
| id          | INTEGER | Primary key                                    |
| date        | TEXT    | Competition date (YYYY-MM-DD)                  |
| location    | TEXT    | Location (e.g., "Oslo, Norway")                |
| categories  | TEXT    | Comma-separated categories (e.g., "A,B,C,D")   |
| ideal_times | TEXT    | JSON object mapping category to ideal time     |

### Teams Table
| Field          | Type    | Description                           |
|----------------|---------|---------------------------------------|
| id             | INTEGER | Primary key                           |
| competition_id | INTEGER | Foreign key to competitions           |
| category       | TEXT    | Team category (A-O)                   |
| name           | TEXT    | Team name                             |
| members_count  | INTEGER | Total number of members               |
| women_count    | INTEGER | Number of women                       |
| children_count | INTEGER | Number of children                    |
| elderly_count  | INTEGER | Number of elderly                     |
| leader_name    | TEXT    | Team leader's name                    |
| member_names   | TEXT    | JSON array of all member names        |
| phone          | TEXT    | Phone number (nullable)               |

## 🎮 User Workflow

1. **Launch Application** → View all competitions in a grid layout
2. **Click "+" Tile** → Create new competition via step-by-step wizard
   - Enter date
   - Enter location
   - Select categories (A-O)
   - Set ideal time for each category
3. **Click Competition Tile** → Open dashboard with details and team list
4. **Click "+ Add Team"** → Create new team via step-by-step wizard
   - Select category
   - Enter team name
   - Enter member counts
   - Enter member names
   - Enter phone (for categories A and B only)
5. **View Teams** → See all teams in a table with their details

## 🎨 UI Components

### Main Window
- Grid layout showing competition tiles
- Each tile displays: date, location, team count
- "+ New Competition" tile at the end
- Clicking a tile opens the dashboard

### Competition Form (Wizard)
- Step 1: Date selection (calendar picker)
- Step 2: Location input
- Step 3: Category selection (checkboxes)
- Step 4+: Ideal time for each selected category
- Navigation: Back and Next buttons

### Dashboard
- Competition details at the top
- Table showing all teams with:
  - Team name
  - Category
  - Member counts (total, women, children, elderly)
  - Leader name
- "+ Add Team" button
- Back button to return to main view

### Team Form (Wizard)
- Step 1: Category selection
- Step 2: Team name
- Step 3: Total members count
- Step 4: Women count
- Step 5: Children count
- Step 6: Elderly count (only for categories D, E, F, O)
- Step 7+: Individual member names (first one is leader)
- Final step: Phone number (only for categories A and B)

## 🔧 Development

### Database Operations

The `database.py` module provides the following functions:

- `init_db()` - Initialize database schema
- `insert_competition(...)` - Create a new competition
- `insert_team(...)` - Create a new team
- `get_competitions()` - Retrieve all competitions
- `get_competition_by_id(id)` - Get specific competition
- `get_teams_by_competition(id)` - Get teams for a competition
- `get_team_count_by_competition(id)` - Count teams in competition

### Adding New Features

The application follows a modular architecture:

1. **Database Layer** (`database.py`) - All database operations
2. **Model Layer** (`models.py`) - Data structures and constants
3. **UI Layer** - Individual widgets for each screen
4. **Main Window** - Orchestrates navigation between screens

## 📝 Notes

- Database file `orienteering.db` is created automatically in the project root
- All UI updates are immediate (no restart required)
- Forms include validation for required fields
- Member counts cannot exceed total member count
- Phone number is optional and only requested for categories A and B
- Elderly count is only requested for categories D, E, F, and O

## 🐛 Troubleshooting

**Application won't start:**
- Ensure PySide6 is installed: `pip install PySide6`
- Check Python version: `python --version` (3.x required)

**Database errors:**
- Delete `orienteering.db` and restart the application
- The database will be recreated automatically

**Import errors:**
- Run from the correct directory: `python src/main.py`
- Or add the src directory to your PYTHONPATH

## 📄 License

This project is open source and available for educational and personal use.

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues and pull requests.

## 👨‍💻 Author

Built as a demonstration of PySide6 desktop application development.
