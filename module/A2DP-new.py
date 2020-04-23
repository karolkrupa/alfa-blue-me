from bluetooth.Manger import defaultManger
from bluetooth.objects.Player import Player
from bluetooth.objects.Device import Device


class A2DP:
    __player: Player = None

    def __init__(self):
        if defaultManger.device_manager.get_active_device().has_player():
            self.set_player(defaultManger.device_manager.get_active_device().get_player())

    def set_player(self, player: Player):
        self.__player = player

        self.__player.event_bus.on('properties-changed', self.__on_player_props_change)

    def __on_player_props_change(self, arg):
        pass

    def set_device(self, device: Device):
        self.__player = device.get_player()