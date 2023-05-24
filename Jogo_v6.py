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
fantasmarosa_img = pygame.transform.scale(fantasmarosa_img, (35, 35))

fantasmaazul_img = pygame.image.load('imgs/fantasma_azul.png').convert_alpha()
fantasmaazul_img = pygame.transform.scale(fantasmaazul_img, (35, 35))

fantasmaazulclaro_img = pygame.image.load('imgs/fantasma_azulclaro.png').convert_alpha()
fantasmaazulclaro_img = pygame.transform.scale(fantasmaazulclaro_img, (35, 35))

fantasmavermelho_img = pygame.image.load('imgs/fantasma_vermelho.png').convert_alpha()
fantasmavermelho_img = pygame.transform.scale(fantasmavermelho_img, (35, 35))

mago_img = pygame.image.load('imgs/Mago.png').convert_alpha()
mago_img = pygame.transform.scale(mago_img, (35, 35))

golem_img = pygame.image.load('imgs/Golem.png').convert_alpha()
golem_img = pygame.transform.scale(golem_img, (35, 35))

arqueiro_img = pygame.image.load('imgs/Arqueiro.png').convert_alpha()
arqueiro_img = pygame.transform.scale(arqueiro_img, (35, 35))

teste = True
caminho = [(0, 203), (80, 203), (80, 80), (200, 80), (200, 243), (360, 243), (360, 160), (600, 160)]

# Classe para os inimigos
class Fantasma(pygame.sprite.Sprite):
    def __init__(self, velocidade, img):
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
                direction_x = dx / distance
                direction_y = dy / distance
                self.rect.x += direction_x * self.velocidade
                self.rect.y += direction_y * self.velocidade
            else:
                self.rect.x = destination[0]
                self.rect.y = destination[1]
                self.path_index += 1


    def draw(self, screen):
        pygame.draw.rect(screen, black, self.rect)

# Classe para as torres
class Torre(pygame.sprite.Sprite):
    def __init__(self, dano, custo, alcance, img):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect()
        self.dano = dano
        self.custo = custo
        self.alcance = alcance

    def draw(self, screen):
        pygame.draw.rect(screen, black, self.rect)

# Grupo para armazenar os inimigos
fantasmas = pygame.sprite.Group()

# Variáveis de controle do jogo
FPS = pygame.time.Clock()
spawn_delay = 2000
last_spawn_time = 0

while teste:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            teste = False

    # Verifica se é hora de criar um novo fantasma (delay)
    tempo_atual = pygame.time.get_ticks()

    if tempo_atual - last_spawn_time >= spawn_delay:
        # Escolhe aleatoriamente o tipo de fantasma
        tipo_fantasma = random.choice(["rosa", "azul", "azulclaro", "vermelho"])

        if tipo_fantasma == "rosa":
            enemy = Fantasma(1, fantasmarosa_img)
        elif tipo_fantasma == "azul":
            enemy = Fantasma(2, fantasmaazul_img)
        elif tipo_fantasma == "azulclaro":
            enemy = Fantasma(3, fantasmaazulclaro_img)
        elif tipo_fantasma == "vermelho":
            enemy = Fantasma(4, fantasmavermelho_img)

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