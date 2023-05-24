#adiciona biblioteca
import pygame
import math
import random

# Inicializa pacotes
pygame.init()

# Gera janela
tela = pygame.display.set_mode((600, 400))
pygame.display.set_caption('Tower Defense')

black = (0, 0, 0)
background = pygame.image.load('imgs/Mapa possivel.png').convert()
fantasmarosa_img = pygame.image.load('imgs/fantasma_rosa.png').convert_alpha()
fantasmarosa_img = pygame.transform.scale(fantasmarosa_img, (40,30))

teste = True
caminho = [(0, 208), (80, 208), (80, 85), (200, 85), (200, 248), (360, 248), (360, 163), (600, 163)]

# Classe para os inimigos
class Fantasma(pygame.sprite.Sprite):
    def __init__(self, velocidade,img):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = caminho[0][0]
        self.rect.y = caminho[0][1]
        self.path_index = 0
        self.velocidade = velocidade

    def update(self):
        if self.path_index < len(caminho) - 1:
            destination = caminho[self.path_index + 1]
            dx = destination[0] - self.rect.x
            dy = destination[1] - self.rect.y
            distance = math.sqrt(dx ** 2 + dy ** 2)
            if distance > self.velocidade:
                speed_x = (dx / distance) * self.velocidade
                speed_y = (dy / distance) * self.velocidade
                self.rect.x += speed_x
                self.rect.y += speed_y
            else:
                self.rect.x = destination[0]
                self.rect.y = destination[1]
                self.path_index += 1

    def draw(self, screen):
        pygame.draw.rect(screen, black, self.rect)

# Grupo para armazenar os inimigos
fantasmas = pygame.sprite.Group()

rosa=1


# Variáveis de controle do jogo
FPS = pygame.time.Clock()
spawn_delay = 2000
last_spawn_time = 0
velocidades = [1, 2, 3, 4]  # Possíveis velocidades para os fantasmas

tempo_de_round=pygame.time.get_ticks()

while teste:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            teste = False

    tempo_de_round= pygame.time.get_ticks()
    tempo_de_jogo = pygame.time.get_ticks()

    # Verifica se é hora de criar um novo fantasma(delay)
    tempo_atual = pygame.time.get_ticks()

    if tempo_de_round < 10000:
        if tempo_atual - last_spawn_time >= spawn_delay:
            enemy = Fantasma(rosa,fantasmarosa_img) # Adiciona o novo fantasma
            fantasmas.add(enemy)
            last_spawn_time = tempo_atual


    # Atualização dos inimigos
    fantasmas.update()

    tela.blit(background, (0, 0))

    # Desenho dos inimigos
    fantasmas.draw(tela)

    pygame.display.flip()
    FPS.tick(60)

# Encerramento do Pygame
pygame.quit()