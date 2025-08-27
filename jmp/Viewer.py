from Validator import Validator
import pygame
import math


#############################
#COLORS
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (137, 12, 37)
GREEN = (30, 89, 39)
BLUE = (16, 48, 124)
BLUE2 = (17, 170, 178)
#############################

class Node:
    def __init__(self, id, type, pos, color):
        global idsFont

        self.id = id
        self.type = type
        self.pos = pos
        self.color = color
        self.idText = idsFont.render(self.id, True, (0, 0, 0))#, (255, 255, 255))
        self.radius = 35

    def setPos(self, pos):
        self.pos = pos

    def Draw(self, canvas):
        pygame.draw.circle(canvas, self.color, self.pos, self.radius)
        canvas.blit(self.idText, (self.pos[0]-self.radius + 5, self.pos[1] - 5))


class NodesDraw:
    def __init__(self, canvas):
        self.canvas = canvas
        self.nodes = {}
        self.connections = []
        self.nodesCount = {"Controller" : 0, "Host" : 0, "Switch" : 0}

        self.radius = 250
        self.angle = 0
        self.__getNextPos()

    def addNode(self, id, type):
        self.nodes[id] = Node(id, type, self.nextPos, self.__getColor(type))
        self.__calculatePositions()

    def addConnection(self, id1, id2):
        self.connections.append((id1,id2))
        self.__calculatePositions()

    def drawTopology(self):
        for link in self.connections:
            pygame.draw.line(self.canvas, BLACK, self.nodes[link[0]].pos, self.nodes[link[1]].pos, 3)
        for node in self.nodes.keys():
            self.nodes[node].Draw(self.canvas)

    def __calculatePositions(self):
        if self.nodesCount["Controller"] == 1:
            self.__calculatePosSingleController()
            return
        self.angle = 0
        for node in sorted(self.nodes.keys()):
            self.__getNextPos()
            self.nodes[node].setPos(self.nextPos)

    def __getColor(self, type):
        if type == "Host":
            self.nodesCount["Host"] += 1
            return RED
        elif type == "Switch":
            self.nodesCount["Switch"] += 1
            return BLUE
        elif type == "OVS":
            self.nodesCount["Switch"] += 1
            return BLUE2
        elif type == "Controller":
            self.nodesCount["Controller"] += 1
            return GREEN

    def __getNextPos(self):
        self.nextPos = (400 + int(self.radius * math.sin(math.radians(self.angle))), 300 + int(self.radius * math.cos(math.radians(self.angle))))
        if len(self.nodes.keys()) != 0:
            self.angle += 360/len(self.nodes.keys())

    def __calculatePosSingleController(self):
        #definir controller bem na esquerda
        x = 50
        for node in self.nodes.keys():
            if (self.nodes[node].type == "Controller"):
                self.nodes[node].setPos((x, 300))
        #depois, definir o(s) switch(s) logo na direita dele
        x = 300
        n = self.nodesCount["Switch"]
        space = 600/n
        count = 0
        for node in self.nodes.keys():
            if self.nodes[node].type == "Switch" or self.nodes[node].type == "OVS":
                y = space * count
                self.nodes[node].setPos((x, int(y + space / 2)))
                self.__positionHosts(self.nodes[node].id, y, x + 300, space)
                count += 1

    def __positionHosts(self, switchId, baseY, x, height):
        #pegar todos os filhos do switch
        children = []
        for node in self.nodes.keys():
            if self.nodes[node].type == "Host":
                for link in self.connections:
                    if (link[0] == self.nodes[node].id and link[1] == switchId) or (link[1] == self.nodes[node].id and link[0] == switchId):
                        children.append(self.nodes[node].id)
        #posicionar filhos
        if len(children) == 0:
            return
        count = 0
        space = height/len(children)
        for node in children:
            y = space * count + space / 2
            self.nodes[node].setPos((x,int(baseY + y)))
            count += 1


#############################
class Viewer:
    def __init__(self, hosts, switches, ovs, controllers, connections):
        global idsFont
        
        pygame.init()
        pygame.font.init()
        self.gameDisplay = pygame.display.set_mode((800,600))
        pygame.display.set_caption("JuMP Topology Viewer")
        self.clock = pygame.time.Clock()
        idsFont = pygame.font.SysFont("arial", 20)
        self.nodes = NodesDraw(self.gameDisplay)
        

        for host in hosts:
            self.nodes.addNode(host.ID, "Host")

        for switch in switches:
            self.nodes.addNode(switch.ID, "Switch")

        for vswitch in ovs:
            self.nodes.addNode(vswitch.ID, "OVS")
            self.nodes.addConnection(str(vswitch.ID), str(vswitch.CONTROLLER))

        for controller in controllers:
            self.nodes.addNode(controller.ID, "Controller")

        for connection in connections:
            self.nodes.addConnection(str(connection["OUT/IN"]), str(connection["IN/OUT"]))


    def view(self):
        self.__mainLoop()
        pygame.quit()
        quit()

    def __mainLoop(self):
        gameExit = False

        while not gameExit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.gameDisplay.fill(WHITE)
            self.nodes.drawTopology()
            pygame.display.update()
            self.clock.tick(30)
