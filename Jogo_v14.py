import pygame
import math
import random

# Inicialização do Pygame
pygame.init()

# Definição das cores
preto = (0, 0, 0)
vermelho = (255, 0, 0)
branco = (255,255,255)

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
mago_img = pygame.transform.scale(mago_img, (45, 45))
golem_img = pygame.image.load('imgs/Golem.png').convert_alpha()
golem_img = pygame.transform.scale(golem_img, (50, 50))
arqueiro_img = pygame.image.load('imgs/Arqueiro.png').convert_alpha()
arqueiro_img = pygame.transform.scale(arqueiro_img, (50, 50))
golem_tiros_img = pygame.image.load('imgs/pedra.png').convert_alpha()
golem_tiros_img = pygame.transform.scale(golem_tiros_img, (20, 20))
mago_tiros_img = pygame.image.load('imgs/Fogo.png').convert_alpha()
mago_tiros_img = pygame.transform.scale(mago_tiros_img, (20, 20))
arqueiro_tiros_img = pygame.image.load('imgs/flecha.png').convert_alpha()
arqueiro_tiros_img = pygame.transform.scale(arqueiro_tiros_img, (20, 30))

# Variáveis de controle do jogo
teste = True
caminho = [(0, 203), (80, 203), (80, 80), (200, 80), (200, 243), (360, 243), (360, 160), (600, 160)]
fim_caminho = (600,160)
fps = 45
spawn_delay = 1000
last_spawn_time = 0
dinheiro = 100

#Preço do valor de cada fantasma
precos_fantasmas = {"rosa": 2,"azul": 4,"azulclaro": 8,"vermelho": 16}

#Custo das Torres
custo = {'mago':100,'arqueiro':150,'golem':300}

# Posições da loja

torre_golem_pos = (545, 345)
torre_mago_pos = (494, 350)
torre_arqueiro_pos = (440, 345)

# Variável para armazenar a vida do jogador
vida_jogador = 100

# Fonte para exibir a vida do jogador na tela
fonte_vida = pygame.font.Font(None, 30)


# Classe para os inimigos
class Fantasma(pygame.sprite.Sprite):
    def __init__(self, velocidade, img, life):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = caminho[0][0]
        self.rect.y = caminho[0][1]
        self.path_index = 0
        self.velocidade = velocidade
        self.life = life

    def update(self):
        global vida_jogador
        if self.path_index < len(caminho)-1:
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
        
            if self.rect.x ==600 and self.rect.y ==160:
                vida_jogador -= self.life
                self.kill()
                if vida_jogador <= 0:
                    pygame.QUIT()

    def draw(self, screen):
        pygame.draw.rect(screen, preto, self.rect)

# Classe para as torres
class Torre(pygame.sprite.Sprite):
    def __init__(self, dano, custo, alcance, img, posicao, alcance_maximo,foto_disparo):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect(center=posicao)
        self.dano = dano
        self.custo = custo
        self.alcance = alcance
        self.alcance_maximo = alcance_maximo
        self.fantasmas_no_alcance = pygame.sprite.Group()
        self.last_shot_time = 0  # Variável para controlar o tempo entre os disparos
        self.shoot_delay = 2000  # Tempo de espera
        self.foto_tiro = foto_disparo 
        self.atirando = False

    def draw(self, screen):
        pygame.draw.rect(screen, preto, self.rect)

    def verificar_alcance(self, fantasma):
        distancia = math.sqrt(
            (fantasma.rect.centerx - self.rect.centerx) ** 2 + (fantasma.rect.centery - self.rect.centery) ** 2
        )
        return distancia <= self.alcance

    def atirar(self):
        current_time = pygame.time.get_ticks()
        if not self.atirando and current_time - self.last_shot_time > self.shoot_delay:
            if self.fantasmas_no_alcance:
                self.atirando = True
                fantasma = self.fantasmas_no_alcance.sprites()[0]  # Seleciona o primeiro fantasma
                projetil = Projetil(self.rect.center, self.dano, fantasma, self.alcance_maximo, self.foto_tiro)
                projeteis.add(projetil)
                self.last_shot_time = current_time
        else:
            self.atirando = False


# Classe para os projéteis
class Projetil(pygame.sprite.Sprite):
    def __init__(self, posicao, dano, alvo, alcance_maximo,foto_disparo):
        super().__init__()
        self.image = foto_disparo
        self.rect = self.image.get_rect(center=posicao)
        self.velocidade = 5
        self.dano = dano
        self.alvo = alvo
        self.alcance_maximo = alcance_maximo
        self.distancia_percorrida = 0

    def update(self):
        if self.alvo is not None:
            dx = self.alvo.rect.centerx - self.rect.centerx
            dy = self.alvo.rect.centery - self.rect.centery
            distance = math.sqrt(dx ** 2 + dy ** 2)
            if distance > 0:
                direction_x = dx / distance
                direction_y = dy / distance
                self.rect.x += direction_x * self.velocidade
                self.rect.y += direction_y * self.velocidade
                self.distancia_percorrida += self.velocidade
                if self.distancia_percorrida >= self.alcance_maximo:
                    self.kill()
            else:
                self.kill()

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
        enemy = Fantasma(1, fantasmarosa_img, 1)
    elif tipo_fantasma == "azul":
        enemy = Fantasma(2, fantasmaazul_img, 2)
    elif tipo_fantasma == "azulclaro":
        enemy = Fantasma(3, fantasmaazulclaro_img, 3)
    elif tipo_fantasma == "vermelho":
        enemy = Fantasma(4, fantasmavermelho_img, 4)

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

#Função para ver se o Fantasma morreu e adicionar dinheiro
def colisao_projetil_fantasma():
    global dinheiro
    colisoes = pygame.sprite.groupcollide(fantasmas, projeteis, False, False)
    for fantasma, projetil_lista in colisoes.items():
        for projetil in projetil_lista:
            fantasma.life -= projetil.dano
            projetil.kill()
        if fantasma.life <= 0:
            fantasma.kill()
            tipo_fantasma = obter_tipo_fantasma(fantasma)
            dinheiro += precos_fantasmas[tipo_fantasma]  # Adiciona o preço do fantasma ao dinheiro do jogador
    return dinheiro


# Função para obter o tipo do fantasma
def obter_tipo_fantasma(fantasma):
    if fantasma.image == fantasmarosa_img:
        return "rosa"
    elif fantasma.image == fantasmaazul_img:
        return "azul"
    elif fantasma.image == fantasmaazulclaro_img:
        return "azulclaro"
    elif fantasma.image == fantasmavermelho_img:
        return "vermelho"

# Função para desenhar o dinheiro na tela
def desenhar_dinheiro(screen):
    fonte = pygame.font.SysFont(None, 30)
    texto_dinheiro = fonte.render("Dinheiro: $" + str(dinheiro), True, branco)
    screen.blit(texto_dinheiro, (10, 360))


#Desenha a vida do jogador no canto superior direito
def desenhar_vida(screen):
    posicao_vida = (480, 20)
    texto_vida = fonte_vida.render("Vidas: " + str(vida_jogador), True, (255, 255, 255))
    screen.blit(texto_vida, posicao_vida)



# Função principal do jogo
def main():
    global last_spawn_time
    global vida_jogador
    global dinheiro
    teste = True
    vida_jogador=100
    dano_atual = 1
    custo_atual = 100
    alcance_atual = 100
    foto_atual = arqueiro_img
    alcancemax_atual = 120
    disparo_atual = arqueiro_tiros_img
    # Loop principal do jogo
    while teste:
        # Eventos do Pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                teste = False
                pygame.quit()
                return
            #Seleciona tipo de Torre
            if event.type == pygame.KEYDOWN:             
                if event.key == pygame.K_1:
                    dano_atual = 1
                    custo_atual = 100
                    alcance_atual = 100
                    foto_atual = arqueiro_img
                    alcancemax_atual = 120
                    disparo_atual = arqueiro_tiros_img
                
                if event.key == pygame.K_2:
                    dano_atual = 2
                    custo_atual = 200
                    alcance_atual = 90
                    foto_atual = mago_img
                    alcancemax_atual = 110
                    disparo_atual = mago_tiros_img

                if event.key == pygame.K_3:
                    dano_atual = 3
                    custo_atual = 400
                    alcance_atual = 70
                    foto_atual = golem_img
                    alcancemax_atual = 100
                    disparo_atual = golem_tiros_img

            #Seleciona posição da Torre
            if event.type == pygame.MOUSEBUTTONDOWN:
                if dinheiro >= custo_atual:
                    if pygame.mouse.get_pressed()[0]:
                        posicao_mouse = pygame.mouse.get_pos()
                        nova_torre = Torre(dano_atual, custo_atual, alcance_atual, foto_atual, posicao_mouse, alcancemax_atual,disparo_atual)
                        torres.add(nova_torre)
                        dinheiro -= custo_atual

        # Atualização dos objetos
        fantasmas.update()
        projeteis.update()

        # Verificação de colisão entre os projéteis e os fantasmas
        dinheiro = colisao_projetil_fantasma()

        # Verificação de colisão entre os projéteis e os fantasmas
        colisoes = pygame.sprite.groupcollide(fantasmas, projeteis, False, False)
        for fantasma, projetil_lista in colisoes.items():
            for projetil in projetil_lista:
                fantasma.life -= projetil.dano
                projetil.kill()
            if fantasma.life <= 0:
                fantasma.kill()
                

        # Verificação de alcance das torres
        for torre in torres:
            torre.fantasmas_no_alcance.empty()
            for fantasma in fantasmas:
                if torre.verificar_alcance(fantasma):
                    torre.fantasmas_no_alcance.add(fantasma)
            if len(torre.fantasmas_no_alcance) > 0:
                torre.atirar()
        
        

        # Renderização do jogo
        tela.blit(background, (0, 0))
        tela.blit(arqueiro_img, torre_arqueiro_pos)
        tela.blit(mago_img, torre_mago_pos)
        tela.blit(golem_img, torre_golem_pos)
        fonte_loja =  pygame.font.SysFont(None, 20)
        texto_preco_arqueiro = fonte_loja.render('$'+str(100),True,branco)
        tela.blit(texto_preco_arqueiro,(450,330))
        texto_preco_golem = fonte_loja.render('$'+str(400),True,branco)
        tela.blit(texto_preco_golem,(550,330))
        texto_preco_mago = fonte_loja.render('$'+str(200),True,branco)
        tela.blit(texto_preco_mago,(500,330))
        texto_tecla_arqueiro = fonte_loja.render(str(1),True,branco)
        tela.blit(texto_tecla_arqueiro,(450,385))
        texto_tecla_mago = fonte_loja.render(str(2),True,branco)
        tela.blit(texto_tecla_mago,(500,385))
        texto_tecla_golem = fonte_loja.render(str(3),True,branco)
        tela.blit(texto_tecla_golem,(550,385))

        desenhar_fantasmas(tela)
        desenhar_torres(tela)
        desenhar_projeteis(tela)
        desenhar_dinheiro(tela)
        desenhar_vida(tela)

        # Verificação do tempo para criar novos fantasmas
        current_time = pygame.time.get_ticks()
        if current_time - last_spawn_time > spawn_delay:
            criar_fantasma()
            last_spawn_time = current_time

        # Atualização da tela
        pygame.display.flip()
        pygame.time.Clock().tick(fps)

# Execução do jogo
if __name__ == "__main__":
    main()