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
    
    def menu_buttons(light_theme : bool) -> tuple[Button, Button]:
        base_color = "#000000" if light_theme else "#ffffff"
        hovering_color = "#636f87" if light_theme else "#99c0ff"

        PLAY_BUTTON = Button((WIDTH/2, HEIGHT/3), "PLAY",
                            pygame.font.Font("assets/font.otf", WIDTH//8), base_color, hovering_color)
        OPTIONS_BUTTON = Button((WIDTH/2, HEIGHT*2/3), "OPTIONS",
                                pygame.font.Font("assets/font.otf", WIDTH//8), base_color, hovering_color)
        
        return PLAY_BUTTON, OPTIONS_BUTTON
    
    def play_buttons(light_theme : bool) -> tuple[Button, Button]:
        base_color = "#000000" if light_theme else "#ffffff"
        hovering_color = "#636f87" if light_theme else "#99c0ff"

        FRIEND_BUTTON = Button((WIDTH/2, HEIGHT/3), "FRIEND",
                            pygame.font.Font("assets/font.otf", WIDTH//8), base_color, hovering_color)
        COMPUTER_BUTTON = Button((WIDTH/2, HEIGHT*2/3), "COMPUTER",
                                pygame.font.Font("assets/font.otf", WIDTH//8), base_color, hovering_color)
        
        return FRIEND_BUTTON, COMPUTER_BUTTON

    def right_left_buttons(height : float, light_theme : bool) -> tuple[Button, Button]:
        base_color = "#000000" if light_theme else "#ffffff"
        hovering_color = "#636f87" if light_theme else "#99c0ff"

        RIGHT_BUTTON = Button((WIDTH*3/4+SQUARE_SIZE, height), ">",
                                    pygame.font.Font("assets/font.otf", WIDTH//8), base_color, hovering_color)
        LEFT_BUTTON = Button((WIDTH*3/4-SQUARE_SIZE, height), "<",
                                    pygame.font.Font("assets/font.otf", WIDTH//8), base_color, hovering_color)

        return RIGHT_BUTTON, LEFT_BUTTON

    def volume_button(volume_status : bool, light_theme : bool) -> Button:
        base_color = "#000000" if light_theme else "#ffffff"
        hovering_color = "#636f87" if light_theme else "#99c0ff"

        VOLUME_ON_BUTTON = Button((WIDTH/4, HEIGHT*9/10), VOLUME_ON,
                                pygame.font.Font("assets/FontAwesome.otf", WIDTH//8), base_color, hovering_color)
        VOLUME_OFF_BUTTON = Button((WIDTH/4, HEIGHT*9/10), VOLUME_OFF,
                                pygame.font.Font("assets/FontAwesome.otf", WIDTH//8), base_color, hovering_color)
        return VOLUME_ON_BUTTON if volume_status else VOLUME_OFF_BUTTON
    
    def theme_button(light_theme : bool) -> Button:
        hovering_color = "#636f87" if light_theme else "#99c0ff"

        LIGHT_BUTTON = Button((WIDTH*8/9, HEIGHT*9/10), SUN,
                                pygame.font.Font("assets/FontAwesome.otf", WIDTH//8), "Orange", hovering_color)
        DARK_BUTTON = Button((WIDTH*8/9, HEIGHT*9/10), MOON,
                                pygame.font.Font("assets/FontAwesome.otf", WIDTH//8), "Dark Blue", hovering_color)
        return DARK_BUTTON if light_theme else LIGHT_BUTTON

    def end_buttons(light_theme : bool) -> tuple[Button, Button]:
        base_color = "#000000" if light_theme else "#ffffff"
        hovering_color = "#636f87" if light_theme else "#99c0ff"

        REMATCH_BUTTON = Button((WIDTH/2, HEIGHT/3+HEIGHT/5), "REMATCH",
                                pygame.font.Font("assets/font.otf", WIDTH//8), base_color, hovering_color)
        MAIN_MENU_BUTTON = Button((WIDTH/2, HEIGHT/3+HEIGHT/2), "MENU",
                                    pygame.font.Font("assets/font.otf", WIDTH//8), base_color, hovering_color)

        return REMATCH_BUTTON, MAIN_MENU_BUTTON