
from gpiozero import LED

led = LED(22)

codigo_morse = {'a': '.- ',
                'b': '-... ',
                'c': '-.-. ',
                'd': '-.. ',
                'e': '. ',
                'f': '..-. ',
                'g': '--. ',
                'h': '.... ',
                'i': '.. ',
                'j': '.--- ',
                'k': '-.- ',
                'l': '.-.. ',
                'm': '-- ',
                'n': '-. ',
                'o': '--- ',
                'p': '.--. ',
                'q': '--.- ',
                'r': '.-. ',
                's': '... ',
                't': '- ',
                'u': '..- ',
                'v': '...- ',
                'w': '.-- ',
                'x': '-..- ',
                'y': '-.-- ',
                'z': '--.. ',
                }


palavra = input("Digite a palavra para ser transformada em codigo morse: ")
palavra_morse = ""

global indice
indice = 0


def pisca_morse():
    global indice
    if palavra_morse[indice] == ".":
        led4.blink(n=1, on_time=0.150, off_time=0)
    elif palavra_morse[indice] == '-':
        led4.blink(n=1, on_time=0.55, off_time=0)
    else:
        led4.blink(n=1, on_time=0, off_time=0.7)
    indice += 1
    if indice < len(palavra):
        timer = Timer(1, pisca_morse)
        timer.start()


for letra in palavra:
    palavra_morse += codigo_morse[letra]
    print("palavra ate agora: ", palavra_morse)

timer = Timer(1, pisca_morse)
timer.start()
