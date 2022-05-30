# coding=utf-8
from OTLMOW.OTLModel.BaseClasses.OTLAttribuut import OTLAttribuut
from OTLMOW.OTLModel.Classes.AIMNaamObject import AIMNaamObject
from OTLMOW.OTLModel.Datatypes.DtcDocument import DtcDocument
from OTLMOW.OTLModel.Datatypes.DteIPv4Adres import DteIPv4Adres
from OTLMOW.OTLModel.Datatypes.KlAIDModuleType import KlAIDModuleType
from OTLMOW.OTLModel.Datatypes.StringField import StringField
from OTLMOW.GeometrieArtefact.PuntGeometrie import PuntGeometrie


# Generated with OTLClassCreator. To modify: extend, do not edit
class AIDModule(AIMNaamObject, PuntGeometrie):
    """Aparte hardware module voor automatische incidentdetectie op camerabeelden. De module kan centraal of lokaal opgesteld staan maar altijd als apart onderdeel, niet als deel van de camera die de beelden doorstuurt. Ze kan gebruikt worden voor modules die analoge beelden analyseren en voor modules die werken op basis van digitale beelden. Het doel is om op een automatische en zo intelligent mogelijk manier gebeurtenissen uit de beelden van een CCTV-camera te halen."""

    typeURI = 'https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#AIDModule'
    """De URI van het object volgens https://www.w3.org/2001/XMLSchema#anyURI."""

    def __init__(self):
        AIMNaamObject.__init__(self)
        PuntGeometrie.__init__(self)

        self._configBestand = OTLAttribuut(field=DtcDocument,
                                           naam='configBestand',
                                           label='config bestand',
                                           objectUri='https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#AIDModule.configBestand',
                                           definition='Configuratiebestand van de configuratie van de AID.',
                                           owner=self)

        self._dnsNaam = OTLAttribuut(field=StringField,
                                     naam='dnsNaam',
                                     label='DNS naam',
                                     objectUri='https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#AIDModule.dnsNaam',
                                     definition='De DNSNaam (ook "volledige domein naam" genoemd ) is een unieke naam binnen het Domain Name System (DNS), het naamgevingssysteem waarmee computers, webservers, diensten en  toepassing op een unieke manier kunnen worden geïdentificeerd. Deze bevat zowel de hostname en de top level domein naam bv. 120c8-ar1.belfa.be.',
                                     owner=self)

        self._ipAdres = OTLAttribuut(field=DteIPv4Adres,
                                     naam='ipAdres',
                                     label='ip adres datastring',
                                     objectUri='https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#AIDModule.ipAdres',
                                     definition='Het IP-adres van de AID-module.',
                                     owner=self)

        self._technischeFiche = OTLAttribuut(field=DtcDocument,
                                             naam='technischeFiche',
                                             label='technische fiche',
                                             objectUri='https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#AIDModule.technischeFiche',
                                             usagenote='Bestanden van het type pdf.',
                                             definition='Technische fiche van de AID-module.',
                                             owner=self)

        self._type = OTLAttribuut(field=KlAIDModuleType,
                                  naam='type',
                                  label='type',
                                  objectUri='https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#AIDModule.type',
                                  definition='Het type van de AID-module.',
                                  owner=self)

    @property
    def configBestand(self):
        """Configuratiebestand van de configuratie van de AID."""
        return self._configBestand.get_waarde()

    @configBestand.setter
    def configBestand(self, value):
        self._configBestand.set_waarde(value, owner=self)

    @property
    def dnsNaam(self):
        """De DNSNaam (ook "volledige domein naam" genoemd ) is een unieke naam binnen het Domain Name System (DNS), het naamgevingssysteem waarmee computers, webservers, diensten en  toepassing op een unieke manier kunnen worden geïdentificeerd. Deze bevat zowel de hostname en de top level domein naam bv. 120c8-ar1.belfa.be."""
        return self._dnsNaam.get_waarde()

    @dnsNaam.setter
    def dnsNaam(self, value):
        self._dnsNaam.set_waarde(value, owner=self)

    @property
    def ipAdres(self):
        """Het IP-adres van de AID-module."""
        return self._ipAdres.get_waarde()

    @ipAdres.setter
    def ipAdres(self, value):
        self._ipAdres.set_waarde(value, owner=self)

    @property
    def technischeFiche(self):
        """Technische fiche van de AID-module."""
        return self._technischeFiche.get_waarde()

    @technischeFiche.setter
    def technischeFiche(self, value):
        self._technischeFiche.set_waarde(value, owner=self)

    @property
    def type(self):
        """Het type van de AID-module."""
        return self._type.get_waarde()

    @type.setter
    def type(self, value):
        self._type.set_waarde(value, owner=self)
