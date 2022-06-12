from email.errors import NonPrintableDefect
from math import hypot
import pygame, nodes

def find():
    global path, nodes_list
    path = con_selected1.find_path(con_selected2, [])
    print([ x.name for x in path])
    print('-'*40, '\n'*3)
    clean_nodes()

def clean_nodes():
    for node in nodes_list:
        node.used = False

def draw_all_nodes():
    global nodes_list, screen

    screen.fill((255, 255, 255))

    for node in nodes_list:
        if node is selected:
            pygame.draw.circle(screen, (255, 0, 0), node.pos, 20)
        pygame.draw.circle(screen, (255, 0, 0), node.pos, 20, 3)

        screen.blit(node.img, node.pos)

        for lnode in node.links.values():
            try:
                if node in path and (lnode is path[path.index(node)-1] or lnode is path[path.index(node)+1]):
                    pygame.draw.line(screen, (255, 0, 0), node.pos, lnode.pos, 3)
                else:
                    pygame.draw.line(screen, (0, 0, 0), node.pos, lnode.pos)
            except Exception as error:
                pygame.draw.line(screen, (0, 0, 0), node.pos, lnode.pos)


    pygame.display.update()

screen = pygame.display.set_mode((800, 400), flags=pygame.RESIZABLE)

running = True

actual_id = 6

nodes_list = [nodes.Node(f'{x}', 800, 400) for x in range(6)]

nodes_list[0].connect(nodes_list[5])
nodes_list[0].connect(nodes_list[3])
nodes_list[0].connect(nodes_list[2])

nodes_list[1].connect(nodes_list[5])
nodes_list[1].connect(nodes_list[4])

nodes_list[2].connect(nodes_list[3])

nodes_list[3].connect(nodes_list[4])

con_selected1 = nodes_list[0]

con_selected2 = '4'

path = None
find()

print([ x.name for x in path])


selected: nodes.Node = None
actual_function = 'connect'

draw_all_nodes()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.WINDOWRESIZED:
            draw_all_nodes()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for node in nodes_list:
                if hypot(event.pos[0]-node.pos[0], event.pos[1]-node.pos[1]) < 20:
                    if actual_function == 'connect' and node is not selected and selected is not None:
                        if node.name in selected.links.keys():
                            selected.disconnect(node)
                        else:
                            selected.connect(node)
                        find()

                        selected = node
                    
                    if actual_function == 'selecting path' and node is not selected and selected is not None:
                        con_selected1 = selected
                        con_selected2 = node.name
                        selected = node
                        find()

                    if node is selected:
                        selected = None
                    else:
                        selected = node
                    
            
            draw_all_nodes()
        
        if event.type == pygame.MOUSEMOTION:
            if selected and actual_function == 'move':
                selected.pos = event.pos
                find()
                draw_all_nodes()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                actual_function = 'selecting path'
            
            if event.key == pygame.K_m:
                actual_function = 'move'

            if event.key == pygame.K_c:
                actual_function = 'connect'

            if event.key == pygame.K_a:
                nodes_list.append(nodes.Node(f'{actual_id}', 800, 400))
                actual_id += 1
                draw_all_nodes()
            
            if event.key == pygame.K_r:
                if selected is not None:
                    while selected.links.values():
                        selected.disconnect(list(selected.links.values())[0])
                    nodes_list.remove(selected)
                    selected = None
                    find()
                    draw_all_nodes()
                    


