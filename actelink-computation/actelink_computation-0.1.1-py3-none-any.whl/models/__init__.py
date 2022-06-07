from collections import namedtuple
from dataclasses import dataclass
from enum import Enum
from actelink.logger import log

# makes our Calcul enum also inherits from str so that it is JSON serializable
class Calcul(str, Enum):
    """
    Enumération des différents types de calcul
    """
    PrimePure = 'primep'
    """ Calcul de la prime pure """
    CoutMoyen = 'avg_cost'
    """ Calcul du coût moyen * fréquence """
    Frequence = 'frequence'
    """ Calcul de la fréquence """

@dataclass
class Context(object):
    """
    Object représentant un contexte de calcul
    """
    millesime:  str
    """ Millésime """
    offre:      str
    """ Offre """
    guarantyId: str
    """ Identifiant unique de garantie """
    calcul:     Calcul
    """ Type de calcul """

    # implements __eq__ and __hash__ so that Context is hashable hence be used as a key
    def __eq__(self, other): 
        return self.millesime == other.millesime and \
            self.offre == other.offre and \
            self.guarantyId == other.guarantyId and \
            self.calcul == other.calcul

    def __hash__(self):
        return hash((self.millesime, self.offre, self.guarantyId, self.calcul))

__functions = {}

def add(fname: str, fcallback: object, context: Context) -> None:
    log.info(f"{fname}, {fcallback}, {context})")
    __functions[context] = {'functionName': fname, 'callback': fcallback, 'context': context}

def get():
    return [{'context': k, 'functionName': v['functionName']} for k,v in __functions.items()]

def compute(data) -> float:
    ret = {"results": []}

    for item in data['contextsWithFunction']:
        res = {"context": item["context"]}
        key = namedtuple("Context", item['context'].keys())(*item['context'].values())

        if key not in __functions:
            log.error(f"unknown context {key}")
            res['functionName'] = ""
            res['rate'] = {"value": 0.0, "unit": "euros"}
        else:
            log.info(f"found function {__functions[key]['functionName']} for {key}")
            res['functionName'] = __functions[key]['functionName']
            res['rate'] = {
                "value": __functions[key]['callback'](__functions[key]['context']),
                "unit": "euros"
            }
        ret["results"].append(res)

    return ret