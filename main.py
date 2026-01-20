import pygame
import sys
import menu
import game_functions as gf
import levels

def main():
    pygame.init()
    
    current_screen = "main_menu"
    current_level = 1
      
    running = True
    while running:
        if current_screen == "main_menu":            
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
            result, level_num = menu.run_level_select_screen()
            if result == "back":
                current_screen = "main_menu"
            elif result == "play_level":
                current_level = level_num
                current_screen = "game"
        
        elif current_screen == "game":          
            stars_earned, final_level, game_time = gf.run_game(current_level)
            
            if game_time is None:
                menu.tracker.load_data()
                menu.create_level_buttons()
                current_screen = "level_select"
                continue
            if stars_earned > 0:
                menu.update_level_stars(final_level, stars_earned)
                total_levels = levels.get_total_levels()
                end_result = gf.show_end_screen(final_level, stars_earned, game_time, total_levels)
                
                if end_result == "next" and final_level < total_levels:
                    current_level = final_level + 1
                    current_screen = "game"
                elif end_result == "restart":
                    current_level = final_level
                    current_screen = "game"
                else:
                    menu.tracker.load_data()
                    menu.create_level_buttons()
                    current_screen = "level_select"
            else:
                menu.tracker.load_data()
                menu.create_level_buttons()
                current_screen = "level_select"
            
        elif current_screen == "options":           
            result = menu.run_options_screen()
            if result == "back":
                current_screen = "main_menu"
                
        elif current_screen == "how_to_play":       
            result = gf.run_how_to_play_screen()
            if result:
                current_screen = "main_menu"
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()