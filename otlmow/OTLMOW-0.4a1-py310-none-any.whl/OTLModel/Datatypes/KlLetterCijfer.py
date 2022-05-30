# coding=utf-8
from OTLMOW.OTLModel.Datatypes.KeuzelijstField import KeuzelijstField
from OTLMOW.OTLModel.Datatypes.KeuzelijstWaarde import KeuzelijstWaarde


# Generated with OTLEnumerationCreator. To modify: extend, do not edit
class KlLetterCijfer(KeuzelijstField):
    """De mogelijke letters en cijfers voor een letter- of cijfermarkering."""
    naam = 'KlLetterCijfer'
    label = 'Letter-cijfer'
    objectUri = 'https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#KlLetterCijfer'
    definition = 'De mogelijke letters en cijfers voor een letter- of cijfermarkering.'
    codelist = 'https://wegenenverkeer.data.vlaanderen.be/id/conceptscheme/KlLetterCijfer'
    options = {
        '-': KeuzelijstWaarde(invulwaarde='-',
                              label='-',
                              definitie='Koppelteken.',
                              objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlLetterCijfer/-'),
        '0': KeuzelijstWaarde(invulwaarde='0',
                              label='0',
                              definitie='Cijfer 0.',
                              objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlLetterCijfer/0'),
        '1': KeuzelijstWaarde(invulwaarde='1',
                              label='1',
                              definitie='Cijfer 1.',
                              objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlLetterCijfer/1'),
        '2': KeuzelijstWaarde(invulwaarde='2',
                              label='2',
                              definitie='Cijfer 2.',
                              objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlLetterCijfer/2'),
        '3': KeuzelijstWaarde(invulwaarde='3',
                              label='3',
                              definitie='Cijfer 3.',
                              objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlLetterCijfer/3'),
        '4': KeuzelijstWaarde(invulwaarde='4',
                              label='4',
                              definitie='Cijfer 4.',
                              objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlLetterCijfer/4'),
        '5': KeuzelijstWaarde(invulwaarde='5',
                              label='5',
                              definitie='Cijfer 5.',
                              objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlLetterCijfer/5'),
        '6': KeuzelijstWaarde(invulwaarde='6',
                              label='6',
                              definitie='Cijfer 6.',
                              objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlLetterCijfer/6'),
        '7': KeuzelijstWaarde(invulwaarde='7',
                              label='7',
                              definitie='Cijfer 7.',
                              objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlLetterCijfer/7'),
        '8': KeuzelijstWaarde(invulwaarde='8',
                              label='8',
                              definitie='Cijfer 8.',
                              objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlLetterCijfer/8'),
        '9': KeuzelijstWaarde(invulwaarde='9',
                              label='9',
                              definitie='Cijfer 9.',
                              objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlLetterCijfer/9'),
        'a': KeuzelijstWaarde(invulwaarde='a',
                              label='a',
                              definitie='Letter a.',
                              objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlLetterCijfer/a'),
        'b': KeuzelijstWaarde(invulwaarde='b',
                              label='b',
                              definitie='Letter b.',
                              objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlLetterCijfer/b'),
        'c': KeuzelijstWaarde(invulwaarde='c',
                              label='c',
                              definitie='Letter c.',
                              objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlLetterCijfer/c'),
        'd': KeuzelijstWaarde(invulwaarde='d',
                              label='d',
                              definitie='Letter d.',
                              objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlLetterCijfer/d'),
        'e': KeuzelijstWaarde(invulwaarde='e',
                              label='e',
                              definitie='Letter e.',
                              objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlLetterCijfer/e'),
        'f': KeuzelijstWaarde(invulwaarde='f',
                              label='f',
                              definitie='Letter f.',
                              objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlLetterCijfer/f'),
        'g': KeuzelijstWaarde(invulwaarde='g',
                              label='g',
                              definitie='Letter g.',
                              objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlLetterCijfer/g'),
        'h': KeuzelijstWaarde(invulwaarde='h',
                              label='h',
                              definitie='Letter h.',
                              objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlLetterCijfer/h'),
        'i': KeuzelijstWaarde(invulwaarde='i',
                              label='i',
                              definitie='Letter i.',
                              objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlLetterCijfer/i'),
        'j': KeuzelijstWaarde(invulwaarde='j',
                              label='j',
                              definitie='Letter j.',
                              objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlLetterCijfer/j'),
        'k': KeuzelijstWaarde(invulwaarde='k',
                              label='k',
                              definitie='Letter k.',
                              objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlLetterCijfer/k'),
        'l': KeuzelijstWaarde(invulwaarde='l',
                              label='l',
                              definitie='Letter l.',
                              objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlLetterCijfer/l'),
        'm': KeuzelijstWaarde(invulwaarde='m',
                              label='m',
                              definitie='Letter m.',
                              objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlLetterCijfer/m'),
        'n': KeuzelijstWaarde(invulwaarde='n',
                              label='n',
                              definitie='Letter n.',
                              objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlLetterCijfer/n'),
        'o': KeuzelijstWaarde(invulwaarde='o',
                              label='o',
                              definitie='Letter o.',
                              objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlLetterCijfer/o'),
        'p': KeuzelijstWaarde(invulwaarde='p',
                              label='p',
                              definitie='Letter p.',
                              objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlLetterCijfer/p'),
        'q': KeuzelijstWaarde(invulwaarde='q',
                              label='q',
                              definitie='Letter q.',
                              objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlLetterCijfer/q'),
        'r': KeuzelijstWaarde(invulwaarde='r',
                              label='r',
                              definitie='Letter r.',
                              objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlLetterCijfer/r'),
        's': KeuzelijstWaarde(invulwaarde='s',
                              label='s',
                              definitie='Letter s.',
                              objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlLetterCijfer/s'),
        't': KeuzelijstWaarde(invulwaarde='t',
                              label='t',
                              definitie='Letter t.',
                              objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlLetterCijfer/t'),
        'u': KeuzelijstWaarde(invulwaarde='u',
                              label='u',
                              definitie='Letter u.',
                              objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlLetterCijfer/u'),
        'v': KeuzelijstWaarde(invulwaarde='v',
                              label='v',
                              definitie='Letter v.',
                              objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlLetterCijfer/v'),
        'w': KeuzelijstWaarde(invulwaarde='w',
                              label='w',
                              definitie='Letter w.',
                              objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlLetterCijfer/w'),
        'x': KeuzelijstWaarde(invulwaarde='x',
                              label='x',
                              definitie='Letter x.',
                              objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlLetterCijfer/x'),
        'y': KeuzelijstWaarde(invulwaarde='y',
                              label='y',
                              definitie='Letter y.',
                              objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlLetterCijfer/y'),
        'z': KeuzelijstWaarde(invulwaarde='z',
                              label='z',
                              definitie='Letter z.',
                              objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlLetterCijfer/z'),
        'â': KeuzelijstWaarde(invulwaarde='â',
                              label='â',
                              definitie='Letter â.',
                              objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlLetterCijfer/â'),
        'é': KeuzelijstWaarde(invulwaarde='é',
                              label='é',
                              definitie='Letter é.',
                              objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlLetterCijfer/é')
    }

