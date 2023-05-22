#adiciona biblioteca
import pygame
import math

#inicia pacotes
pygame.init()

#gera janela
tela= pygame.display.set_mode((600,400))
pygame.display.set_caption('Tower Defense')


black = (0, 0, 0)
background = pygame.image.load('imgs/Mapa possivel.png').convert()

teste=True
caminho=[(0,200),(100,200),(100,100),(200,100),(200,250),(400,250),(400,180),(600,180)]

# Classe para os inimigos
class Fantasma(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(black)
        self.rect = self.image.get_rect()
        self.rect.x = caminho[0][0]
        self.rect.y = caminho[0][1]
        self.path_index = 0

    def update(self):
        if self.path_index < len(caminho) - 1:
            destination = caminho[self.path_index + 1]
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
fantasmas  = pygame.sprite.Group()


# Variáveis de controle do jogo
FPS = pygame.time.Clock()

while teste:

    tela.blit(background, (0, 0))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            teste = False

    # Criação de inimigos
    if len(fantasmas) < 10:  # Limite de inimigos
        enemy = Fantasma()
        fantasmas.add(enemy)

    # Atualização dos inimigos
    for enemy in fantasmas:
        enemy.update()

    # Desenho do caminho
    pygame.draw.lines(tela, black, False, caminho)

    # Desenho dos inimigos
    for enemy in fantasmas:
        enemy.draw(tela)

    


    pygame.display.flip()
    FPS.tick(60)

# Encerramento do Pygame
pygame.quit()