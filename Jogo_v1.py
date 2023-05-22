#adiciona biblioteca
import pygame

#inicia pacotes
pygame.init()

#gera janela
tela= pygame.display.set_mode((600,400))
pygame.display.set_caption('Tower Defense')

background = pygame.image.load('imgs/Mapa possivel.png').convert()

teste=True

while teste:

    for event in pygame.event.get():
        # ----- Verifica consequências
        if event.type == pygame.QUIT:
            teste = False

    tela.blit(background, (0, 0))
    pygame.display.update()