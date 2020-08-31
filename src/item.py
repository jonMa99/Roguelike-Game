import menu
from constant import *
import config
import game_text
import entity_generator
import json


with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data/item.json')) as f:
    data = json.load(f)


class Equipment:
    def __init__(self, strength_bonus=0, defense_bonus=0, wizardry_bonus=0, hp_bonus=0, mp_bonus=0, slot=None):
        """
        Class representing item bonus stats and slot it occupies

        Only items considered equipment will have equipment field in their
        parent entity

        Args:
            strength_bonus (int): Strength bonus item gives
            defense_bonus (int): Defense bonus item gives
            wizardry_bonus (int): Magic power bonus item gives
            hp_bonus (int): Max hp bonus item gives
            mp_bonus (int): Max hp bonus item gives
            slot (String): Slot item occupies
        """
        self.strength_bonus = strength_bonus
        self.defense_bonus = defense_bonus
        self.wizardry_bonus = wizardry_bonus
        self.hp_bonus = hp_bonus
        self.mp_bonus = mp_bonus
        self.slot = slot
        self.equipped = False
        self.owner = None

    def toggle_equip(self):
        """
        Toggles equipped status of item
        """
        if self.equipped:
            self.unequip()
        else:
            self.equip()

    def unequip(self):
        """
        Unequips item
        """
        equipped_dict = self.owner.item.current_container.owner.creature.equipment
        equipped_dict[self.slot] = None
        self.equipped = False
        game_text.add_game_message_to_print("Unequipped item", WHITE)

        self.owner.item.current_container.inventory.append(self.owner)

        # self.equipped = False
        # game_text.add_game_message_to_print("Unequipped item", WHITE)

    def equip(self):
        """
        Equips item if slot is free, else does nothing
        """
        equipped_dict = self.owner.item.current_container.owner.creature.equipment

        if equipped_dict[self.slot] == None:
            equipped_dict[self.slot] = self.owner
            self.equipped = True
            game_text.add_game_message_to_print("Equipped item", WHITE)
            self.owner.item.current_container.inventory.remove(self.owner)
        else:
            game_text.add_game_message_to_print("Slot equipped already", RED)



        # item_entities = self.owner.item.current_container.equipped_items
        #
        # for item in item_entities:
        #     if item.equipment and item.equipment.slot == self.slot:
        #         game_text.add_game_message_to_print("Slot equipped already", RED)
        #         return
        #
        # self.equipped = True
        # game_text.add_game_message_to_print("Equipped item", WHITW)



class Item:
    def __init__(self, name, weight=0.0, volume=0.0):
        """
        Class that represents an item

        Attributes:
            name (arg, String): Name of item
            weight (arg, Int): Weight of item
            volume (arg, Int): Volume of item
            owner (Entity): Owner of item component
            current_container (Container): Container that is currently
                holding item
            use_item_args (List): Args for use_item
            hover_args (Tuple): Args for hovering over item
            drop_item_args (Tuple): Args for dropping item
        """
        self.name = name
        self.weight = weight
        self.volume = volume
        self.owner = None
        self.current_container = None
        self.use_item_args = None
        self.hover_args = None
        self.drop_item_args = None

        self._load_item_values()

    def _load_item_values(self):
        if self.name in data.keys():
            dict = data[self.name]
            args = tuple(dict.values())
            self.use_item_args = args


    def pick_up(self, entity):
        """
        Entity (Player/Creature Object) with container picks up item if
        the current volume of container + item is < container.volume
        Add item to inventory
        Remove item from game_objects

        Args:
            entity (Entity): Entity that is going to pick up item
        """
        if entity.container:
            if entity.container.volume + self.volume > entity.container.volume:
                game_text.add_game_message_to_print("Inventory Full", WHITE)
            else:
                game_text.add_game_message_to_print("Picked Up " + self.name, WHITE)
                entity.container.inventory.append(self.owner)

                config.GAME_DATA.item_data.remove(self.owner)

                self.current_container = entity.container

    def drop_item(self, entity):
        """
        Drop item at entity's position x and y
        Update position and rect of item to player.x,player,y
        Remove item from inventory
        Add item to game_objects

        Args:
            entity (Entity): Entity that is dropping the item
        """
        config.GAME_DATA.item_data.insert(0, self.owner)
        entity.container.inventory.remove(self.owner)
        self.current_container = None
        self.owner.x = entity.x
        self.owner.y = entity.y
        game_text.add_game_message_to_print(self.name + " Item Dropped", WHITE)

    def use_item(self):
        """
        Uses item and produces affect and removes it

        If self is an consumable item (ie no equipment field in entity owner)
        use item, else equip item
        """
        # If item is not equipment
        if not self.owner.equipment:
            use_fn = item_use_dict[self.name]
            if use_fn:
                use_fn(self.current_container.owner, self.use_item_args)
                self.current_container.inventory.remove(self.owner)
                self.current_container = None
        # Item is equipment
        else:
            use_fn = self.owner.equipment.toggle_equip
            use_fn()

    def hover_over_item(self):
        """
        Draws white box with item name on top of item
        when hovering over it

        Variables:
            button_x (int): x coord of IconButton item is in
            button_y (int): y coord of IconButton item is in
            offset_x (int): Where GridButtonManager is (needed for finding where to
                place hover box)
            offset_y (int): Where GridButtonManager is (needed for finding where to
                place hover box)
        """
        button_x, button_y, offset_x, offset_y = self.hover_args
        # Single line text
        # item_button = menu.TextButton(self.name, (BUTTON_WIDTH, BUTTON_HEIGHT),
        #                               # offset_x + x makes it so center of text is GridButtonManager x + button x
        #                               # offset_y + y is to make text centered vertically and the - (SPRITE_SIZE // 2)
        #                               #      is to make it so text isn't covering item since TextButton is always centered
        #                               (offset_x + button_x, offset_y + button_y - (SPRITE_SIZE // 2)),
        #                               WHITE)
        #
        # item_button.draw()
        # Multiline text
        rect = pygame.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT * 2)
        surface = game_text.multiLineSurface(self.name + "\n \n" + data[self.name]["desc"], FONT_ITEM_DESCRIPTION, rect, BLACK, WHITE, 1)
        surface_rect = surface.get_rect()
        surface_rect.center = (offset_x + button_x, offset_y + button_y - BUTTON_HEIGHT)
        config.SURFACE_MAIN.blit(surface, surface_rect)


    def drop_item_fn_pointer(self):
        """
        Drops item at entity's feet
        """
        entity = self.drop_item_args
        self.drop_item(entity)


# Change it so if at max hp, it heals for 0
def heal_user_hp(user_entity, args):
    """
    Heals user_entity's hp for value in item.json under Red Potion

    Args:
        user_entity (Entity): Entity using item
        args (List): List of data from item.json
    """
    heal = args[0]
    user_entity.creature.stat.heal_hp(heal)
    game_text.add_game_message_to_print(user_entity.creature.name_instance + " healed " + str(heal) + " hp",
                                        WHITE)


# Change it so if at max mp, it heals for 0
def heal_user_mp(user_entity, args):
    """
    Heals user_entity's mp for value in item.json under Blue Potion

    Args:
        user_entity (Entity): Entity using item
        args (List): List of data from item.json
    """
    heal = args[0]
    user_entity.creature.stat.heal_mp(heal)
    game_text.add_game_message_to_print(user_entity.creature.name_instance + " healed " + str(heal) + " mp",
                                        WHITE)


def teleport_user(user_entity, args):
    """
    Teleports user_entity to random location

    Args:
        user_entity (Entity): Entity using item
        args (List): List of data from item.json (not used in this method)
    """
    x, y = entity_generator.generate_player_spawn(config.MAP_INFO.map_tree)
    user_entity.x, user_entity.y = x, y
    game_text.add_game_message_to_print(user_entity.creature.name_instance + " teleported",
                                        BLUE)

def equip_item(user_entity, args):
    pass




# Lookup table for item effect when used
item_use_dict = {
    "Red Potion": heal_user_hp,
    "Blue Potion": heal_user_mp,
    "Teleport Scroll": teleport_user
}