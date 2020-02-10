import math

dictornay = {
    '\r': '000000',
    '0': '000001',
    '1': '000010',
    '2': '000011',
    '3': '000100',
    '4': '000101',
    '5': '000110',
    '6': '000111',
    '7': '001000',
    '8': '001001',
    '9': '001010',
    '.': '001011',
    'A': '001100',
    'B': '001101',
    'C': '001110',
    'D': '001111',
    'E': '010000',
    'F': '010001',
    'G': '010010',
    'H': '010011',
    'I': '010100',
    'J': '010101',
    'K': '010110',
    'L': '010111',
    'M': '011000',
    'N': '011001',
    'O': '011010',
    'P': '011011',
    'Q': '011100',
    'R': '011101',
    'S': '011110',
    'T': '011111',
    'U': '100000',
    'V': '100001',
    'W': '100010',
    'K': '100011',
    'Y': '100100',
    'Z': '100101',
    'ñ': '100110',
    'ç': '100111',
    ' ': '101000',
    'Ğ': '101001',
    'i': '101010',
    'j': '101011',
    '§': '101100',
    'À': '101101',
    'Ä': '101110',
    'ŭ': '101111',
    'Ü': '110000',
    '9': '110001',
    '_': '110010',
    '_': '110011',
    '_': '110100',
    '?': '110101',
    '°': '110110',
    '!': '110111',
    '+': '111000',
    '-': '111001',
    ':': '111010',
    '/': '111011',
    '#': '111100',
    '*': '111101',
    '_': '111110',
    '\n': '111111'
}


def encode(text, type = 0x02):
    encoded = ''
    for letter in text:
        encoded += dictornay[letter.upper()]
    encoded += '000000'

    print(encoded)

    # msg = [0, 0x02]
    msg = []
    encodeIndex = 0
    while encodeIndex < len(encoded):
        # print(int(encoded[encodeIndex:encodeIndex+8], 2))
        msg.append(int(encoded[encodeIndex:encodeIndex + 8], 2))
        encodeIndex += 8

    frameCount = math.ceil(len(msg) / 6) - 1
    currentFrame = [int('0x' + str(frameCount) + '0', 16), type]
    frameStack = [currentFrame]
    for byte in msg:
        if len(currentFrame) >= 8:
            currentFrame = [int('0x' + str(frameCount) + str(len(frameStack)), 16), type]
            frameStack.append(currentFrame)
        currentFrame.append(byte)

    while (len(currentFrame) < 8):
        currentFrame.append(0x00)

    return frameStack