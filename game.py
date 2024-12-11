import pygame
from random import randint
from objects import Board, Button

### SETUP *********************************************************************
pygame.init()
SCREEN = WIDTH, HEIGHT = 890, 480
win = pygame.display.set_mode(SCREEN, pygame.NOFRAME)
pygame.display.set_caption('Memory Puzzle')

clock = pygame.time.Clock()
FPS = 30

ROWS, COLS = 8, 10
TILESIZE = 45

### COLORS ********************************************************************
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 25, 25)
WHITE = (255, 255, 255)

### LOADING IMAGES ************************************************************
img_list = []
for img in range(1, 21):
    image = pygame.image.load(f"Assets/icons/{img}.jpg")
    image = pygame.transform.scale(image, (TILESIZE, TILESIZE))
    img_list.append(image)

bg = pygame.image.load('Assets/bg.jpg')
game_won = pygame.image.load('Assets/won.png')
rightbar = pygame.image.load('Assets/image.jpg')
rightbar = pygame.transform.scale(rightbar, (280, HEIGHT - 47))

### Buttons *******************************************************************
restart_img = pygame.image.load('Assets/restart.png')
restart_btn = Button(restart_img, (40, 40), 720, 230)

close_img = pygame.image.load('Assets/close.png')
close_btn = Button(close_img, (40, 40), 720, 280)

### LOADING FONTS *************************************************************
sys_font = pygame.font.SysFont(("Times New Roman"), 20)
clicks_font = pygame.font.SysFont(("Algerian"), 30)

### CREATING BOARD ************************************************************
board = Board(img_list)
board.randomize_images()

animated_boxes = [(randint(0, 7), randint(0, 9)) for i in range(20)]

### GAME VARIABLES ************************************************************
game_screen = True
first_card = None
second_card = None
first_click_time = None
second_click_time = None
numCards = 80
isLoading = True
animation_on = True
animation_count = 0

gameWon = False
numClicks = 0

running = True

while running:
    win.blit(bg, (0, 0), (400, 100, WIDTH, HEIGHT))
    win.blit(rightbar, (595, 20))
    pygame.draw.rect(win, BLUE, (5, 10, 580, HEIGHT - 20), 2)
    pygame.draw.rect(win, BLUE, (585, 10, 300, HEIGHT - 20), 2)

    # Restart Button
    if restart_btn.draw(win):
        game_screen = True
        first_card = None
        second_card = None
        first_click_time = None
        second_click_time = None

        board.randomize_images()

        isLoading = True
        animation_on = True
        animation_count = 0
        numClicks = 0
        numCards = 80
        gameWon = False

    # Close Button
    if close_btn.draw(win):
        running = False

    clicked = False

    x, y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                clicked = True
                x, y = pygame.mouse.get_pos()

    if game_screen:
        # Game logic here...
        if numCards == 0:
            gameWon = True

        if isLoading:
            # Preview card animation
            clicked = False

            if animation_count < 20:
                for index, pos in enumerate(animated_boxes):
                    card = board.board[pos[0]][pos[1]]
                    if card.cover_x >= TILESIZE:
                        card.visible = True
                        card.animate = True
                        card.slide_left = True

                    if card.cover_x <= 0:
                        card.animate = True
                        card.slide_left = False

                if card.animation_complete:
                    for pos in animated_boxes:
                        card = board.board[pos[0]][pos[1]]
                        card.visible = False
                        card.animate = False
                    animated_boxes = [(randint(0, 7), randint(0, 9)) for i in range(20)]
                    animation_count += 1
            else:
                isLoading = False
                animation_on = False
                animation_count = 0

        if not gameWon:
            # Polling time to hide cards
            if second_click_time:
                current_time = pygame.time.get_ticks()

                delta = current_time - second_click_time
                if delta >= 1000:
                    if first_card.value == second_card.value:
                        first_card.is_alive = False
                        second_card.is_alive = False
                        numCards -= 2

                    index = first_card.index
                    fcard = board.board[index[0]][index[1]]
                    fcard.animate = True
                    fcard.slide_left = False
                    first_card = None

                    index = second_card.index
                    scard = board.board[index[0]][index[1]]
                    scard.animate = True
                    scard.slide_left = False
                    second_card = None

                    first_click_time = None
                    second_click_time = None
                else:
                    clicked = False

            # Displaying cards
            for r in range(ROWS):
                for c in range(COLS):
                    border = False
                    card = board.board[r][c]
                    if card.is_alive:
                        xcord = card.rect.x
                        ycord = card.rect.y

                        if not isLoading:
                            if card.rect.collidepoint((x, y)):
                                border = True
                                if clicked:
                                    numClicks += 1
                                    card.visible = True
                                    card.animate = True
                                    card.slide_left = True

                                    if not first_card:
                                        first_card = card
                                    else:
                                        second_card = card
                                        if second_card != first_card:
                                            second_click_time = pygame.time.get_ticks()
                                        else:
                                            second_card = None

                        pygame.draw.rect(win, BLACK, (xcord+5, ycord+5, TILESIZE, TILESIZE))

                        if not card.animate:
                            if card.visible:
                                win.blit(card.image, card.rect)
                            else:
                                pygame.draw.rect(win, WHITE, (xcord, ycord, TILESIZE, TILESIZE))

                            if border and not isLoading:
                                pygame.draw.rect(win, RED, (xcord, ycord, TILESIZE, TILESIZE), 2)
                        else:
                            if isLoading:
                                speed = 5
                            else:
                                speed = 8
                            card.on_click(win, speed)
        else:
            win.blit(game_won, (50, 100))
            image = clicks_font.render(f'Number of Clicks : {numClicks}', 0, (0, 0, 0))
            win.blit(image, (150, 350))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
