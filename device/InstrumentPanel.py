from device.Device import Device
import utils.TextEncoder as TextEncoder


class InstrumentPanel(Device):
    def display(self, text):
        pass

    def display_text_center(self, text):
        frames = TextEncoder.encode(' \n' + text, 0x02)
        self.send_frames(0x5E7, frames)
