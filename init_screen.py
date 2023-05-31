import pygame

# Inicialização do Pygame
pygame.init()

def tela_inicial():
    tela = pygame.display.set_mode((600, 400))
    pygame.display.set_caption('Tower Defense')
    relogio = pygame.time.Clock()
    fps = 45

    background = pygame.image.load('imgs/Mapa possivel.png').convert()
    # Configurações do botão "Start game"
    largura_botao = 200
    altura_botao = 50
    cor_botao = (231, 135, 0)  
    cor_do_texto = (255, 255, 255)  
    
    running = True
    while running:
        # Ajusta a velocidade do jogo.
        relogio.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                button_rect = pygame.Rect((tela.get_width() - largura_botao) // 2,(tela.get_height() - altura_botao) // 2,largura_botao,altura_botao)
                if button_rect.collidepoint(mouse_pos):
                    start_game()  # Função para iniciar o jogo

        # Desenha o fundo
        tela.blit(background, (0, 0))
        
        # Desenha o botão "Start game"
        button_rect = pygame.Rect(
            (tela.get_width() - largura_botao) // 2,
            (tela.get_height() - altura_botao) // 2,
            largura_botao,
            altura_botao
        )
        pygame.draw.rect(tela, cor_botao, button_rect)
        
        # Desenha o texto do botão
        font = pygame.font.Font(None, 30)
        text = font.render("Start game", True, cor_do_texto)
        text_rect = text.get_rect(center=button_rect.center)
        tela.blit(text, text_rect)

        # Atualiza a tela
        pygame.display.flip()

    pygame.quit()

def start_game():
    # Lógica para iniciar o jogo
    print("Jogo iniciado!")
    # Adicione aqui o código para mudar para a tela de jogo

# Executa a tela inicial
tela_inicial()
