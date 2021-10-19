import time
import pygame as pg
from settings import *
from os import path
#from units import *

# from tqdm import tqdm


class Unite:
    batiment = False
    soldat = False
    villageois = False
    alive = False
    type = False
    name = False
    res = [0, 0, 0, 0]

    def __init__(self, name, type):
        self.name = name
        self.type = type
        if str(self.type) in ("cavalerie", "infanterie", "artillerie"):
            self.soldat = True
            self.alive = True
        elif str(self.type) in ("batiment"):
            self.batiment = True
            self.alive = True
        elif str(self.type) in ("villageois"):
            self.villageois = True
            self.alive = True
        else:
            print("Il faut choisir un type valable")


def militaire(nb, troop, type, res, t):
    # test_resource(res)
    armee = {}
    for i in range(nb):
        time.sleep(t)
        armee[i] = Unite(troop, type)
        print("Vous avez enrôlé", i + 1, str(troop), "de type", str(type), "pour", res[0], "de bois",
              res[1], "de pierre", res[2], "d'or et", res[3], "de nourriture")
    return armee


def villager(nb):
    # test_resource(res)
    villageois = {}
    res = [0, 0, 0, 50]
    for i in range(nb):
        time.sleep(3)
        villageois[i] = Unite("villageois", "villageois")
        print("Villageois créé pour", res[3], "de nourriture")
    return villageois


def construire(name, res, t):
    # test_resource(res)
    time.sleep(t)
    construction = Unite(name, 'batiment')
    print("Vous avez bâti un(e)", str(name), "pour", res[0], "de bois",
          res[1], "de pierre", res[2], "d'or et", res[3], "de nourriture")
    return construction


# [ WOOD , ROCK , GOLD , FOOD ]
units_res = {
    # caserne
    'archer': [0, 0, 30, 20],
    'arbaletrier': [0, 0, 20, 45],
    'piquier': [30, 0, 0, 30],
    'fantassin': [25, 0, 35, 0],

    # usine
    'canon_lourd': [150, 0, 80, 0],
    'couleuvrine': [200, 0, 80, 0],

    # ecurie
    'chevalier': [0, 0, 100, 75],
    'uhlan': [0, 0, 75, 60],

    # batiments
    'centre_ville': [600, 0, 0, 0],
    'caserne': [150, 0, 0, 0],
    'usine': [200, 0, 0, 0],
    'moulin': [150, 0, 0, 0],
    'ecurie': [175, 0, 0, 0],
    'plantation': [800, 0, 0, 0]
}

units_time = {
    # caserne
    'archer': 3,
    'arbaletrier': 3,
    'piquier': 4,
    'fantassin': 5,

    # usine
    'canon_lourd': 30,
    'couleuvrine': 30,

    # ecurie
    'chevalier': 12,
    'uhlan': 10,

    # batiments
    'centre_ville': 60,
    'caserne': 40,
    'usine': 40,
    'moulin': 30,
    'ecurie': 40,
    'plantation': 30
}

units_age = {
    # caserne
    'archer': 1,
    'arbaletrier': 1,
    'piquier': 1,
    'fantassin': 2,

    # usine
    'canon_lourd': 2,
    'couleuvrine': 2,

    # ecurie
    'chevalier': 2,
    'uhlan': 1,

    # batiments
    'centre_ville': 1,
    'caserne': 1,
    'usine': 2,
    'moulin': 1,
    'ecurie': 1,
    'plantation': 2
}


def caserne(nb, troop):
    militaire(nb, troop, 'infanterie', units_res[str(troop)], units_time[str(troop)])


def usine(nb, troop):
    militaire(nb, troop, 'artillerie', units_res[str(troop)], units_time[str(troop)])


def ecurie(nb, troop):
    militaire(nb, troop, 'cavalerie', units_res[str(troop)], units_time[str(troop)])


def batiment(nom):
    construire(nom, units_res[str(nom)], units_time[str(nom)])


caserne(1, "archer")

ecurie(1, 'uhlan')

batiment('moulin')

usine(1, 'canon_lourd')

villager(3)

class Archer:

    def __init__(self, pos):
        image = pg.image.load(path.join(graphics_folder, "unit01.png"))
        self.image = image
        self.name = "Archer"
        self.rect = self.image.get_rect(topleft=pos)
        # [ WOOD , ROCK , GOLD , FOOD ]
        self.attack = 3
        self.range = 5
        self.res = [20, 0, 0, 40]
        self.health = 35

    def update(self):
        if self.health != 0:
            self.health -= 1

class Infantryman:

    def __init__(self, pos):
        image = pg.image.load(path.join(graphics_folder, "unit03.png"))
        self.image = image
        self.name = "Infantryman"
        self.rect = self.image.get_rect(topleft=pos)
        # [ WOOD , ROCK , GOLD , FOOD ]
        self.attack = 7
        self.range = 0
        self.res = [0, 0, 15, 35]
        self.health = 40

    def update(self):
        if self.health != 0:
            self.health -= 1

class Cavalry:

    def __init__(self, pos):
        image = pg.image.load(path.join(graphics_folder, "unit04.png"))
        self.image = image
        self.name = "Cavalry"
        self.rect = self.image.get_rect(topleft=pos)
        # [ WOOD , ROCK , GOLD , FOOD ]
        self.attack = 8
        self.range = 0
        self.res = [0, 0, 80, 70]
        self.health = 150

    def update(self):
        if self.health != 0:
            self.health -= 1

class Catapult:

    def __init__(self, pos):
        image = pg.image.load(path.join(graphics_folder, "unit05.png"))
        self.image = image
        self.name = "Catapult"
        self.rect = self.image.get_rect(topleft=pos)
        # [ WOOD , ROCK , GOLD , FOOD ]
        self.attack = 60
        self.range = 12
        self.res = [180, 0, 80, 0]
        self.health = 75

    def update(self):
        if self.health != 0:
            self.health -= 1

#Pour l'instant j'ai mis unit0?.png pour le sprite de chaque unité, il faudra renommer les sprites de cette manière.
