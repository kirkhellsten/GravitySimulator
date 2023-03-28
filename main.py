
import sys, pygame
import math
import time, random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BACKGROUND_COLOR = (46, 52, 64)

SUN_COLOR = (255, 255, 0)
PROJECTILE_COLOR = (0, 0, 255)

GRAVITATIONAL_CONSTANT = 9.81

VELOCITY_REDUCTION_FACTOR = 0.15

FPS = 30
fpsClock = pygame.time.Clock()

class Utils:

    @staticmethod
    def xComponent(component, angle):
        return math.cos(angle)*component

    @staticmethod
    def yComponent(component, angle):
        return math.sin(angle)*component

    @staticmethod
    def calculateAngle(cp1, cp2):
        a = cp1[0] - cp2[0]
        b = cp1[1] - cp2[1]
        if cp1[0] - cp2[0] < 0:
            angle = math.atan(b/a) + math.pi
        else:
            angle = math.atan(b / a)
        return angle

    @staticmethod
    def calculateRadius(cp1, cp2):
        a = abs(cp2[0] - cp1[0])
        b = abs(cp2[1] - cp1[1])
        c = math.sqrt(a**2+b**2)
        return c

    @staticmethod
    def forceOfGravity(m1, m2, r):
        fgrav = (GRAVITATIONAL_CONSTANT*m1*m2) / r**2
        return fgrav

class Renderer:

    @staticmethod
    def __drawBackground():
        screen.fill(BACKGROUND_COLOR)

    @staticmethod
    def __drawSuns():
        for sun in Sun.suns:
            pygame.draw.circle(screen, SUN_COLOR, (sun.centerPosition[0], sun.centerPosition[1]), sun.radius)

    @staticmethod
    def __drawProjectiles():
        for projectile in Projectile.projectiles:
            pygame.draw.circle(screen, PROJECTILE_COLOR, (projectile.centerPosition[0], projectile.centerPosition[1]), projectile.radius)


    @staticmethod
    def draw():

        Renderer.__drawBackground()
        Renderer.__drawProjectiles()
        Renderer.__drawSuns()


class Projectile:
    def __init__(self, cx, cy, mass=1, radius=5):
        self.centerPosition = [cx,cy]
        self.mass = mass
        self.radius = radius
        self.velocity = [0,0]

    def updateVelocity(self, xComponent, yComponent):
        self.velocity[0] += xComponent
        self.velocity[1] += yComponent

    def update(self):
        self.centerPosition[0] += self.velocity[0]
        self.centerPosition[1] += self.velocity[1]

class Sun:
    def __init__(self, cx, cy, mass=1000, radius=15):
        self.centerPosition = [cx,cy]
        self.mass = mass
        self.radius = radius

class GameWorld:

    @staticmethod
    def init():

        Sun.suns = []
        Projectile.projectiles = []

    @staticmethod
    def reset():
        return None


    @staticmethod
    def quit():
        return None

    @staticmethod
    def __updateProjectilesToSun():
        for sun in Sun.suns:
            for projectile in Projectile.projectiles:
                radius = Utils.calculateRadius(sun.centerPosition, projectile.centerPosition)

                fgrav = Utils.forceOfGravity(sun.mass, projectile.mass, radius)

                angle = Utils.calculateAngle(sun.centerPosition, projectile.centerPosition)

                xComponent = Utils.xComponent(fgrav, angle)
                yComponent = Utils.yComponent(fgrav, angle)

                projectile.updateVelocity(xComponent, yComponent)

                projectile.update()

    @staticmethod
    def update():
        GameWorld.__updateProjectilesToSun()


if __name__ == '__main__':

    size = SCREEN_WIDTH, SCREEN_HEIGHT
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Gravity Simulator")

    prev_time = time.time()

    GameWorld.init()

    running = True

    mouseStartPos = []
    mouseEndPos = []

    while running:

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mousePressed = pygame.mouse.get_pressed()

                if mousePressed[0] == True:
                    mouseStartPos = [pos[0],pos[1]]


                if mousePressed[2] == True:
                    sun = Sun(pos[0],pos[1])
                    Sun.suns.append(sun)

            elif event.type == pygame.MOUSEBUTTONUP:
                if mousePressed[0] == True:
                    mouseEndPos = [pos[0], pos[1]]
                    projectile = Projectile(pos[0],pos[1])
                    projectile.updateVelocity((mouseStartPos[0]-mouseEndPos[0])*VELOCITY_REDUCTION_FACTOR,
                                              (mouseStartPos[1]-mouseEndPos[1])*VELOCITY_REDUCTION_FACTOR)
                    Projectile.projectiles.append(projectile)

        GameWorld.update()
        Renderer.draw()

        pygame.display.flip()
        fpsClock.tick(FPS)

    GameWorld.quit()
