from __future__ import annotations
import pygame
from constants import *

class Button():
    def __init__(self, pos, text_input, font, base_color, hovering_color):
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        self.rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def draw(self, screen):
        screen.blit(self.text, self.text_rect)

    def check_for_input(self, position):
        return position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom)


    def change_color(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
    
    
    def menu_buttons() -> tuple[Button, Button]:
        PLAY_BUTTON = Button((WIDTH/2, HEIGHT/3+HEIGHT/8), "PLAY",
                            pygame.font.Font("assets/font.otf", WIDTH//8),"#000000", "Dark Blue")
        OPTIONS_BUTTON = Button((WIDTH/2, 2*HEIGHT/3+HEIGHT/8), "OPTIONS",
                                pygame.font.Font("assets/font.otf", WIDTH//8), "#000000", "Dark Blue")
        
        return PLAY_BUTTON, OPTIONS_BUTTON


    def right_left_buttons(height : float) -> tuple[Button, Button]:
        RIGHT_BUTTON = Button((WIDTH*3/4+SQUARE_SIZE, height), ">",
                                    pygame.font.Font("assets/font.otf", WIDTH//8), "White", "Dark Blue")
        LEFT_BUTTON = Button((WIDTH*3/4-SQUARE_SIZE, height), "<",
                                    pygame.font.Font("assets/font.otf", WIDTH//8), "White", "Dark Blue")

        return RIGHT_BUTTON, LEFT_BUTTON


    def end_buttons() -> tuple[Button, Button]:
        REMATCH_BUTTON = Button((WIDTH/2, HEIGHT/3+HEIGHT/5), "REMATCH",
                                pygame.font.Font("assets/font.otf", WIDTH//8), "Gray", "Green")
        MAIN_MENU_BUTTON = Button((WIDTH/2, HEIGHT/3+HEIGHT/2), "MENU",
                                    pygame.font.Font("assets/font.otf", WIDTH//8), "Gray", "Green")

        return REMATCH_BUTTON, MAIN_MENU_BUTTON