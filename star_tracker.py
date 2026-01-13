
import json
import os

class StarTracker:
    """Track star achievements using list-based data structures"""
    
    def __init__(self, filename="star_data.json"):
        """Initialize star tracker with empty stacks for each level"""
        self.filename = filename
        self.total_levels = 10
        
        # Main data structure: list of stacks (FILO) for star history
        # Each level has a stack of star achievements
        self.star_stacks = []
        
        # Queue (FIFO) for recent achievements (last 5)
        self.recent_achievements = []
        
        # Queue (FIFO) for completed levels to control unlock order
        self.level_unlock_queue = []
        
        # Initialize with empty stacks
        for _ in range(self.total_levels):
            self.star_stacks.append([])  # Empty stack for each level
        
        self.load_data()
    
    def push_star_achievement(self, level, stars, time):
        """Push a new star achievement onto the level's stack (Stack - FILO)"""
        if 1 <= level <= self.total_levels:
            achievement = {
                'stars': stars,
                'time': time,
                'timestamp': self.get_current_time()
            }
            
            # Push to stack (FILO)
            self.star_stacks[level-1].append(achievement)
            
            # Also add to recent achievements queue (FIFO)
            self.enqueue_recent_achievement(level, stars, time)
            
            self.save_data()
            return True
        return False
    
    def pop_star_achievement(self, level):
        """Pop the most recent achievement from level's stack (Stack - FILO)"""
        if 1 <= level <= self.total_levels:
            if self.star_stacks[level-1]:
                return self.star_stacks[level-1].pop()  # FILO
        return None
    
    def peek_star_achievement(self, level):
        """Peek at the top achievement without removing it (Stack - FILO)"""
        if 1 <= level <= self.total_levels:
            if self.star_stacks[level-1]:
                return self.star_stacks[level-1][-1]  # Last element
        return None
    
    def get_best_stars(self, level):
        """Get the best star rating for a level by iterating through stack"""
        if 1 <= level <= self.total_levels:
            best_stars = 0
            best_time = 0  # Change from float('inf') to 0
            
            # If stack is empty, return 0, 0
            if not self.star_stacks[level-1]:
                return best_stars, best_time
            
            # Initialize with first achievement
            first_achievement = self.star_stacks[level-1][0]
            best_stars = first_achievement['stars']
            best_time = first_achievement['time']
            
            # Iterate through remaining achievements to find best
            for achievement in self.star_stacks[level-1][1:]:
                if achievement['stars'] > best_stars:
                    best_stars = achievement['stars']
                    best_time = achievement['time']
                elif achievement['stars'] == best_stars and achievement['time'] < best_time:
                    best_time = achievement['time']
            
            return best_stars, best_time
        return 0, 0
    
    def get_level_stats(self, level):
        """Get comprehensive stats for a level using list operations"""
        if 1 <= level <= self.total_levels:
            stack = self.star_stacks[level-1]
            if not stack:
                return {
                    'best_stars': 0,
                    'best_time': 0,
                    'total_attempts': 0,
                    'average_stars': 0,
                    'completion_rate': 0
                }
            
            # Calculate various stats using list comprehension
            stars_list = [a['stars'] for a in stack]
            time_list = [a['time'] for a in stack]
            
            best_stars = max(stars_list)
            best_time = min(time_list) if time_list else 0
            
            # Filter completed attempts (stars > 0)
            completed_attempts = [a for a in stack if a['stars'] > 0]
            
            return {
                'best_stars': best_stars,
                'best_time': best_time,
                'total_attempts': len(stack),
                'average_stars': sum(stars_list) / len(stars_list),
                'completion_rate': len(completed_attempts) / len(stack) * 100
            }
        return None
    
    def enqueue_recent_achievement(self, level, stars, time):
        """Add achievement to recent queue (Queue - FIFO)"""
        achievement = {
            'level': level,
            'stars': stars,
            'time': time,
            'timestamp': self.get_current_time()
        }
        
        # Enqueue (FIFO) - add to end
        self.recent_achievements.append(achievement)
        
        # Keep only last 5 achievements
        if len(self.recent_achievements) > 5:
            # Dequeue from front (FIFO)
            self.recent_achievements.pop(0)
    
    def dequeue_recent_achievement(self):
        """Remove and return oldest achievement from recent queue (FIFO)"""
        if self.recent_achievements:
            return self.recent_achievements.pop(0)  # FIFO
        return None
    
    def get_recent_achievements(self):
        """Get all recent achievements (Queue - FIFO order)"""
        return self.recent_achievements.copy()
    
    def get_level_completion_status(self):
        """Get completion status for all levels using list operations"""
        status = []
        for level in range(1, self.total_levels + 1):
            best_stars, best_time = self.get_best_stars(level)
            status.append({
                'level': level,
                'best_stars': best_stars,
                'best_time': best_time,
                'completed': best_stars > 0
            })
        return status
    
    def get_total_stars(self):
        """Get total stars earned across all levels"""
        total = 0
        for level in range(1, self.total_levels + 1):
            best_stars, _ = self.get_best_stars(level)
            total += best_stars
        return total
    
    def unlock_next_level(self, completed_level):
        """
        Use Queue (FIFO) to unlock levels sequentially.
        When a level is completed, unlock the next level in the queue.
        """
        if 1 <= completed_level < self.total_levels:
            next_level = completed_level + 1
            if next_level not in self.level_unlock_queue:
                self.level_unlock_queue.append(next_level)  # Enqueue
                self.save_data()
                return next_level
        return None
    
    def get_unlocked_levels(self):
        """
        Get list of unlocked levels using the queue.
        Level 1 always unlocked, rest unlock via completion queue.
        """
        unlocked = [1]  # Level 1 always available
        
        # Add all levels that have been completed (exist in completion status)
        completion_status = self.get_level_completion_status()
        for status in completion_status:
            if status['completed'] and status['level'] not in unlocked:
                unlocked.append(status['level'])
        
        # Add queued levels
        for level in self.level_unlock_queue:
            if level not in unlocked:
                unlocked.append(level)
        
        return sorted(unlocked)
    
    def is_level_unlocked(self, level):
        """Check if a level is unlocked using the queue system"""
        unlocked_levels = self.get_unlocked_levels()
        return level in unlocked_levels
    
    def get_next_locked_level(self):
        """Get the next level that's locked (for UI hints)"""
        unlocked_levels = self.get_unlocked_levels()
        for level in range(1, self.total_levels + 1):
            if level not in unlocked_levels:
                return level
        return None
    
    def clear_level_data(self, level):
        """Clear all achievements for a specific level"""
        if 1 <= level <= self.total_levels:
            self.star_stacks[level-1].clear()
            self.save_data()
            return True
        return False
    
    def clear_all_data(self):
        """Clear all star tracking data"""
        for i in range(self.total_levels):
            self.star_stacks[i].clear()
        self.recent_achievements.clear()
        self.level_unlock_queue.clear()
        self.save_data()
    
    def reset_all_levels(self):
        """Reset all levels - clear all achievements and unlock queue"""
        self.clear_all_data()
    
    def save_data(self):
        """Save star data to JSON file"""
        try:
            # Convert stacks to serializable format
            serializable_stacks = []
            for stack in self.star_stacks:
                serializable_stacks.append(stack.copy())
            
            data = {
                'star_stacks': serializable_stacks,
                'recent_achievements': self.recent_achievements,
                'level_unlock_queue': self.level_unlock_queue
            }
            
            with open(self.filename, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving star data: {e}")
            return False
    
    def load_data(self):
        """Load star data from JSON file"""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                
                # Load stacks
                self.star_stacks = []
                for stack_data in data.get('star_stacks', []):
                    self.star_stacks.append(stack_data)
                
                # Load recent achievements
                self.recent_achievements = data.get('recent_achievements', [])
                
                # Load level unlock queue
                self.level_unlock_queue = data.get('level_unlock_queue', [])
                
                # Ensure we have the right number of stacks
                while len(self.star_stacks) < self.total_levels:
                    self.star_stacks.append([])
                
                # Trim if we have too many
                self.star_stacks = self.star_stacks[:self.total_levels]
                
                return True
        except Exception as e:
            print(f"Error loading star data: {e}")
        return False
    
    def get_current_time(self):
        """Get current timestamp (simplified for this game)"""
        import time
        return time.time()
    
    def display_stats(self):
        """Display all statistics (for debugging/console)"""
        print("\n=== STAR TRACKER STATISTICS ===")
        print(f"Total Stars Earned: {self.get_total_stars()}")
        print(f"Total Levels: {self.total_levels}")
        
        print("\nLevel Completion Status:")
        for status in self.get_level_completion_status():
            star_symbols = "★" * status['best_stars'] + "☆" * (3 - status['best_stars'])
            print(f"  Level {status['level']}: {star_symbols} (Best: {status['best_time']:.1f}s)")
        
        print("\nRecent Achievements (FIFO):")
        for i, achievement in enumerate(self.recent_achievements, 1):
            star_symbols = "★" * achievement['stars'] + "☆" * (3 - achievement['stars'])
            print(f"  {i}. Level {achievement['level']}: {star_symbols} in {achievement['time']:.1f}s")
        
        print("\nStack Operations Available:")
        print("  - push_star_achievement(level, stars, time): Add new achievement (FILO)")
        print("  - pop_star_achievement(level): Remove latest achievement (FILO)")
        print("  - peek_star_achievement(level): View latest without removing")
        print("\nQueue Operations Available:")
        print("  - Recent achievements automatically enqueued (FIFO)")
        print("  - dequeue_recent_achievement(): Remove oldest recent achievement")
        print("=" * 35)


# Example usage
if __name__ == "__main__":
    tracker = StarTracker()
    
    # Demo stack operations (FILO)
    print("Demo: Stack Operations (FILO - Last In, First Out)")
    tracker.push_star_achievement(1, 3, 25.5)
    tracker.push_star_achievement(1, 2, 35.0)
    tracker.push_star_achievement(1, 3, 22.0)  # This will be on top
    
    top = tracker.peek_star_achievement(1)
    print(f"Top of stack for level 1: {top['stars']} stars in {top['time']}s")
    
    popped = tracker.pop_star_achievement(1)
    print(f"Popped from stack: {popped['stars']} stars")
    
    # Demo queue operations (FIFO)
    print("\nDemo: Queue Operations (FIFO - First In, First Out)")
    tracker.enqueue_recent_achievement(2, 3, 45.0)
    tracker.enqueue_recent_achievement(3, 1, 60.0)
    
    recent = tracker.get_recent_achievements()
    print(f"Recent achievements queue: {len(recent)} items")
    
    # Display all stats
    tracker.display_stats()