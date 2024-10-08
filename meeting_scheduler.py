from typing import List, Tuple
import numpy as np
class TeamMember:
   def __init__(self, name: str, availability: List[Tuple[int, int]], state: str, seniority: int):
       self.name = name
       self.availability = availability
       self.state = state
       self.seniority = seniority
  
   def getName(self) -> str:
       """Return the name of the team member."""
       return self.name


   def getAvailability(self) -> List[Tuple[int, int]]:
       """Return the availability of the team member."""
       return self.availability


   def getState(self) -> str:
       """Return the state of the team member."""
       return self.state


   def getSeniority(self) -> int:
       """Return the seniority of the team member, which is based on seniority."""
       return self.seniority


   def __repr__(self) -> str:
       return (f"TeamMember(name={self.name}, "
               f"availability={self.availability}, "
               f"state={self.state}, "
               f"seniority={self.seniority})")

class Scheduler:
    state_time_zones = {
        "AL": "Central",
        "AK": "Pacific", 
        "AZ": "Pacific", 
        "AR": "Mountain",
        "CA": "Pacific",
        "CO": "Mountain", 
        "CT": "Eastern",
        "DE": "Eastern",
        "FL": "Eastern",
        "GA": "Eastern",
        "HI": "Pacific", 
        "ID": "Mountain",  
        "IL": "Central",
        "IN": "Eastern",  
        "IA": "Central",
        "KS": "Central",
        "KY": "Eastern", 
        "LA": "Central",
        "ME": "Eastern",
        "MD": "Eastern",
        "MA": "Eastern",
        "MI": "Eastern", 
        "MN": "Central",
        "MS": "Central",
        "MO": "Central",
        "MT": "Mountain",  
        "NE": "Central",  
        "NV": "Pacific",
        "NH": "Eastern",
        "NJ": "Eastern",
        "NM": "Mountain", 
        "NY": "Eastern",
        "NC": "Eastern",
        "ND": "Central",
        "OH": "Eastern",
        "OK": "Central",
        "OR": "Pacific",
        "PA": "Eastern",
        "RI": "Eastern",
        "SC": "Eastern",
        "SD": "Central",
        "TN": "Central",
        "TX": "Central",
        "UT": "Mountain", 
        "VT": "Eastern",
        "VA": "Eastern",
        "WA": "Pacific",
        "WV": "Eastern",
        "WI": "Central",
        "WY": "Mountain" 
    }

    time_difference_UTC = {
        "Pacific": -8,
        "Mountain": -7,
        "Central": -6,
        "Eastern": -5
    }

    def __init__(self, meeting_duration: int):
       """Initialize with the desired meeting duration."""
       self.meeting_duration = meeting_duration

    def convert_timezone(self, team_members: List[TeamMember], target_timezone: str = "Eastern") -> List[TeamMember]:
        """
        Converts the time zone of the team members to the target timezone.
        """
        for member in team_members:
            state = member.getState()
            time_zone = self.state_time_zones[state]
            time_difference = self.time_difference_UTC[time_zone] 
            for i, (start, end) in enumerate(member.getAvailability()):
                member.availability[i] = (start + time_difference, end + time_difference)
        return team_members
    
    def create_availability_matrix(self, team_members: List[TeamMember]) -> np.ndarray:
        """
        Initialize 2D numpy array to store availability and seniority of a team member at a given start time
        """
        availability_matrix = np.zeros((24, len(team_members), 2))  # Adding another dimension for seniority
        for i, member in enumerate(team_members):
            for start, end in member.getAvailability():
                availability_matrix[start:end, i, 0] = 1  # Mark availability
                availability_matrix[start:end, i, 1] = member.getSeniority() - 1  # Mark seniority (0 for non-senior, 1 for senior)
        return availability_matrix

    def find_optimal_time(self, availability_matrix: np.ndarray, executive: bool = False) -> int:
        """
        Finds the best times for a meeting by checking the availability
        of the team members. 
        Return the time with the most members available if in default mode. 
        Return time with the most seniors available if in executive mode.
        """
        # Find the number of people and number of seniors available at each start time considering the meeting duration
        availability_count = np.zeros(24)
        senior_count = np.zeros(24)
        for start_time in range(24 - self.meeting_duration + 1):
            end_time = start_time + self.meeting_duration
            availability_count[start_time] = availability_matrix[start_time:end_time, :, 0].sum()
            senior_count[start_time] = availability_matrix[start_time:end_time, :, 1].sum()

        # Find the top five optimal time slots with a tuple of the start time, total number people available, and number of seniors available
        if executive:
            return np.argmax(availability_count)
        else:
            return np.argmax(availability_count)

def get_total_members(availability_matrix: np.ndarray, start_time: int, meeting_duration: int) -> int:
    """
    Get the total number of members available at a given start time.
    """
    return availability_matrix[start_time:start_time + meeting_duration, :, 0].sum()

def get_total_seniors(availability_matrix: np.ndarray, start_time: int, meeting_duration: int) -> int:
    """
    Get the total number of senior members available at a given start time.
    """
    return availability_matrix[start_time:start_time + meeting_duration, :, 1].sum()

# Example usage
member1 = TeamMember(name="Alice", availability=[(9, 11), (14, 16)], state="CA", seniority=2)
member2 = TeamMember(name="Bob", availability=[(10, 12), (13, 15)], state="NY", seniority=1)
member3 = TeamMember(name="Charlie", availability=[(9, 11), (14, 17)], state="TX", seniority=1)


# Create the scheduler with a specific meeting duration in hours
scheduler = Scheduler(meeting_time=1)
team = scheduler.convert_timezone([member1, member2, member3])

# Find the optimal meeting time
availability_matrix = scheduler.create_availability_matrix(team)
mode = True # Executive mode
optimal_time = scheduler.find_optimal_time(availability_matrix, mode)
total_members = get_total_members(availability_matrix, optimal_time, scheduler.meeting_time)
total_seniors = get_total_seniors(availability_matrix, optimal_time, scheduler.meeting_time)
print(f"The optimal meeting time is: {optimal_time}:00. There are {total_members} members, including {total_seniors} seniors, available.")
