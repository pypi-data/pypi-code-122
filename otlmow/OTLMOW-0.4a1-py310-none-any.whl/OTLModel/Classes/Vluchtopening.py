# coding=utf-8
from OTLMOW.OTLModel.BaseClasses.OTLAttribuut import OTLAttribuut
from OTLMOW.OTLModel.Classes.AIMObject import AIMObject
from OTLMOW.OTLModel.Datatypes.DtcDocument import DtcDocument
from OTLMOW.OTLModel.Datatypes.KlLEGCOpeningType import KlLEGCOpeningType
from OTLMOW.GeometrieArtefact.PuntGeometrie import PuntGeometrie


# Generated with OTLClassCreator. To modify: extend, do not edit
class Vluchtopening(AIMObject, PuntGeometrie):
    """Vluchtopeningen voorzien een vluchtmogelijkheid. Deze bezitten dezelfde akoestische kwaliteitseisen als de voorgestelde schermen."""

    typeURI = 'https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Vluchtopening'
    """De URI van het object volgens https://www.w3.org/2001/XMLSchema#anyURI."""

    def __init__(self):
        AIMObject.__init__(self)
        PuntGeometrie.__init__(self)

        self._technischeFiche = OTLAttribuut(field=DtcDocument,
                                             naam='technischeFiche',
                                             label='technische fiche',
                                             objectUri='https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Vluchtopening.technischeFiche',
                                             definition='Document waarin onder andere het inplantingsplan van de doorgang wordt weergegeven.',
                                             owner=self)

        self._type = OTLAttribuut(field=KlLEGCOpeningType,
                                  naam='type',
                                  label='type',
                                  objectUri='https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Vluchtopening.type',
                                  usagenote='Attribuut uit gebruik sinds versie 2.1.0 ',
                                  deprecated_version='2.1.0',
                                  definition='Bepaling van het type van doorgang (sas, nooddeur) (voorlopig opgenomen in figuur 8-4-1).',
                                  owner=self)

    @property
    def technischeFiche(self):
        """Document waarin onder andere het inplantingsplan van de doorgang wordt weergegeven."""
        return self._technischeFiche.get_waarde()

    @technischeFiche.setter
    def technischeFiche(self, value):
        self._technischeFiche.set_waarde(value, owner=self)

    @property
    def type(self):
        """Bepaling van het type van doorgang (sas, nooddeur) (voorlopig opgenomen in figuur 8-4-1)."""
        return self._type.get_waarde()

    @type.setter
    def type(self, value):
        self._type.set_waarde(value, owner=self)
