# Queue-Based Level Locking System

## Overview
This system uses a **Queue (FIFO)** data structure to implement sequential level unlocking. Players must complete levels in order to unlock the next level.

## How It Works

### 1. Level Unlock Queue (`level_unlock_queue`)
- **Data Structure**: Queue (FIFO - First In, First Out)
- **Location**: `star_tracker.py` in the `StarTracker` class
- **Purpose**: Tracks which levels should be unlocked as players progress

### 2. Unlocking Mechanism

#### Initial State
- **Level 1** is always unlocked (starting level)
- All other levels (2-10) start as locked

#### Progression Flow
1. Player completes **Level 1** → Level 2 is enqueued (added to `level_unlock_queue`)
2. Player completes **Level 2** → Level 3 is enqueued
3. Player completes **Level 3** → Level 4 is enqueued
4. And so on...

### 3. Core Methods in `star_tracker.py`

#### `unlock_next_level(completed_level)`
```python
def unlock_next_level(self, completed_level):
    """
    Use Queue (FIFO) to unlock levels sequentially.
    When a level is completed, unlock the next level in the queue.
    """
    if 1 <= completed_level < self.total_levels:
        next_level = completed_level + 1
        if next_level not in self.level_unlock_queue:
            self.level_unlock_queue.append(next_level)
            self.save_data()
            return next_level
    return None
```
- Called when a player completes a level
- Enqueues the next level (FIFO - append to end)

#### `get_unlocked_levels()`
```python
def get_unlocked_levels(self):
    """
    Get list of unlocked levels using the queue.
    Level 1 always unlocked, rest unlock via completion queue.
    """
    unlocked = [1]
    
    completion_status = self.get_level_completion_status()
    for status in completion_status:
        if status['completed'] and status['level'] not in unlocked:
            unlocked.append(status['level'])
    
    for level in self.level_unlock_queue:
        if level not in unlocked:
            unlocked.append(level)
    
    return sorted(unlocked)
```
- Returns list of all currently unlocked levels
- Includes: Level 1 (always), completed levels, and queued levels

#### `is_level_unlocked(level)`
```python
def is_level_unlocked(self, level):
    """Check if a level is unlocked using the queue system"""
    unlocked_levels = self.get_unlocked_levels()
    return level in unlocked_levels
```
- Quick check if a specific level is unlocked

#### `get_next_locked_level()`
```python
def get_next_locked_level(self):
    """Get the next level that's locked (for UI hints)"""
    unlocked_levels = self.get_unlocked_levels()
    for level in range(1, self.total_levels + 1):
        if level not in unlocked_levels:
            return level
    return None
```
- Returns the first locked level (useful for UI hints)

## UI Integration in `menu.py`

### Modified `LevelButton` Class
- **New Parameter**: `is_locked` - indicates if level is locked
- **Visual Feedback**:
  - Locked levels: Darker color + lock emoji (🔒)
  - Unlocked levels: Normal color + stars + level number
  - Locked levels: Cannot be hovered or clicked

### Updated `create_level_buttons()`
```python
def create_level_buttons():
    unlocked_levels = tracker.get_unlocked_levels()
    
    for i in range(10):
        level_num = i + 1
        is_locked = level_num not in unlocked_levels
        level_buttons.append(LevelButton(x, y, level_size, level_num, 
                                         level_stars[i], is_locked=is_locked))
```
- Queries tracker for unlocked levels
- Creates buttons with appropriate lock status

### Level Select Screen Hint
- Displays message: "Complete Level X to unlock Level Y"
- Shows at bottom of level select screen
- Guides player on what to do next

### Updated `update_level_stars()`
```python
def update_level_stars(level_num, stars_earned):
    if 1 <= level_num <= 10:
        if stars_earned > level_stars[level_num - 1]:
            level_stars[level_num - 1] = stars_earned
            tracker.unlock_next_level(level_num)
            create_level_buttons()
            return True
    return False
```
- Automatically unlocks next level when current level is completed

## Data Persistence

The `level_unlock_queue` is saved to `star_data.json`:
```json
{
  "star_stacks": [...],
  "recent_achievements": [...],
  "level_unlock_queue": [2, 3, 4, 5]
}
```

## Example Progression

### Start Game
- Unlocked: [1]
- Locked: [2, 3, 4, 5, 6, 7, 8, 9, 10]

### After Completing Level 1
- Unlocked: [1, 2]
- Queue: [2]
- Locked: [3, 4, 5, 6, 7, 8, 9, 10]

### After Completing Levels 1-3
- Unlocked: [1, 2, 3, 4]
- Queue: [2, 3, 4]
- Locked: [5, 6, 7, 8, 9, 10]

## Features

✅ **Sequential Unlocking**: Must complete levels in order  
✅ **Queue-Based System**: Uses FIFO structure as specified  
✅ **Visual Feedback**: Locked levels show lock emoji  
✅ **Persistent Progress**: Saves unlock state to JSON  
✅ **Helpful UI Hints**: Shows next level to unlock  
✅ **No Skipping**: Can't play ahead of progression  

## Testing

To test the system:
1. Start a new game - only Level 1 should be unlocked
2. Complete Level 1 - Level 2 should unlock automatically
3. Close and reopen game - unlock state should persist
4. Try to click locked levels - should be unclickable
