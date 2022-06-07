""" Le module actelink.variables permet de facilement interroger votre moteur de variables Actelink.

Une variable peut avoir trois types :

* d0 : une clé / valeur 
    Exemple pour une variable *intercept* : intercept=0.8

* d1 : un vecteur de clé / valeur
    Exemple pour une variable *niveau* : low=0.1, medium=0.24, high=0.3

* d2 : une matrice à deux dimensions de clé / valeur
    Exemple pour une variable *situation* : [homme, marié]=0.2, [homme, célibataire]=0.1 [femme, marié]=0.3, [femme, célibataire]=0.2

Une fois initialisé, ce module va se connecter à votre moteur de variables Actelink en utilisant les paramètres de connexion spécifiés.

Pour l'utiliser :

Installez le module :

>>> python -m pip install actelink-variables

Si le module est déjà installé, pour faire une mise à jour :

>>> python -m pip install --upgrade actelink-variables

Puis importez le dans votre code :

>>> import actelink.variables as av

Définir les paramètres de connexion à votre serveur Actelink, par exemple :

>>> url = "https://prod.actelink.tech:1234"
>>> key = "0123456789"

Initialiser le module actelink.variables :

>>> av.init(url, key)

Pour récupérer la valeur d'une variable :

>>> contexte = {'millesime': '2022', 'offre': 'Actelior', 'garantie': 'hos-hmed-medoptok', 'calcul': 'avg_cost'}
>>> sigma = av.get_variable(context, 'sigma')
>>> print(sigma)
0.3862223
"""

import requests
import urllib.parse
from actelink.logger import log

_stores             = dict()

def init(url: str, key: str):
    """Initialise le module actelink.variables

    :param str url: L'url de connexion au moteur de varibales.
    :param str key: La clé d'API avec laquelle s'authentifier auprès du moteur de variables.

    :raises ConnectionError: en cas d'échec de connexion au moteur de variables.
    """
    log.info(f"call variables engine with url: {url}, key: {key}")
    global __CUSTOMER_KEY, __VARIABLES_ENDPOINT, __STORES_ENDPOINT, _stores
    __CUSTOMER_KEY       = key
    __VARIABLES_ENDPOINT = urllib.parse.urljoin(url, '/api/v1/stores/{storeId}/variables/{label}')
    __STORES_ENDPOINT    = urllib.parse.urljoin(url, '/api/v1/stores')
    # retrieve the list of stores for this customer
    try:
        response = requests.get(__STORES_ENDPOINT, headers={'api-key': __CUSTOMER_KEY})
    except requests.exceptions.ConnectionError as error:
        log.error(f"CONNECTION FAILED!\n\n{error})")
        raise
    # check response is valid
    if response.status_code != 200:
        raise requests.exceptions.ConnectionError(f'Request failed, reason: {response.reason}')
    elif response.json() is None:
        log.warn('Warning: no stores found')
    else:
        for s in response.json():
            _stores[s['name']] = s['id']
            log.debug(f"found store {s['name']} (id {s['id']})")

def get_stores() -> tuple:
    """Retourne les stores existants sous forme d'un tuple.
    
    :returns: Un tuple contenant l'ensemble des stores associés à votre clé d'API.
    :rtype: tuple
    """
    return tuple(_stores)

def __contextToStore(context: dict) -> str:
    store_name = ".".join(f'{v}' for v in context.values())
    if store_name not in _stores:
        raise NameError(f'store {store_name} not found')
    return store_name

def get_variable(context: dict, var_label: str, var_keys=None) -> float:
    """Retourne la valeur d'une variable dans un contexte donné.

    :param dict context: Le contexte dans lequel on demande cette variable.
    :param str var_label: Le nom de la variable à retourner.
    :param str var_keys: La ou les clés à spécifier pour cette variable (None par défaut).
    :type var_keys: str or list or None

    :returns: La valeur de la variable *var_label* pour la/les clé(s) donnée(s) si spécifiée(s).
    :rtype: float
    :raises NameError: si le contexte donné n'existe pas.
    :raises ConnectionError: si la variable/clé n'existe pas.

    Exemples d'utilisation :

    * Cas d'une variable d0

    >>> context = {...}
    >>> intercept = av.get_variable(context, 'intercept')
    >>> print(intercept)
    0.893

    * Cas d'une variable d1
    
    >>> niveau = av.get_variable(context, 'niveau', 'medium')
    >>> print(niveau)
    0.24

    * Cas d'une variable d2
    
    >>> situation = av.get_variable(context, 'situation', 'homme,celibataire')
    >>> print(situation)
    0.893

    .. NOTE:: Dans le cas d'une variable de type d2, où deux clés doivent être spécifiées, celles ci peuvent être passées en paramètre sous la forme d'une string ou d'une liste :
    
    >>> situation = av.get_variable(context, 'situation', 'homme,celibataire')

    est équivalent à :

    >>> situation = av.get_variable(context, 'situation', ['homme', 'celibataire'])
    """
    store_name = __contextToStore(context)
    log.info(f'get_variable {var_label} on store {store_name}, requested key: {var_keys}')
    url = __VARIABLES_ENDPOINT.replace('{storeId}', _stores[store_name]).replace('{label}', var_label)
    # var_keys can be passed as a string or array of strings
    var_keys = ','.join(k.strip() for k in var_keys) if isinstance(var_keys, list) else var_keys
    try:
        response = requests.get(url, headers={'api-key': __CUSTOMER_KEY}, params={'key': var_keys})
    except requests.exceptions.ConnectionError as error:
        log.error(f"GET {url} FAILED\n\n{error})")
        raise
    if response.status_code != 200:
        log.error(f'GET {url} failed, reason: {response.reason}')
        raise requests.exceptions.ConnectionError(f'GET {url} failed, reason: {response.reason}')
    return float(response.json())

def get_variables(context: dict) -> list:
    """Retourne la liste de toutes les variables d'un contexte (store) donné.

    :param dict context: Le contexte pour lequel on veut récupérer la liste de variables.

    :returns: La liste des variables du contexte donné.
    :rtype: list

    Exemples d'utilisation :

    >>> context = {...}
    >>> vars = av.get_variables(context)
    """
    store_name = __contextToStore(context)
    try:
        response = requests.get(__STORES_ENDPOINT, headers={'api-key': __CUSTOMER_KEY})
    except requests.exceptions.ConnectionError as error:
        log.error(f"GET {__STORES_ENDPOINT} failed\n\n{error})")
        raise
    # check response is valid
    if response.status_code != 200:
        raise requests.exceptions.ConnectionError(f'GET {__STORES_ENDPOINT} failed, reason: {response.reason}')
    store = next(s for s in response.json() if s['name'] == store_name)
    return store['variables']
