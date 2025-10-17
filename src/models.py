"""
Data models for the orienteering application.
"""

class Competition:
    """Represents an orienteering competition."""
    
    def __init__(self, id=None, date='', location='', categories=None, ideal_times=None):
        self.id = id
        self.date = date
        self.location = location
        self.categories = categories or []
        self.ideal_times = ideal_times or {}
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'date': self.date,
            'location': self.location,
            'categories': self.categories,
            'ideal_times': self.ideal_times
        }
    
    @staticmethod
    def from_dict(data):
        """Create Competition from dictionary."""
        return Competition(
            id=data.get('id'),
            date=data.get('date', ''),
            location=data.get('location', ''),
            categories=data.get('categories', []),
            ideal_times=data.get('ideal_times', {})
        )

class Team:
    """Represents an orienteering team."""
    
    def __init__(self, id=None, competition_id=None, category='', name='', 
                 members_count=0, women_count=0, children_count=0, elderly_count=0,
                 leader_name='', member_names=None, phone=None):
        self.id = id
        self.competition_id = competition_id
        self.category = category
        self.name = name
        self.members_count = members_count
        self.women_count = women_count
        self.children_count = children_count
        self.elderly_count = elderly_count
        self.leader_name = leader_name
        self.member_names = member_names or []
        self.phone = phone
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'competition_id': self.competition_id,
            'category': self.category,
            'name': self.name,
            'members_count': self.members_count,
            'women_count': self.women_count,
            'children_count': self.children_count,
            'elderly_count': self.elderly_count,
            'leader_name': self.leader_name,
            'member_names': self.member_names,
            'phone': self.phone
        }
    
    @staticmethod
    def from_dict(data):
        """Create Team from dictionary."""
        return Team(
            id=data.get('id'),
            competition_id=data.get('competition_id'),
            category=data.get('category', ''),
            name=data.get('name', ''),
            members_count=data.get('members_count', 0),
            women_count=data.get('women_count', 0),
            children_count=data.get('children_count', 0),
            elderly_count=data.get('elderly_count', 0),
            leader_name=data.get('leader_name', ''),
            member_names=data.get('member_names', []),
            phone=data.get('phone')
        )

# Available categories
CATEGORIES = ['A', 'B', 'C', 'D', 'E', 'F', 'O']
