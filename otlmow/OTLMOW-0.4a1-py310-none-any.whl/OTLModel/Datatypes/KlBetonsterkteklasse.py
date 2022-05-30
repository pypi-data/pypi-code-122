# coding=utf-8
from OTLMOW.OTLModel.Datatypes.KeuzelijstField import KeuzelijstField
from OTLMOW.OTLModel.Datatypes.KeuzelijstWaarde import KeuzelijstWaarde


# Generated with OTLEnumerationCreator. To modify: extend, do not edit
class KlBetonsterkteklasse(KeuzelijstField):
    """De klasse waarin de sterkte van beton wordt uitgedrukt."""
    naam = 'KlBetonsterkteklasse'
    label = 'Betonsterkteklasse'
    objectUri = 'https://wegenenverkeer.data.vlaanderen.be/ns/implementatieelement#KlBetonsterkteklasse'
    definition = 'De klasse waarin de sterkte van beton wordt uitgedrukt.'
    codelist = 'https://wegenenverkeer.data.vlaanderen.be/id/conceptscheme/KlBetonsterkteklasse'
    options = {
        'c-12-15': KeuzelijstWaarde(invulwaarde='c-12-15',
                                    label='C12/15',
                                    definitie='C van Concrete (Beton). 12 is de karakteristieke druksterkte bij beproeving op cilinders. 15 is de karakteristieke druksterkte bij beproeving op kubussen. Beiden uitgedrukt in MPa.',
                                    objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlBetonsterkteklasse/c-12-15'),
        'c-16-20': KeuzelijstWaarde(invulwaarde='c-16-20',
                                    label='C16/20',
                                    definitie='C van Concrete (Beton). 16 is de karakteristieke druksterkte bij beproeving op cilinders. 20 is de karakteristieke druksterkte bij beproeving op kubussen. Beiden uitgedrukt in MPa.',
                                    objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlBetonsterkteklasse/c-16-20'),
        'c-20-25': KeuzelijstWaarde(invulwaarde='c-20-25',
                                    label='C20/25',
                                    definitie='C van Concrete (Beton). 20 is de karakteristieke druksterkte bij beproeving op cilinders. 25 is de karakteristieke druksterkte bij beproeving op kubussen. Beiden uitgedrukt in MPa.',
                                    objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlBetonsterkteklasse/c-20-25'),
        'c-25-30': KeuzelijstWaarde(invulwaarde='c-25-30',
                                    label='C25/30',
                                    definitie='C van Concrete (Beton). 25 is de karakteristieke druksterkte bij beproeving op cilinders. 30 is de karakteristieke druksterkte bij beproeving op kubussen. Beiden uitgedrukt in MPa.',
                                    objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlBetonsterkteklasse/c-25-30'),
        'c-28-35': KeuzelijstWaarde(invulwaarde='c-28-35',
                                    label='C28/35',
                                    definitie='C van Concrete (Beton). 28 is de karakteristieke druksterkte bij beproeving op cilinders. 35 is de karakteristieke druksterkte bij beproeving op kubussen. Beiden uitgedrukt in MPa.',
                                    objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlBetonsterkteklasse/c-28-35'),
        'c-30-37': KeuzelijstWaarde(invulwaarde='c-30-37',
                                    label='C30/37',
                                    definitie='C van Concrete (Beton). 30 is de karakteristieke druksterkte bij beproeving op cilinders. 37 is de karakteristieke druksterkte bij beproeving op kubussen. Beiden uitgedrukt in MPa.',
                                    objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlBetonsterkteklasse/c-30-37'),
        'c-35-45': KeuzelijstWaarde(invulwaarde='c-35-45',
                                    label='C35/45',
                                    definitie='C van Concrete (Beton). 35 is de karakteristieke druksterkte bij beproeving op cilinders. 45 is de karakteristieke druksterkte bij beproeving op kubussen. Beiden uitgedrukt in MPa.',
                                    objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlBetonsterkteklasse/c-35-45'),
        'c-40-50': KeuzelijstWaarde(invulwaarde='c-40-50',
                                    label='C40/50',
                                    definitie='C van Concrete (Beton). 40 is de karakteristieke druksterkte bij beproeving op cilinders. 50 is de karakteristieke druksterkte bij beproeving op kubussen. Beiden uitgedrukt in MPa.',
                                    objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlBetonsterkteklasse/c-40-50'),
        'c-45-55': KeuzelijstWaarde(invulwaarde='c-45-55',
                                    label='C45/55',
                                    definitie='C van Concrete (Beton). 45 is de karakteristieke druksterkte bij beproeving op cilinders. 55 is de karakteristieke druksterkte bij beproeving op kubussen. Beiden uitgedrukt in MPa.',
                                    objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlBetonsterkteklasse/c-45-55'),
        'c-50-60': KeuzelijstWaarde(invulwaarde='c-50-60',
                                    label='C50/60',
                                    definitie='C van Concrete (Beton). 50 is de karakteristieke druksterkte bij beproeving op cilinders. 60 is de karakteristieke druksterkte bij beproeving op kubussen. Beiden uitgedrukt in MPa.',
                                    objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlBetonsterkteklasse/c-50-60'),
        'c-53-65': KeuzelijstWaarde(invulwaarde='c-53-65',
                                    label='C53/65',
                                    definitie='C van Concrete (Beton). 53 is de karakteristieke druksterkte bij beproeving op cilinders. 65 is de karakteristieke druksterkte bij beproeving op kubussen. Beiden uitgedrukt in MPa.',
                                    objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlBetonsterkteklasse/c-53-65'),
        'c-55-67': KeuzelijstWaarde(invulwaarde='c-55-67',
                                    label='C55/67',
                                    definitie='C van Concrete (Beton). 55 is de karakteristieke druksterkte bij beproeving op cilinders. 67 is de karakteristieke druksterkte bij beproeving op kubussen. Beiden uitgedrukt in MPa.',
                                    objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlBetonsterkteklasse/c-55-67'),
        'c-60-75': KeuzelijstWaarde(invulwaarde='c-60-75',
                                    label='C60/75',
                                    definitie='C van Concrete (Beton). 60 is de karakteristieke druksterkte bij beproeving op cilinders. 75 is de karakteristieke druksterkte bij beproeving op kubussen. Beiden uitgedrukt in MPa.',
                                    objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlBetonsterkteklasse/c-60-75'),
        'c-70-85': KeuzelijstWaarde(invulwaarde='c-70-85',
                                    label='C70/85',
                                    definitie='C van Concrete (Beton). 70 is de karakteristieke druksterkte bij beproeving op cilinders. 85 is de karakteristieke druksterkte bij beproeving op kubussen. Beiden uitgedrukt in MPa.',
                                    objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlBetonsterkteklasse/c-70-85'),
        'c-8-10': KeuzelijstWaarde(invulwaarde='c-8-10',
                                   label='C8/10',
                                   definitie='C van Concrete (Beton). 8 is de karakteristieke druksterkte bij beproeving op cilinders. 10 is de karakteristieke druksterkte bij beproeving op kubussen. Beiden uitgedrukt in MPa.',
                                   objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlBetonsterkteklasse/c-8-10'),
        'c-80-85': KeuzelijstWaarde(invulwaarde='c-80-85',
                                    label='C80/85',
                                    definitie='C van Concrete (Beton). 80 is de karakteristieke druksterkte bij beproeving op cilinders. 85 is de karakteristieke druksterkte bij beproeving op kubussen. Beiden uitgedrukt in MPa.',
                                    objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlBetonsterkteklasse/c-80-85'),
        'c-90-105': KeuzelijstWaarde(invulwaarde='c-90-105',
                                     label='C90/105',
                                     definitie='C van Concrete (Beton). 90 is de karakteristieke druksterkte bij beproeving op cilinders. 105 is de karakteristieke druksterkte bij beproeving op kubussen. Beiden uitgedrukt in MPa.',
                                     objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlBetonsterkteklasse/c-90-105')
    }

