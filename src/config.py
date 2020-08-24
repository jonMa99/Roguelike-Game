from constant import *
import game
import pygame
import sprite
import entity_generator
import gamemap
import camera
import pathfinding
import fov

pygame.init()

SURFACE_MAIN = pygame.display.set_mode(RESOLUTION, pygame.RESIZABLE)
CLOCK = pygame.time.Clock()
# Load in all the sprites
SPRITE = sprite.GameSprites()

# Save this
CURRENT_FLOOR = 1
# Save this
TURN_COUNT = 0

# Save this
MAP_INFO = gamemap.MapInfo()

CAMERA = camera.Camera(MAP_INFO)

PATHFINDING = pathfinding.Graph()
PATHFINDING.make_graph(MAP_INFO)
PATHFINDING.neighbour()

# Save this
PLAYER = entity_generator.generate_player(MAP_INFO.map_tree)
# Initialized in game

# Save this
GAME_DATA = None

FOV = fov.new_fov(MAP_INFO)

PARTICLE_LIST = []

WALL_HACK = False

MINIMAP = False

