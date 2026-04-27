import pygame
from datetime import datetime
from tools import flood_fill, draw_shape, WHITE, BLACK


pygame.init()

WIDTH, HEIGHT = 1000, 700
TOOLBAR_HEIGHT = 80

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS2 Paint Application")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)

canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
canvas.fill(WHITE)

current_color = BLACK
brush_size = 5

tool = "pencil"

drawing = False
start_pos = None
last_pos = None

text_mode = False
text_position = None
text_buffer = ""

colors = [
    BLACK,
    (255, 0, 0),
    (0, 150, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 165, 0),
    (128, 0, 128),
    WHITE
]

tools = [
    "pencil",
    "line",
    "rectangle",
    "circle",
    "square",
    "right_triangle",
    "equilateral_triangle",
    "rhombus",
    "fill",
    "text",
    "eraser"
]


def canvas_pos(pos):
    x, y = pos
    return x, y - TOOLBAR_HEIGHT


def is_inside_canvas(pos):
    x, y = pos
    return y >= TOOLBAR_HEIGHT


def save_canvas():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"canvas_{timestamp}.png"
    pygame.image.save(canvas, filename)
    print(f"Saved: {filename}")


def draw_toolbar():
    pygame.draw.rect(screen, (220, 220, 220), (0, 0, WIDTH, TOOLBAR_HEIGHT))

    x = 10

    for t in tools:
        color = (180, 180, 180)
        if tool == t:
            color = (120, 180, 255)

        rect = pygame.Rect(x, 10, 95, 28)
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 1)

        label = font.render(t[:10], True, BLACK)
        screen.blit(label, (x + 5, 15))

        x += 100

    x = 10
    y = 45

    for c in colors:
        rect = pygame.Rect(x, y, 28, 28)
        pygame.draw.rect(screen, c, rect)
        pygame.draw.rect(screen, BLACK, rect, 1)

        if c == current_color:
            pygame.draw.rect(screen, (0, 0, 0), rect, 3)

        x += 35

    size_text = font.render(f"Brush: {brush_size}px | 1=2px 2=5px 3=10px | Ctrl+S Save", True, BLACK)
    screen.blit(size_text, (330, 50))


def handle_toolbar_click(pos):
    global tool, current_color

    x, y = pos

    if y <= 40:
        index = x // 100
        if 0 <= index < len(tools):
            tool = tools[index]

    elif 45 <= y <= 73:
        color_index = (x - 10) // 35
        if 0 <= color_index < len(colors):
            current_color = colors[color_index]


running = True

while running:
    screen.fill(WHITE)
    screen.blit(canvas, (0, TOOLBAR_HEIGHT))

    preview_surface = canvas.copy()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Keyboard shortcuts
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                brush_size = 2
            elif event.key == pygame.K_2:
                brush_size = 5
            elif event.key == pygame.K_3:
                brush_size = 10

            elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                save_canvas()

            elif text_mode:
                if event.key == pygame.K_RETURN:
                    rendered_text = font.render(text_buffer, True, current_color)
                    canvas.blit(rendered_text, text_position)
                    text_mode = False
                    text_buffer = ""

                elif event.key == pygame.K_ESCAPE:
                    text_mode = False
                    text_buffer = ""

                elif event.key == pygame.K_BACKSPACE:
                    text_buffer = text_buffer[:-1]

                else:
                    text_buffer += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if event.pos[1] < TOOLBAR_HEIGHT:
                    handle_toolbar_click(event.pos)
                else:
                    pos = canvas_pos(event.pos)

                    if tool == "fill":
                        flood_fill(canvas, pos[0], pos[1], current_color)

                    elif tool == "text":
                        text_mode = True
                        text_position = pos
                        text_buffer = ""

                    else:
                        drawing = True
                        start_pos = pos
                        last_pos = pos

        if event.type == pygame.MOUSEMOTION:
            if drawing and is_inside_canvas(event.pos):
                pos = canvas_pos(event.pos)

                if tool == "pencil":
                    pygame.draw.line(canvas, current_color, last_pos, pos, brush_size)
                    last_pos = pos

                elif tool == "eraser":
                    pygame.draw.line(canvas, WHITE, last_pos, pos, brush_size)
                    last_pos = pos

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drawing:
                end_pos = canvas_pos(event.pos)

                if tool not in ["pencil", "eraser"]:
                    draw_shape(canvas, tool, current_color, start_pos, end_pos, brush_size)

                drawing = False
                start_pos = None
                last_pos = None

    # Live preview for line and shapes
    if drawing and start_pos and pygame.mouse.get_pressed()[0]:
        mouse_pos = pygame.mouse.get_pos()

        if is_inside_canvas(mouse_pos) and tool not in ["pencil", "eraser"]:
            end_pos = canvas_pos(mouse_pos)
            draw_shape(preview_surface, tool, current_color, start_pos, end_pos, brush_size)
            screen.blit(preview_surface, (0, TOOLBAR_HEIGHT))

    # Text preview
    if text_mode and text_position:
        rendered_text = font.render(text_buffer, True, current_color)
        screen.blit(rendered_text, (text_position[0], text_position[1] + TOOLBAR_HEIGHT))

    draw_toolbar()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

print("START")