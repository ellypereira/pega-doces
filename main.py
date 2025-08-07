import pygame
import random
import os

# Inicializar o pygame
pygame.init()

# Caminho para assets
CAMINHO_ASSETS = os.path.join(os.path.dirname(__file__), "assets")

# Iniciar música de fundo
pygame.mixer.music.load(os.path.join(CAMINHO_ASSETS, "musica.ogg.wav"))  # ou .mp3
pygame.mixer.music.play(-1)  # -1 faz tocar em loop infinito
pygame.mixer.music.set_volume(0.4)  # volume entre 0.0 e 1.0

# Pontuação e fonte
pontuacao = 0
fonte = pygame.font.SysFont("Arial", 30)

# Configurações da janela
LARGURA = 700
ALTURA = 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("🍬 Pega Doces!")

# Cores
BRANCO = (242, 193, 209)

# Carregar imagem do personagem
personagem_img = pygame.image.load(os.path.join(CAMINHO_ASSETS, "personagem.png")).convert_alpha()
personagem_img = pygame.transform.scale(personagem_img, (80, 80))

# Carregar imagens dos doces
doces_imgs = [
    pygame.transform.scale(pygame.image.load(os.path.join(CAMINHO_ASSETS, "doce1.png")).convert_alpha(), (40, 40)),
    pygame.transform.scale(pygame.image.load(os.path.join(CAMINHO_ASSETS, "doce2.png")).convert_alpha(), (40, 40)),
    pygame.transform.scale(pygame.image.load(os.path.join(CAMINHO_ASSETS, "doce3.png")).convert_alpha(), (40, 40))
]

# Posição inicial do personagem
personagem_x = LARGURA // 2
personagem_y = ALTURA - 100
personagem_vel = 8

# Lista de doces
doces = []
velocidade_doce = 5
intervalo_spawn = 30
contador_frames = 0

# Jogo
vidas = 5
estado_jogo = "jogando"

velocidade_doce = 2             # começa devagar
intervalo_spawn = 60            # mais tempo entre os doces
contador_frames = 0
dificuldade_timer = 0          # tempo para aumentar dificuldade


# Loop do jogo
rodando = True
relogio = pygame.time.Clock()

while rodando:
    tela.fill(BRANCO)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.MOUSEBUTTONDOWN and estado_jogo == "fim":
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if botao_x <= mouse_x <= botao_x + botao_largura and botao_y <= mouse_y <= botao_y + botao_altura:
                # Reinicia o jogo
                doces.clear()
                pontuacao = 0
                vidas = 5
                personagem_x = LARGURA // 2
                estado_jogo = "jogando"
                contador_frames = 0
                velocidade_doce = 2
                intervalo_spawn = 60
                dificuldade_timer = 0

    if estado_jogo == "jogando":
        # Aumentar dificuldade com o tempo
        dificuldade_timer += 1
        if dificuldade_timer % 600 == 0:  # a cada 10 segundos (600 frames se o jogo roda a 60 FPS)
            if velocidade_doce < 15:
                velocidade_doce += 1  # doces caem mais rápido
            if intervalo_spawn > 10:
                intervalo_spawn -= 5  # doces aparecem mais frequentemente
        # Movimento
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and personagem_x > 0:
            personagem_x -= personagem_vel
        if teclas[pygame.K_RIGHT] and personagem_x < LARGURA - 80:
            personagem_x += personagem_vel

        # Gerar doces
        contador_frames += 1
        if contador_frames % intervalo_spawn == 0:
            novo_doce = {
                "x": random.randint(0, LARGURA - 40),
                "y": 0,
                "img": random.choice(doces_imgs)
            }
            doces.append(novo_doce)

        # Atualizar e desenhar doces
        for doce in doces[:]:
            doce["y"] += velocidade_doce
            tela.blit(doce["img"], (doce["x"], doce["y"]))

            # Colisão
            personagem_ret = pygame.Rect(personagem_x, personagem_y, 80, 80)
            doce_ret = pygame.Rect(doce["x"], doce["y"], 40, 40)

            if personagem_ret.colliderect(doce_ret):
                doces.remove(doce)
                pontuacao += 1

            elif doce["y"] > ALTURA:
                doces.remove(doce)
                vidas -= 1
                if vidas <= 0:
                    estado_jogo = "fim"

        # Texto de pontos e vidas
        texto = fonte.render(f"Pontos: {pontuacao}", True, (0, 0, 0))
        vidas_txt = fonte.render(f"Vidas: {vidas}", True, (255, 0, 0))
        tela.blit(texto, (10, 10))
        tela.blit(vidas_txt, (10, 50))

        # Personagem
        tela.blit(personagem_img, (personagem_x, personagem_y))

    elif estado_jogo == "fim":
        # Tela de fim
        # TELA DE GAME OVER
        game_over_txt = fonte.render("Game Over!", True, (0, 0, 0))
        pontos_finais = fonte.render(f"Pontuação final: {pontuacao}", True, (0, 0, 0))
        tela.blit(game_over_txt, (LARGURA // 2 - 100, ALTURA // 2 - 60))
        tela.blit(pontos_finais, (LARGURA // 2 - 100, ALTURA // 2 - 20))

        # Botão "Jogar Novamente"
        botao_largura = 300
        botao_altura = 50
        botao_x = LARGURA // 2 - botao_largura // 2
        botao_y = ALTURA // 2 + 40

        # Desenha o botão
        pygame.draw.rect(tela, (0, 200, 0), (botao_x, botao_y, botao_largura, botao_altura))
        texto_botao = fonte.render("Jogar Novamente", True, (255, 255, 255))
        tela.blit(texto_botao, (botao_x + 20, botao_y + 10))

    # Atualiza a tela
    pygame.display.update()
    relogio.tick(60)

pygame.quit()
