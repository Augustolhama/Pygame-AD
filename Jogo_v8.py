import pygame
import math
import random

# Inicialização do Pygame
pygame.init()

# Definição das cores
preto = (0, 0, 0)
vermelho = (255, 0, 0)

# Geração da janela
tela = pygame.display.set_mode((600, 400))
pygame.display.set_caption('Tower Defense')

# Carregamento das imagens
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

# Variáveis de controle do jogo
teste = True
caminho = [(0, 203), (80, 203), (80, 80), (200, 80), (200, 243), (360, 243), (360, 160), (600, 160)]
fps = 60
spawn_delay = 2000
last_spawn_time = 0

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
        pygame.draw.rect(screen, preto, self.rect)

# Classe para as torres
class Torre(pygame.sprite.Sprite):
    def __init__(self, dano, custo, alcance, img, posicao):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect(center=posicao)
        self.dano = dano
        self.custo = custo
        self.alcance = alcance

    def draw(self, screen):
        pygame.draw.rect(screen, preto, self.rect)

    def verificar_alcance(self, alvo):
        dx = alvo.rect.centerx - self.rect.centerx
        dy = alvo.rect.centery - self.rect.centery
        distancia = math.sqrt(dx ** 2 + dy ** 2)
        return distancia <= self.alcance

    def atirar(self):
        projetil = Projetil(self.rect.center, self.dano)
        projeteis.add(projetil)

# Classe para os projéteis
class Projetil(pygame.sprite.Sprite):
    def __init__(self, posicao, dano):
        super().__init__()
        self.image = pygame.Surface((8, 8))
        self.image.fill(vermelho)
        self.rect = self.image.get_rect(center=posicao)
        self.velocidade = 5
        self.dano = dano

    def update(self):
        self.rect.x += self.velocidade

# Grupo para armazenar os inimigos
fantasmas = pygame.sprite.Group()

# Grupo para armazenar as torres
torres = pygame.sprite.Group()

# Grupo para armazenar os projéteis
projeteis = pygame.sprite.Group()

# Função para criar um novo fantasma
def criar_fantasma():
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

# Função para desenhar os fantasmas na tela
def desenhar_fantasmas(screen):
    for fantasma in fantasmas:
        screen.blit(fantasma.image, fantasma.rect)

# Função para desenhar as torres na tela
def desenhar_torres(screen):
    for torre in torres:
        screen.blit(torre.image, torre.rect)

# Função para desenhar os projéteis na tela
def desenhar_projeteis(screen):
    for projetil in projeteis:
        screen.blit(projetil.image, projetil.rect)

# Função para atualizar os projéteis
def atualizar_projeteis():
    projeteis.update()

# Função para verificar colisões entre projéteis e fantasmas
def verificar_colisoes():
    colisoes = pygame.sprite.groupcollide(fantasmas, projeteis, True, True)
    for fantasma, projetil_lista in colisoes.items():
        for projetil in projetil_lista:
            print(f"Fantasma atingido! Dano: {projetil.dano}")

# Criação da torre
torre_mago = Torre(2, 100, 150, mago_img, (140, 140))
torres.add(torre_mago)

while teste:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            teste = False

    # Verifica se é hora de criar um novo fantasma (delay)
    tempo_atual = pygame.time.get_ticks()

    if tempo_atual - last_spawn_time >= spawn_delay:
        criar_fantasma()
        last_spawn_time = tempo_atual

    # Atualizações
    fantasmas.update()
    projeteis.update()

    # Verifica colisões
    verificar_colisoes()

    # Atira nas torres quando um fantasma está dentro do alcance
    for torre in torres:
        for fantasma in fantasmas:
            if torre.verificar_alcance(fantasma):
                torre.atirar()

    # Renderização
    tela.blit(background, (0, 0))
    desenhar_fantasmas(tela)
    desenhar_torres(tela)
    desenhar_projeteis(tela)

    pygame.display.flip()
    pygame.time.Clock().tick(fps)

# Encerramento do Pygame
pygame.quit()