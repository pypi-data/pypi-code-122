# coding=utf-8
from OTLMOW.OEFModel.EMObject import EMObject


# Generated with OEFClassCreator. To modify: extend, do not edit
class Wind(EMObject):
    """windmeter - richting en snelheid"""

    typeURI = 'https://lgc.data.wegenenverkeer.be/ns/installatie#Wind'
    label = 'Windmeter'

    def __init__(self):
        super().__init__()

