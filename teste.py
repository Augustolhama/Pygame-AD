import pygame
import sys
import random
import math

# Inicialização do Pygame
pygame.init()

# Configurações da janela
window_width = 800
window_height = 600
window_size = (window_width, window_height)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Tower Defense")

# Cores
black = (0, 0, 0)
white = (255, 255, 255)

# Variáveis de controle do jogo
clock = pygame.time.Clock()
game_over = False

# Definição do caminho
path = [(0, 200), (200, 200), (200, 400), (600, 400), (600, 200), (800, 200)]

# Classe para os inimigos
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(black)
        self.rect = self.image.get_rect()
        self.rect.x = path[0][0]
        self.rect.y = path[0][1]
        self.path_index = 0

    def update(self):
        if self.path_index < len(path) - 1:
            destination = path[self.path_index + 1]
            dx = destination[0] - self.rect.x
            dy = destination[1] - self.rect.y
            distance = math.sqrt(dx ** 2 + dy ** 2)
            if distance > 0:
                speed = 2  # Velocidade do inimigo
                self.rect.x += (dx / distance) * speed
                self.rect.y += (dy / distance) * speed
            if dx == 0 and dy == 0:
                self.path_index += 1

    def draw(self, screen):
        pygame.draw.rect(screen, black, self.rect)

# Grupo para armazenar os inimigos
enemies = pygame.sprite.Group()

# Loop principal do jogo
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    # Criação de inimigos
    if len(enemies) < 10:  # Limite de inimigos
        enemy = Enemy()
        enemies.add(enemy)

    # Atualização dos inimigos
    for enemy in enemies:
        enemy.update()

    # Renderização da tela
    window.fill(white)

    # Desenho do caminho
    pygame.draw.lines(window, black, False, path)

    # Desenho dos inimigos
    for enemy in enemies:
        enemy.draw(window)

    pygame.display.flip()
    clock.tick(60)

# Encerramento do Pygame
pygame.quit()
sys.exit()