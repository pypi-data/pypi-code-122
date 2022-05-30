# coding=utf-8
from OTLMOW.OTLModel.BaseClasses.OTLAttribuut import OTLAttribuut
from abc import abstractmethod, ABC
from OTLMOW.OTLModel.Datatypes.DtcAdres import DtcAdres
from OTLMOW.OTLModel.Datatypes.DtcDocument import DtcDocument
from OTLMOW.OTLModel.Datatypes.DteTekstblok import DteTekstblok
from OTLMOW.OTLModel.Datatypes.KwantWrdInMeter import KwantWrdInMeter
from OTLMOW.OTLModel.Datatypes.KwantWrdInMeterTAW import KwantWrdInMeterTAW


# Generated with OTLClassCreator. To modify: extend, do not edit
class Put(ABC):
    """Abstracte bedoeld om de verschillende soort putten onder te brengen en gemeenschappelijke eigenschappen over te dragen. De relaties worden overgedragen via de abstracte PutRelaties."""

    typeURI = 'https://wegenenverkeer.data.vlaanderen.be/ns/abstracten#Put'
    """De URI van het object volgens https://www.w3.org/2001/XMLSchema#anyURI."""

    @abstractmethod
    def __init__(self):
        self._adres = OTLAttribuut(field=DtcAdres,
                                   naam='adres',
                                   label='adres',
                                   objectUri='https://wegenenverkeer.data.vlaanderen.be/ns/abstracten#Put.adres',
                                   definition='Dichtstbijgelegen adres voor de put, het adres bestaat enkel uit de straatnaam indien het dichtstbijzijnde adres > 100m verwijderd is.',
                                   owner=self)

        self._diepte = OTLAttribuut(field=KwantWrdInMeter,
                                    naam='diepte',
                                    label='diepte',
                                    objectUri='https://wegenenverkeer.data.vlaanderen.be/ns/abstracten#Put.diepte',
                                    definition='Het verschil tussen het maaiveldpeil en het laagste punt van de binnenkant van de put in meter.',
                                    owner=self)

        self._maaiveldpeil = OTLAttribuut(field=KwantWrdInMeterTAW,
                                          naam='maaiveldpeil',
                                          label='maaiveldpeil',
                                          objectUri='https://wegenenverkeer.data.vlaanderen.be/ns/abstracten#Put.maaiveldpeil',
                                          definition='De hoogte van het grondoppervlak in meter-TAW in het midden van het deksel van de put.',
                                          owner=self)

        self._technischeFiche = OTLAttribuut(field=DtcDocument,
                                             naam='technischeFiche',
                                             label='technische fiche',
                                             objectUri='https://wegenenverkeer.data.vlaanderen.be/ns/abstracten#Put.technischeFiche',
                                             kardinaliteit_max='*',
                                             definition='De technische fiche van de put.',
                                             owner=self)

        self._toestandPut = OTLAttribuut(field=DteTekstblok,
                                         naam='toestandPut',
                                         label='toestand put',
                                         objectUri='https://wegenenverkeer.data.vlaanderen.be/ns/abstracten#Put.toestandPut',
                                         definition='Opmerkingen van de toestand en staat van de (verbindings-)put.',
                                         owner=self)

    @property
    def adres(self):
        """Dichtstbijgelegen adres voor de put, het adres bestaat enkel uit de straatnaam indien het dichtstbijzijnde adres > 100m verwijderd is."""
        return self._adres.get_waarde()

    @adres.setter
    def adres(self, value):
        self._adres.set_waarde(value, owner=self)

    @property
    def diepte(self):
        """Het verschil tussen het maaiveldpeil en het laagste punt van de binnenkant van de put in meter."""
        return self._diepte.get_waarde()

    @diepte.setter
    def diepte(self, value):
        self._diepte.set_waarde(value, owner=self)

    @property
    def maaiveldpeil(self):
        """De hoogte van het grondoppervlak in meter-TAW in het midden van het deksel van de put."""
        return self._maaiveldpeil.get_waarde()

    @maaiveldpeil.setter
    def maaiveldpeil(self, value):
        self._maaiveldpeil.set_waarde(value, owner=self)

    @property
    def technischeFiche(self):
        """De technische fiche van de put."""
        return self._technischeFiche.get_waarde()

    @technischeFiche.setter
    def technischeFiche(self, value):
        self._technischeFiche.set_waarde(value, owner=self)

    @property
    def toestandPut(self):
        """Opmerkingen van de toestand en staat van de (verbindings-)put."""
        return self._toestandPut.get_waarde()

    @toestandPut.setter
    def toestandPut(self, value):
        self._toestandPut.set_waarde(value, owner=self)
