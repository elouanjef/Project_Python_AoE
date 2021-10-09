from settings import HUD_COLOUR, WHITE, graphics_folder
import pygame as pg
from .utils import draw_text
from os import path

class Hud:

    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.hud_colour = HUD_COLOUR

        #resource hud
        self.resources_surface = pg.Surface((width, height * 0.02), pg.SRCALPHA)
        self.resources_rect = self.resources_surface.get_rect(topleft = (0, 0))
        self.resources_surface.fill(self.hud_colour)

        #building hud
        self.build_surface = pg.Surface((width * 0.15, height * 0.25), pg.SRCALPHA)
        self.build_rect = self.build_surface.get_rect(topleft = (self.width * 0.84, self.height * 0.74))
        self.build_surface.fill(self.hud_colour)

        #select hud
        self.select_surface = pg.Surface((width * 0.3, height * 0.2), pg.SRCALPHA)
        self.select_rect = self.select_surface.get_rect(topleft = (self.width * 0.35, self.height * 0.79))    
        self.select_surface.fill(self.hud_colour)


        self.images = self.load_images()


        #create a new hud
        self.tiles = self.create_build_hud()

        self.selected_tile = None




    #afficher les batiments pour choisir et construire
    def create_build_hud(self):

        #position in the inventory
        render_pos = [self.width * 0.84 + 10,self.height * 0.74 + 10]
        object_width = self.build_surface.get_width() // 8

        tiles =[]
        #print('create_build_hud')
        for image_name, image in self.images.items():   #ajouter l'image dans la fonction load_image()
            #print('in for create_build_hud')
            pos = render_pos.copy()
            image_tmp = image.copy()
            image_scale = self.scale_image(image_tmp, w = object_width)
            #choose the rect around the entity
            rect = image_scale.get_rect(topleft = pos)

            tiles.append(
                {
                    "name": image_name,
                    "icon": image_scale,
                    "image": self.images[image_name],
                    "rect": rect
                    #on peut ajouter plusieuse attibutes ici
                }
            )

            #positionn in inventory for each entity
            render_pos[0] += image_scale.get_width() + 10


        return tiles


    def update(self):
        #work in inventory
        mouse_pos = pg.mouse.get_pos()
        mouse_action = pg.mouse.get_pressed()
        #unselect entity
        if mouse_action[2]:
            self.selected_tile = None

        for tile in self.tiles:

            if tile["rect"].collidepoint(mouse_pos):
            #tile["rect"] is defined in create_build_hud() 
                if mouse_action[0]:
                    self.selected_tile = tile
                    


    def draw(self, screen):

        # if self.selected_tile is not None:
        #     img = self.selected_tile["image"].copy()
        #     img.set_alpha(100)
        #     screen.blit(img, pg.mouse.get_pos())

        #resource 
        screen.blit(self.resources_surface, (0, 0))
        #build hud
        screen.blit(self.build_surface, (self.width * 0.84, self.height * 0.74))
        #select hud
        screen.blit(self.select_surface, (self.width * 0.35, self.height * 0.79))




        #icon for entity selecting
        for tile in self.tiles:
            screen.blit(tile["icon"], tile["rect"].topleft)




        #resource
        pos = self.width - 420                                           #resource info position
        for resource in ["wood:{}".format(500), "stone:{}".format(250), "gold:{}".format(100),"food: {}".format(230)]:
            draw_text(screen, resource, 25, WHITE, (pos, 0))
            pos += 100







    def load_images(self):

        #read images
        #all images are saved in folder assets/graphics
        building1 = pg.image.load(path.join(graphics_folder,"building01.png"))
        building2 = pg.image.load(path.join(graphics_folder,"building02.png"))
        tree = pg.image.load(path.join(graphics_folder,"tree.png"))
        rock = pg.image.load(path.join(graphics_folder,"rock.png"))



        #load des images  d'unites ici
        #example: troop = pg.image.load(path.join.(graphic_folder,"le nom de fichier"))




        #on peut l'appeller sous le nom "image_name" comme dans la ligne 63
        images = {
            "building1": building1,
            "building2": building2,
            "tree": tree,
            "rock": rock
            #ajouter les images d'unites ici
            #example "troop": troop;
        }

        return images


    def scale_image(self, image, w = None, h = None):

        if (w == None) and (h == None):
            pass
        elif h == None:
            scale = w / image.get_width()
            h = scale * image.get_height()
            image = pg.transform.scale(image, (int(w), int(h)))
        elif w == None:
            scale = h / image.get_height()
            w = scale * image.get_width()
            image = pg.transform.scale(image, (int(w), int(h)))
        else:
            image = pg.transform.scale(image, (int(w), int(h)))


        return image
