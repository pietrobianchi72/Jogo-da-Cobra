import pygame
import random
import sys
import time

pygame.init()

largura = 600
altura = 400
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('🐍 Snake Avançado - Comidas, Níveis e Obstáculos')

PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
AMARELO = (255, 255, 0)
AZUL = (0, 0, 255)

tamanho_bloco = 20
velocidade_inicial = 10

fonte = pygame.font.SysFont('Arial', 25)
grande_fonte = pygame.font.SysFont('Arial', 40)
pequena_fonte = pygame.font.SysFont('Arial', 20)

comidas = [
    {"nome": "Maçã", "cor": VERMELHO, "pontos": 1},
    {"nome": "Banana", "cor": AMARELO, "pontos": 3},
    {"nome": "Mirtilo", "cor": AZUL, "pontos": 5},
]

def gerar_comida(obstaculos, corpo_cobra):
    while True:
        tipo = random.choice(comidas)
        x = random.randrange(0, largura - tamanho_bloco, tamanho_bloco)
        y = random.randrange(0, altura - tamanho_bloco, tamanho_bloco)
        if [x, y] not in obstaculos and [x, y] not in corpo_cobra:
            return {"x": x, "y": y, "cor": tipo["cor"], "pontos": tipo["pontos"]}

def gerar_obstaculos(nivel, corpo_cobra):
    obstaculos = []
    for _ in range(nivel * 3):
        while True:
            x = random.randrange(0, largura - tamanho_bloco, tamanho_bloco)
            y = random.randrange(0, altura - tamanho_bloco, tamanho_bloco)
            if [x, y] not in corpo_cobra:
                obstaculos.append([x, y])
                break
    return obstaculos

def mostrar_info(pontos, nivel):
    texto = fonte.render(f"Pontuação: {pontos}   Nível: {nivel}", True, BRANCO)
    tela.blit(texto, [10, 10])

def tela_inicial():
    while True:
        tela.fill(PRETO)
        titulo = grande_fonte.render("🐍 Snake Avançado", True, VERDE)
        instrucao = fonte.render("Pressione ESPAÇO para começar a partida", True, BRANCO)
        tela.blit(titulo, titulo.get_rect(center=(largura // 2, 50)))
        tela.blit(instrucao, instrucao.get_rect(center=(largura // 2, 100)))

        y_offset = 150
        texto_comidas = fonte.render("Comidas e Pontuações:", True, BRANCO)
        tela.blit(texto_comidas, (30, y_offset))

        for i, comida in enumerate(comidas):
            pygame.draw.rect(tela, comida["cor"], (30, y_offset + 30 + i * 40, tamanho_bloco, tamanho_bloco))
            texto = pequena_fonte.render(f"{comida['nome']} = {comida['pontos']} pontos", True, BRANCO)
            tela.blit(texto, (70, y_offset + 30 + i * 40))

        y_obs = y_offset + 30 + len(comidas)*40 + 20
        texto_obs = fonte.render("Obstáculos:", True, BRANCO)
        tela.blit(texto_obs, (30, y_obs))
        pygame.draw.rect(tela, BRANCO, (30, y_obs + 30, tamanho_bloco, tamanho_bloco))
        texto_obs_info = pequena_fonte.render("Barras brancas - não encoste!", True, BRANCO)
        tela.blit(texto_obs_info, (70, y_obs + 30))

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    return

def contagem_regressiva():
    for i in range(3, 0, -1):
        tela.fill(PRETO)
        texto = grande_fonte.render(f"Iniciando em {i}...", True, BRANCO)
        texto_rect = texto.get_rect(center=(largura // 2, altura // 2))
        tela.blit(texto, texto_rect)
        pygame.display.update()
        time.sleep(1)

def tela_game_over():
    while True:
        tela.fill(PRETO)
        texto = grande_fonte.render("Game Over!", True, VERMELHO)
        subtexto = fonte.render("Espaço - Reiniciar | Q - Sair", True, BRANCO)
        tela.blit(texto, texto.get_rect(center=(largura // 2, altura // 2 - 30)))
        tela.blit(subtexto, subtexto.get_rect(center=(largura // 2, altura // 2 + 20)))
        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif evento.key == pygame.K_SPACE:
                    return

def jogar():
    tela_inicial()
    contagem_regressiva()

    x = largura // 2
    y = altura // 2
    x_mudanca = tamanho_bloco
    y_mudanca = 0

    corpo_cobra = []
    comprimento_cobra = 3

    pontos = 0
    nivel = 1
    velocidade = velocidade_inicial
    clock = pygame.time.Clock()

    obstaculos = gerar_obstaculos(nivel, corpo_cobra)
    comida = gerar_comida(obstaculos, corpo_cobra)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT and x_mudanca == 0:
                    x_mudanca = -tamanho_bloco
                    y_mudanca = 0
                elif evento.key == pygame.K_RIGHT and x_mudanca == 0:
                    x_mudanca = tamanho_bloco
                    y_mudanca = 0
                elif evento.key == pygame.K_UP and y_mudanca == 0:
                    y_mudanca = -tamanho_bloco
                    x_mudanca = 0
                elif evento.key == pygame.K_DOWN and y_mudanca == 0:
                    y_mudanca = tamanho_bloco
                    x_mudanca = 0

        x += x_mudanca
        y += y_mudanca

        cabeca = [x, y]
        corpo_cobra.append(cabeca)
        if len(corpo_cobra) > comprimento_cobra:
            del corpo_cobra[0]

        if x < 0 or x >= largura or y < 0 or y >= altura or cabeca in corpo_cobra[:-1] or cabeca in obstaculos:
            tela_game_over()
            return

        if x == comida["x"] and y == comida["y"]:
            pontos += comida["pontos"]
            comprimento_cobra += 1

            novo_nivel = pontos // 10 + 1
            if novo_nivel > nivel:
                nivel = novo_nivel
                obstaculos = gerar_obstaculos(nivel, corpo_cobra)
                velocidade = velocidade_inicial + (nivel - 1) * 2

            comida = gerar_comida(obstaculos, corpo_cobra)

        tela.fill(PRETO)

        pygame.draw.rect(tela, comida["cor"], [comida["x"], comida["y"], tamanho_bloco, tamanho_bloco])

        for obs in obstaculos:
            pygame.draw.rect(tela, BRANCO, [obs[0], obs[1], tamanho_bloco, tamanho_bloco])

        for parte in corpo_cobra:
            pygame.draw.rect(tela, VERDE, [parte[0], parte[1], tamanho_bloco, tamanho_bloco])

        mostrar_info(pontos, nivel)
        pygame.display.update()
        clock.tick(velocidade)

while True:
    jogar()
