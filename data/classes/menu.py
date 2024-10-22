import pygame


pygame.init()

WINDOW_SIZE = (700, 700)
screen = pygame.display.set_mode(WINDOW_SIZE)

screen.fill('white')
pygame.display.update()
tlac1 = pygame.Rect(200,200,300,100)
pygame.draw.rect(screen,"black",tlac1)
pygame.draw.rect(screen,"white",pygame.Rect(205,205,290,90))
font = pygame.font.SysFont('Arial', 50)
screen.blit(pygame.font.SysFont('Arial',100).render("Chess", True, "black"),(200,50))
screen.blit(font.render("Play", True, "black"),(300,225))
tlac1 = pygame.Rect(200,350,300,100)
pygame.draw.rect(screen,"black",tlac1)
pygame.draw.rect(screen,"white",pygame.Rect(205,355,290,90))
screen.blit(font.render("AI", True, "black"),(300,375))
	
running = True
	
while running:
	mx, my = pygame.mouse.get_pos()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				print("click")
	pygame.display.update()