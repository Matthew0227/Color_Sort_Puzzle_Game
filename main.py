import pygame
import sys
import menu
import game_functions as gf

def main():
    # Initialize pygame
    pygame.init()
    
    # Start with menu
    current_screen = "main_menu"
    current_level = 1
    
    # Main application loop
    running = True
    while running:
        if current_screen == "main_menu":
            # Run menu screen
            result = menu.run_menu_screen()
            if result == "quit":
                running = False
            elif result == "level_select":
                current_screen = "level_select"
            elif result == "options":
                current_screen = "options"
            elif result == "how_to_play":
                current_screen = "how_to_play"
        
        elif current_screen == "level_select":
            # Run level select screen
            result, level_num = menu.run_level_select_screen()
            if result == "back":
                current_screen = "main_menu"
            elif result == "play_level":
                current_level = level_num
                current_screen = "game"
        
        elif current_screen == "game":
            # Run the actual game
            stars_earned = gf.run_game(current_level)
            
            # Update level progress with stars earned
            if stars_earned > 0:
                menu.update_level_stars(current_level, stars_earned)
            
            # Return to level select
            current_screen = "level_select"
            
        elif current_screen == "options":
            # Run options screen
            result = menu.run_options_screen()
            if result == "back":
                current_screen = "main_menu"
                
        elif current_screen == "how_to_play":
            # Run how to play screen
            result = gf.run_how_to_play_screen()
            if result:
                current_screen = "main_menu"
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()