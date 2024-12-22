from IntComputer.computer import IntComputer
import pygame

program = [int(num) for num in open("program.txt").read().split(",")]
program[0] = 2
c = IntComputer(program, True, True)
finished = c.run_program()
pygame.init()
boxX = boxY = 10
screenX = screenY = 500
screen = pygame.display.set_mode([screenX, screenY])
screen.fill((210, 251, 255))
score = 0
ball_pos = paddle_pos = 0
out = c.piped_output
while not finished:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
            break

    inp = 0
    if ball_pos > paddle_pos:
        inp = 1
    elif ball_pos < paddle_pos:
        inp = -1
    c.piped_input.append(inp)
    finished = c.run_program()
    print(score)

    screen.fill((210, 251, 255))
    screen.fill((150,170,60))

    while c.piped_output:
        x,y, tile = c.piped_output.pop(0), c.piped_output.pop(0), c.piped_output.pop(0)
        if x == -1 and y == 0:
            score = tile
        else:
            color = (255,255,255)
            if tile == 0:
                color = (161, 228, 255)
            elif tile == 1:
                color = (204, 131, 108)
            elif tile == 2:
                color = (108, 126, 204)
            elif tile == 3:
                color = (35,57,153)
                paddle_pos = x
            elif tile == 4:
                color = (250,187,149)
                ball_pos = x
            else:
                print("something is wrong")
                exit()

            rect = pygame.draw.rect(screen, color, [x*boxX, y*boxY, boxX, boxY])

    pygame.display.flip()
    pygame.time.Clock().tick(60)

print(score)
