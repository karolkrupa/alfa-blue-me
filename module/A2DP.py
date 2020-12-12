from bluetooth.Manger import defaultManger, deviceManager
from device.Radio import radio, DisplayMode
from module.EventBus import mainEventBus
import subprocess
from bluetooth.objects.Device import Device


class A2DP:
    _interact_with_player = True
    _bluealsa_process = None

    def __init__(self):
        defaultManger.get_device_manager().event_bus.on(
            'bt-device-manager:active-device:active-player:properties-changed',
            self.__on_player_props_change
        )
        self.__register_steering_wheel_events()
        self.__register_player_change_event()
        self.__register_player_enabled_event()

    def play(self):
        if not self._can_interact_with_player():
            return

        self._get_active_player().play()

    def toggle_play(self):
        if not self._can_interact_with_player():
            return

        if self._get_active_player().is_playing():
            self.pause()
        else:
            self.play()

    def pause(self):
        if not self._can_interact_with_player():
            return

        self._get_active_player().pause()

    def next(self):
        if not self._can_interact_with_player():
            return

        self._get_active_player().next()

    def previous(self):
        if not self._can_interact_with_player():
            return

        self._get_active_player().previous()

    def _is_player(self):
        if not deviceManager.has_active_device():
            return False

        return deviceManager.get_active_device().has_player()

    def _can_interact_with_player(self):
        return self._is_player() and self._interact_with_player

    def _get_active_player(self):
        return deviceManager.get_active_device().get_player()

    def __on_player_props_change(self, arg):
        changed = arg['changed']  # type: dict
        if 'Track' in changed:
            track = changed['Track']  # type: dict
            if not track.get('Artist', False) and not track.get('Title', False):
                return
            self.__display_track_name(track.get('Artist', ''), track.get('Title', ''))

    def __display_track_name(self, artist, title):
        if artist:
            radio.set_display_mode(DisplayMode.artists)
        else:
            radio.set_display_mode(DisplayMode.text)

        radio.set_first_field(artist)
        radio.set_second_filed(title)
        radio.display()

    def __register_steering_wheel_events(self):
        mainEventBus.on('steering-wheel:next', lambda args: self.next())
        mainEventBus.on('steering-wheel:prev', lambda args: self.previous())
        mainEventBus.on('steering-wheel:mute', lambda args: self.toggle_play())

    def __register_player_change_event(self):
        mainEventBus.on(
            'bt-device-manager:active-device',
            lambda args: self._on_device_change(args['device'])
        )

    def __register_player_enabled_event(self):
        mainEventBus.on(
            'status-manager:media-player-enabled',
            lambda args: self.__on_player_enabled_change(args['enabled'])
        )

    def __on_player_enabled_change(self, enabled: bool):
        if enabled:
            self.play()
        else:
            self.pause()

    def _on_device_change(self, device: Device):
        if self._bluealsa_process:
            self._bluealsa_process.kill()
            self._bluealsa_process.wait()
        self._bluealsa_process = subprocess.Popen(
            # 'exec bluealsa-aplay --pcm-buffer-time=10000000 ' + device.get_address(),
            'exec bluealsa-aplay ' + device.get_address(),
            shell=True,
        )


a2dp = A2DP()
