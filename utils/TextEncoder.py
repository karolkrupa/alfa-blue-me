import math

dictornay = {
    "0": "000001",
    "1": "000010",
    "2": "000011",
    "3": "000100",
    "4": "000101",
    "5": "000110",
    "6": "000111",
    "7": "001000",
    "8": "001001",
    "9": "001010",
    ".": "001011",
    "A": "001100",
    "B": "001101",
    "C": "001110",
    "D": "001111",
    "E": "010000",
    "F": "010001",
    "G": "010010",
    "H": "010011",
    "I": "010100",
    "J": "010101",
    "K": "010110",
    "L": "010111",
    "M": "011000",
    "N": "011001",
    "O": "011010",
    "P": "011011",
    "Q": "011100",
    "R": "011101",
    "S": "011110",
    "T": "011111",
    "U": "100000",
    "V": "100001",
    "W": "100010",
    "X": "100011",
    "Y": "100100",
    "Z": "100101",
    "ñ": "100110",
    "ç": "100111",
    " ": "101000",
    "Ğ": "101001",
    "i": "101010",
    "j": "101011",
    "§": "101100",
    "À": "101101",
    "Ä": "101110",
    "ŭ": "101111",
    "Ü": "110000",
    "_": "110010",
    "?": "110101",
    "°": "110110",
    "!": "110111",
    "+": "111000",
    "-": "111001",
    ":": "111010",
    "/": "111011",
    "#": "111100",
    "*": "111101",
    "\r": "000000",
    "\n": "111111"
}


def __init__(self):
    pass


def encode(message: str, message_target):
    binary = __convert_to_binary(message)
    bytes_array = __convert_binary_to_bytes(binary)
    return __create_frames_from_bytes(bytes_array, message_target)


def __convert_to_binary(text) -> str:
    encoded = ''
    print(text)
    text = remove_accents(text.upper())

    for letter in text:
        if letter not in dictornay:
            encoded += dictornay['_']
        else:
            encoded += dictornay[letter]
    encoded += '000000'
    return encoded


def remove_accents(input_text):
    strange = 'ŮôῡΒძěἊἦëĐᾇόἶἧзвŅῑἼźἓŉἐÿἈΌἢὶЁϋυŕŽŎŃğûλВὦėἜŤŨîᾪĝžἙâᾣÚκὔჯᾏᾢĠфĞὝŲŊŁČῐЙῤŌὭŏყἀхῦЧĎὍОуνἱῺèᾒῘᾘὨШūლἚύсÁóĒἍŷöὄЗὤἥბĔõὅῥŋБщἝξĢюᾫაπჟῸდΓÕűřἅгἰშΨńģὌΥÒᾬÏἴქὀῖὣᾙῶŠὟὁἵÖἕΕῨčᾈķЭτἻůᾕἫжΩᾶŇᾁἣჩαἄἹΖеУŹἃἠᾞåᾄГΠКíōĪὮϊὂᾱიżŦИὙἮὖÛĮἳφᾖἋΎΰῩŚἷРῈĲἁéὃσňİΙῠΚĸὛΪᾝᾯψÄᾭêὠÀღЫĩĈμΆᾌἨÑἑïოĵÃŒŸζჭᾼőΣŻçųøΤΑËņĭῙŘАдὗპŰἤცᾓήἯΐÎეὊὼΘЖᾜὢĚἩħĂыῳὧďТΗἺĬὰὡὬὫÇЩᾧñῢĻᾅÆßшδòÂчῌᾃΉᾑΦÍīМƒÜἒĴἿťᾴĶÊΊȘῃΟúχΔὋŴćŔῴῆЦЮΝΛῪŢὯнῬũãáἽĕᾗნᾳἆᾥйᾡὒსᾎĆрĀüСὕÅýფᾺῲšŵкἎἇὑЛვёἂΏθĘэᾋΧĉᾐĤὐὴιăąäὺÈФĺῇἘſგŜæῼῄĊἏØÉПяწДĿᾮἭĜХῂᾦωთĦлðὩზკίᾂᾆἪпἸиᾠώᾀŪāоÙἉἾρаđἌΞļÔβĖÝᾔĨНŀęᾤÓцЕĽŞὈÞუтΈέıàᾍἛśìŶŬȚĳῧῊᾟάεŖᾨᾉςΡმᾊᾸįᾚὥηᾛġÐὓłγľмþᾹἲἔбċῗჰხοἬŗŐἡὲῷῚΫŭᾩὸùᾷĹēრЯĄὉὪῒᾲΜᾰÌœĥტ'
    ascii_replacements = 'UoyBdeAieDaoiiZVNiIzeneyAOiiEyyrZONgulVoeETUiOgzEaoUkyjAoGFGYUNLCiIrOOoqaKyCDOOUniOeiIIOSulEySAoEAyooZoibEoornBSEkGYOapzOdGOuraGisPngOYOOIikoioIoSYoiOeEYcAkEtIuiIZOaNaicaaIZEUZaiIaaGPKioIOioaizTIYIyUIifiAYyYSiREIaeosnIIyKkYIIOpAOeoAgYiCmAAINeiojAOYzcAoSZcuoTAEniIRADypUitiiIiIeOoTZIoEIhAYoodTIIIaoOOCSonyKaAsSdoACIaIiFIiMfUeJItaKEISiOuxDOWcRoiTYNLYTONRuaaIeinaaoIoysACRAuSyAypAoswKAayLvEaOtEEAXciHyiiaaayEFliEsgSaOiCAOEPYtDKOIGKiootHLdOzkiaaIPIIooaUaOUAIrAdAKlObEYiINleoOTEKSOTuTEeiaAEsiYUTiyIIaeROAsRmAAiIoiIgDylglMtAieBcihkoIrOieoIYuOouaKerYAOOiaMaIoht'
    translator = str.maketrans(strange, ascii_replacements)
    return input_text.translate(translator)


def __convert_binary_to_bytes(binary: str) -> [int]:
    bytes_array = []
    encode_index = 0
    while encode_index < len(binary):
        bytes_array.append(int(binary[encode_index:encode_index + 8], 2))
        encode_index += 8
    return bytes_array


def __create_frames_from_bytes(bytes_array: [], message_target):
    frames_count = math.ceil(len(bytes_array) / 6) - 1
    current_frame = [__get_frames_count_byte(frames_count, 0), message_target]
    frames_stack = [current_frame]
    for byte in bytes_array:
        if len(current_frame) >= 8:
            current_frame = [__get_frames_count_byte(frames_count, len(frames_stack)), message_target]
            frames_stack.append(current_frame)
        current_frame.append(byte)

    while (len(current_frame) < 8):
        current_frame.append(0x00)

    return frames_stack


def __get_frames_count_byte(frames_count, current_frame):
    return int('0x' + str(frames_count) + str(current_frame), 16)
