from constant import *
import config
import game_text
import entity_generator
import menu


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
            use_item_args (*args): Args for use_item
            hover_args (*args): Args for hovering over item
            drop_item_args (*args): Args for dropping item
        """
        self.name = name
        self.weight = weight
        self.volume = volume
        self.owner = None
        self.current_container = None
        self.use_item_args = None
        self.hover_args = None
        self.drop_item_args = None


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
        """
        use_fn = item_use_dict[self.name]
        if use_fn:
            use_fn(self.current_container.owner)
            self.current_container.inventory.remove(self.owner)
            self.current_container = None

    def hover_over_item(self):
        """
        Draws white box with item name on top of item
        when hovering over it

        Variables:
            button (IconButton): IconButton item is in
            offset_x (int): Where ButtonManager is (needed for finding where to
                place hover box)
            offset_y (int): Where ButtonManager is (needed for finding where to
                place hover box)
        """
        button, offset_x, offset_y = self.hover_args
        x, y = button.rect.topleft
        item_button = menu.TextButton(self.name, (BUTTON_WIDTH, BUTTON_HEIGHT),
                                      # offset_x + x makes it so center of text is ButtonManager x + button x
                                      # offset_y + y is to make text centered vertically and the - (SPRITE_SIZE // 2)
                                      #      is to make it so text isn't covering item since TextButton is always centered
                                      (offset_x + x, offset_y + y - (SPRITE_SIZE // 2)),
                                      WHITE)

        item_button.draw()

    def drop_item_fn_pointer(self):
        """
        Drops item at entity's feet
        """
        entity = self.drop_item_args
        self.drop_item(entity)


# Change it so if at max hp, it heals for 0
def heal_user_hp(user_entity, *args):
    user_entity.creature.stat.heal_hp(10)
    game_text.add_game_message_to_print(user_entity.creature.name_instance + " healed " + str(10) + " hp",
                                        WHITE)


# Change it so if at max mp, it heals for 0
def heal_user_mp(user_entity, *args):
    user_entity.creature.stat.heal_mp(5)
    game_text.add_game_message_to_print(user_entity.creature.name_instance + " healed " + str(5) + " mp",
                                        WHITE)


def teleport_user(user_entity, *args):
    x, y = entity_generator.generate_player_spawn(config.MAP_INFO.map_tree)
    user_entity.x, user_entity.y = x, y
    game_text.add_game_message_to_print(user_entity.creature.name_instance + " teleported",
                                        BLUE)


# Lookup table for item effect when used
item_use_dict = {
    "Red Potion": heal_user_hp,
    "Blue Potion": heal_user_mp,
    "Teleport Scroll": teleport_user,
    "Sword": None
}