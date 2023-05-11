import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, WHITE, BLACK
from checkers.game import Game
from checkers.board import Board
from poda_alpha_beta.algorithm import poda_alpha_beta, poda_alpha_beta1


FPS = 60
WIN = pygame.display.set_mode((850, 610))
depth=4


background_image = pygame.image.load('assets/fondo2.jpg')
background_image = pygame.transform.scale(background_image, (850, 610))

logo = pygame.image.load('assets/logo.png')
logo = pygame.transform.scale(logo, (150, 80))

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    if row >= 8 or col >= 8 or row < 0 or col < 0:
        return None, None
    return row, col


def menu():
    run = True
    while run:
        
        # Dibuja el fondo del menú
        WIN.fill((128, 128, 128))
        WIN.blit(background_image, (0, 0))
        WIN.blit(logo, (350, 500))
        # Dibuja los botones del menú
        pvp_button = pygame.Rect(190, 100, 500, 50)
        pve_button = pygame.Rect(190, 200, 500, 50)
        pygame.draw.rect(WIN, (84, 68, 102), pvp_button)
        pygame.draw.rect(WIN, (0, 255, 0), pve_button)
        
        # Dibuja el texto en los botones
        font = pygame.font.SysFont('comicsans', 30)
        pvp_text = font.render('Jugador contra Jugador', True, (255, 255, 255))
        pve_text = font.render('Jugador contra IA', True, (255, 255, 255))

        WIN.blit(pvp_text, (pvp_button.x + pvp_button.width // 2 - pvp_text.get_width() // 2, pvp_button.y + pvp_button.height // 2 - pvp_text.get_height() // 2))
        WIN.blit(pve_text, (pve_button.x + pve_button.width // 2 - pve_text.get_width() // 2, pve_button.y + pve_button.height // 2 - pve_text.get_height() // 2))
        #cREANDO BOTON DE ai vs ai
        ia_vs_ia_button = pygame.Rect(190, 300, 500, 50)
        pygame.draw.rect(WIN, (0, 0, 255), ia_vs_ia_button)

        ia_vs_ia_text = font.render('IA contra IA', True, (255, 255, 255))
        WIN.blit(ia_vs_ia_text, (ia_vs_ia_button.x + ia_vs_ia_button.width // 2 - ia_vs_ia_text.get_width() // 2, ia_vs_ia_button.y + ia_vs_ia_button.height // 2 - ia_vs_ia_text.get_height() // 2))
        
        # Actualiza la pantalla
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pvp_button.collidepoint(event.pos):
                    # Inicia un juego PvP
                    run = False
                    game = Game(WIN)
                    game_loop(game)
                elif pve_button.collidepoint(event.pos):
                    # Inicia un juego PvE
                    run = False
                    game = Game(WIN)
                    game_loop(game, ai_player=True)
                elif ia_vs_ia_button.collidepoint(event.pos):
                    # Inicia un juego IA vs IA
                    run = False
                    game = Game(WIN)
                    game_loop(game, ai_player=False, ai_vs_ai=True)


def get_depth():
    text_input = ''
    # Solicitar al usuario la profundidad deseada
    font = pygame.font.SysFont('comicsans', 30)
    text = font.render('Introduzca la profundidad deseada (1-10):', True, (255, 255, 255))
    input_rect = pygame.Rect(150, 100, 500, 50)
    pygame.draw.rect(WIN, (128, 128, 128), input_rect)
    pygame.draw.rect(WIN, (255, 255, 255), input_rect, 2)
    WIN.blit(text, (120, 50))
    pygame.display.update()

    depth = None
    while depth is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    try:
                        depth = int(text_input)
                        print("valor introducido ",text_input)
                        if depth < 1 or depth > 10:
                            text_input = ''
                            depth = None
                            raise ValueError
                    except ValueError:
                        # Si el usuario ingresa un valor inválido, borrar el texto ingresado y seguir solicitando
                        text_input = ''
                        text = font.render('Valor inválido. Introduzca un número entero del 1 al 10:', True, (255, 0, 0))
                        pygame.draw.rect(WIN, (128, 128, 128), input_rect)
                        pygame.draw.rect(WIN, (255, 255, 255), input_rect, 2)
                        WIN.blit(text, (20, 150))
                        pygame.display.update()
                        pygame.time.wait(1000)
                elif event.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]
                else:
                    text_input += event.unicode
                # Mostrar el texto ingresado en la pantalla
                input_text = font.render(text_input, True, (255, 255, 255))
                pygame.draw.rect(WIN, (128, 128, 128), input_rect)
                WIN.blit(input_text, (input_rect.x + 5, input_rect.y + 5))
                pygame.display.update()
    return depth


def show_winner_screen(winner, game):
    run = True
    while run:
        # Dibuja el fondo de la pantalla de ganador
        # ...
        pygame.init()
        pygame.display.set_caption('Winner!')
        # Crear una ventana
        winner_screen = pygame.display.set_mode((850, 610))
        
        # Mostrar el mensaje del ganador en la ventana
        font = pygame.font.SysFont('comicsans', 30)
        text = font.render(f'{winner}', True, (255, 255, 255))
        winner_screen.blit(text, (70, 280))
        
        # Actualizar la pantalla
            # Dibuja el botón de regreso
        #pygame.display.update()
        back_button = pygame.Rect(50, 50, 200, 50)
        pygame.draw.rect(WIN, (255, 255, 255), back_button)
        font = pygame.font.SysFont('comicsans', 30)
        back_text = font.render('Regresar', True, (0, 0, 0))
        WIN.blit(back_text, (back_button.x + back_button.width // 2 - back_text.get_width() // 2, back_button.y + back_button.height // 2 - back_text.get_height() // 2))
        
        WIN.blit(logo, (350, 500))
        # Actualiza la pantalla
        pygame.display.update()
        # Espera a que el usuario haga clic en el botón de regreso
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    run = False
                    menu()
   
def show_winner_screen1(winner):
    # Inicializar pygame
    pygame.init()
    pygame.display.set_caption('Winner!')
    
    # Crear una ventana
    winner_screen = pygame.display.set_mode((850, 610))
    
    # Mostrar el mensaje del ganador en la ventana
    font = pygame.font.SysFont('comicsans', 30)
    text = font.render(f'{winner}', True, (255, 255, 255))
    winner_screen.blit(text, (70, 280))
    
    # Actualizar la pantalla
    pygame.display.flip()
    
    # Esperar a que se cierre la ventana
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                


def game_loop(game, ai_player=False, ai_vs_ai=False):
    
    run = True
    clock = pygame.time.Clock()
    if ai_player==True or ai_vs_ai==True:
        depth=get_depth()

    verbose=False
    
    while run:
        clock.tick(FPS)
       
        if ai_player and game.turn == WHITE:
           
           # Llamada a la función poda_alpha_beta con verbose=True
           #evaluation, best_move = poda_alpha_beta(game.get_board(), 3, float('-inf'), float('inf'), True, game, True)
           eval, new_board = poda_alpha_beta(game.get_board(), depth, float('-inf'), float('inf'), True, game, verbose)
           print(f"La mejor jugada tiene una evaluación de {eval}")
           game.ai_move(new_board)
        
        
        
        elif ai_vs_ai:
            # Alternar entre ambos jugadores IA
            if game.turn == WHITE:
                # Mover jugador IA blanco
                eval, new_board = poda_alpha_beta(game.get_board(), depth, float('-inf'), float('inf'), True, game, verbose)
                print(f"La mejor jugada tiene una evaluación de {eval}")
                game.ai_move(new_board)
            else:
                # Mover jugador IA negro
                #print("entro a negro")
                eval, new_board = poda_alpha_beta1(game.get_board(), depth, float('-inf'), float('inf'), False, game, verbose)
                print(f"La mejor jugada tiene una evaluación de {eval}")
                game.ai_move(new_board)
        winner = game.winner()
        if winner is not None:
            show_winner_screen(winner, game)
            run = False
            
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                if row is not None and col is not None:
                    # Intenta mover la pieza del jugador actual
                    if not ai_player and not ai_vs_ai:
                        game.select(row, col)
                    elif ai_player and game.turn == BLACK:
                        game.select(row, col)
    
        game.update()
        board = game.get_board()
        font = pygame.font.SysFont('comicsans', 30)
        black_count = font.render(f"Rojas: {board.black_left}", True, (255, 255, 255))
        white_count = font.render(f"Moradas: {board.white_left}", True, (255, 255, 255))
        turn = font.render(f"Turno: {'Rojas' if game.turn == BLACK else 'Moradas'}", True, (255, 255, 255))
        WIN.blit(white_count, (620, 80))
        WIN.blit(turn, (620, 180))
        WIN.blit(black_count, (620, 280))
        WIN.blit(logo, (650, 500))
        
        
        
        pygame.display.update()

    pygame.quit()


def main():
    pygame.init()
    pygame.display.set_caption('Checkers')
    menu()

main()
