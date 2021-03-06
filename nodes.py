import random, pygame, math

pygame.font.init()

class Node:
    def __init__(self, name, max_width, max_height) -> None:
        self.name = name
        self.pos = random.randint(50, max_width-50), random.randint(50, max_height-50)
        self.links = {}
        self.used = False
        font = pygame.font.SysFont(None, 24)
        self.img = font.render(name, True, (0, 0, 100))
    
    def connect(self, node):
        self.links[node.name] = node
        node.links[self.name] = self
    
    def disconnect(self, node):
        self.links.pop(node.name)
        node.links.pop(self.name)
    
    def find_path(self, name, path, limit=None):
        
        path.append(self)
        
        for anode in self.links.values():
            if anode.name == name:
                path.append(anode)
                print(f'(a procura do {name}){self.name} achou nos imediatos')
                self.used = False
                return path

        print(f'(a procura do {name}){self.name} não achou nos imediatos')

        if limit is not None:
            if self.weight(path) >= limit:
                print(f'passou do limite {limit}')
                return path

        valids = []

        self.used = True

        for anode in self.links.values():
            if not anode.used:
                print(f'(a procura do {name}){self.name} tenta {anode.name}')
                res = anode.find_path(name, path.copy(), limit)
                if res[-1].name == name:
                    limit = self.weight(res)
                    valids.append(res)
        
        if valids:
            print('valids: ', [[x.name for x in y] for y in valids])
            self.used = False

            return min(valids, key=self.weight)

        self.used = False
        return path

    @staticmethod
    def weight(path):
        path1 = path[:-1]
        path2 = path[1:]
        return sum([math.hypot(node1.pos[0]-node2.pos[0], node1.pos[1]-node2.pos[1]) for node1, node2 in zip(path1, path2)])
            


