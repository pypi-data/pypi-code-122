'''Provides exceptions used in Nawah'''

from ._attr import (InvalidAttrTypeArgException, InvalidAttrTypeException,
                    InvalidAttrTypeRefException, JSONPathNotFoundException)
from ._call import (InvalidCallEndpointException, InvalidFuncException,
                    InvalidModuleException, NotPermittedException)
from ._config import ConfigException
from ._data import UnknownDeleteStrategyException
from ._func import (FuncException, InvalidDocAttrException,
                    InvalidDocException, InvalidQueryAttrException,
                    InvalidQueryException, MissingDocAttrException,
                    MissingQueryAttrException)
from ._query import (InvalidQueryOperTypeException,
                     InvalidQueryStepAttrLenException,
                     InvalidQueryStepAttrTypeException,
                     InvalidQueryStepLenException,
                     InvalidQueryStepTypeException, UnknownQueryOperException)
from ._validate import InvalidAttrException, MissingAttrException
from ._var import InvalidLocaleException, InvalidVarException

__all__ = [
    'InvalidAttrTypeArgException',
    'InvalidAttrTypeException',
    'InvalidAttrTypeRefException',
    'JSONPathNotFoundException',
    'InvalidCallEndpointException',
    'InvalidFuncException',
    'InvalidModuleException',
    'NotPermittedException',
    'ConfigException',
    'UnknownDeleteStrategyException',
    'FuncException',
    'InvalidDocAttrException',
    'InvalidDocException',
    'InvalidQueryAttrException',
    'InvalidQueryException',
    'MissingDocAttrException',
    'MissingQueryAttrException',
    'InvalidQueryOperTypeException',
    'InvalidQueryStepAttrLenException',
    'InvalidQueryStepAttrTypeException',
    'InvalidQueryStepLenException',
    'InvalidQueryStepTypeException',
    'UnknownQueryOperException',
    'InvalidAttrException',
    'MissingAttrException',
    'InvalidLocaleException',
    'InvalidVarException',
]
