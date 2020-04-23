from bluetooth.Manger import defaultManger
from bluetooth.objects.Player import Player
from bluetooth.objects.Device import Device


class A2DP:
    __player: Player = None

    __device_event_pointers = []
    __player_props_change_event = None

    def __init__(self):
        if defaultManger.device_manager.get_active_device().has_player():
            self.set_player(defaultManger.device_manager.get_active_device().get_player())

    def set_player(self, player: Player):
        self.__player = player

        if self.__player_props_change_event is not None:
            self.__player_props_change_event.off()

        self.__player_props_change_event = self.__player.event_bus.on('properties-changed', self.__on_player_props_change)

    def __on_player_props_change(self, arg):
        pass
