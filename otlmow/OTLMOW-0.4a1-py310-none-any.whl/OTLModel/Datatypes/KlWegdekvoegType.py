# coding=utf-8
from OTLMOW.OTLModel.Datatypes.KeuzelijstField import KeuzelijstField
from OTLMOW.OTLModel.Datatypes.KeuzelijstWaarde import KeuzelijstWaarde


# Generated with OTLEnumerationCreator. To modify: extend, do not edit
class KlWegdekvoegType(KeuzelijstField):
    """Vormen van wegdekvoeg."""
    naam = 'KlWegdekvoegType'
    label = 'Voeg type'
    objectUri = 'https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#KlWegdekvoegType'
    definition = 'Vormen van wegdekvoeg.'
    codelist = 'https://wegenenverkeer.data.vlaanderen.be/id/conceptscheme/KlWegdekvoegType'
    options = {
        'DGB-compoundvoeg': KeuzelijstWaarde(invulwaarde='DGB-compoundvoeg',
                                             label='DGB compoundvoeg',
                                             definitie='Een voeg die het uitzetten en krimpen van materialen, ook wel werking genoemd, opvangt.',
                                             objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlWegdekvoegType/DGB-compoundvoeg'),
        'dwarse-werkvoeg': KeuzelijstWaarde(invulwaarde='dwarse-werkvoeg',
                                            label='dwarse werkvoeg',
                                            definitie='Een dwarse voeg die het uitzetten en krimpen van materialen, ook wel werking genoemd, opvangt.',
                                            objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlWegdekvoegType/dwarse-werkvoeg'),
        'geëxtrudeerde-voegband': KeuzelijstWaarde(invulwaarde='geëxtrudeerde-voegband',
                                                   label='geëxtrudeerde voegband',
                                                   definitie='Een geëxtrudeerde voegband die het uitzetten en krimpen van materialen, ook wel werking genoemd, opvangt.',
                                                   objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlWegdekvoegType/geëxtrudeerde-voegband'),
        'isolatievoeg-tussen-bestaande-constructie-en-betonverharding': KeuzelijstWaarde(invulwaarde='isolatievoeg-tussen-bestaande-constructie-en-betonverharding',
                                                                                         label='isolatievoeg tussen bestaande constructie en betonverharding',
                                                                                         definitie='isolatievoeg tussen bestaande constructie en betonverharding',
                                                                                         objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlWegdekvoegType/isolatievoeg-tussen-bestaande-constructie-en-betonverharding'),
        'langse-buigingsvoeg': KeuzelijstWaarde(invulwaarde='langse-buigingsvoeg',
                                                label='langse buigingsvoeg',
                                                definitie='Een zaagsnede om de verharding toe te laten te scharnieren volgens de lengteas en om de spanningen ingevolge de thermische gradiënt te beperken.',
                                                objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlWegdekvoegType/langse-buigingsvoeg'),
        'langse-werkvoeg': KeuzelijstWaarde(invulwaarde='langse-werkvoeg',
                                            label='langse werkvoeg',
                                            definitie='Een langse voeg die het uitzetten en krimpen van materialen, ook wel werking genoemd, opvangt.',
                                            objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlWegdekvoegType/langse-werkvoeg'),
        'langsvoeg-tussen-asfalt-en-beton': KeuzelijstWaarde(invulwaarde='langsvoeg-tussen-asfalt-en-beton',
                                                             label='langsvoeg tussen asfalt en beton',
                                                             definitie='Een doorgaande voeg in de lengterichting tussen asfalt en beton.',
                                                             objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlWegdekvoegType/langsvoeg-tussen-asfalt-en-beton'),
        'langsvoeg-tussen-fietspad-en-betonverharding': KeuzelijstWaarde(invulwaarde='langsvoeg-tussen-fietspad-en-betonverharding',
                                                                         label='langsvoeg tussen fietspad en betonverharding',
                                                                         definitie='Een doorgaande voeg in de lengterichting tussen een fietspad en betonverharding.',
                                                                         objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlWegdekvoegType/langsvoeg-tussen-fietspad-en-betonverharding'),
        'langsvoeg-tussen-lijnvormig-element-en-betonverharding': KeuzelijstWaarde(invulwaarde='langsvoeg-tussen-lijnvormig-element-en-betonverharding',
                                                                                   label='langsvoeg tussen lijnvormig element en betonverharding',
                                                                                   definitie='Een doorgaande voeg in de lengterichting tussen een lijnvormig element en betonverharding.',
                                                                                   objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlWegdekvoegType/langsvoeg-tussen-lijnvormig-element-en-betonverharding'),
        'langsvoeg-tussen-lijnvormig-element-en-bitumineuze-verharding': KeuzelijstWaarde(invulwaarde='langsvoeg-tussen-lijnvormig-element-en-bitumineuze-verharding',
                                                                                          label='langsvoeg tussen lijnvormig element en bitumineuze verharding',
                                                                                          definitie='langsvoeg tussen lijnvormig element en bitumineuze verharding',
                                                                                          objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlWegdekvoegType/langsvoeg-tussen-lijnvormig-element-en-bitumineuze-verharding'),
        'uitzettingsvoeg': KeuzelijstWaarde(invulwaarde='uitzettingsvoeg',
                                            label='uitzettingsvoeg',
                                            definitie='Een voeg die het uitzetten en krimpen van materialen, ook wel werking genoemd, opvangt.',
                                            objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlWegdekvoegType/uitzettingsvoeg'),
        'voorgevormde-voegband': KeuzelijstWaarde(invulwaarde='voorgevormde-voegband',
                                                  label='voorgevormde voegband',
                                                  definitie='Een voorgevormde voegband die het uitzetten en krimpen van materialen, ook wel werking genoemd, opvangt.',
                                                  objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlWegdekvoegType/voorgevormde-voegband')
    }

