'''Provides exceptions related to Query'''

from typing import Any, Literal


class InvalidQueryStepTypeException(Exception):
    '''Raised by \'validate_query_step\' if type of Query step is not 'dict' '''

    status = 400

    def __init__(self, *, step_type: Any):
        super().__init__(
            InvalidQueryStepTypeException.format_msg(step_type=step_type),
            {'step_type': step_type},
        )

    @staticmethod
    def format_msg(*, step_type):
        '''Formats exception message'''

        return (
            f'Query step type should be of type \'dict\'. Got \'{step_type}\' instead'
        )


class InvalidQueryStepLenException(Exception):
    '''Raised by \'validate_query_step\' if Query step has more than one item'''

    status = 400

    def __init__(self, *, step_items: tuple[str]):
        super().__init__(
            InvalidQueryStepLenException.format_msg(step_items=step_items),
            {'step_items': step_items},
        )

    @staticmethod
    def format_msg(*, step_items):
        '''Formats exception message'''

        return f'Query step can only have one item. Got \'{step_items}\' instead'


class InvalidQueryStepAttrTypeException(Exception):
    '''Raised by \'validate_query_step\' if type of Query step attr is not 'dict' '''

    status = 400

    def __init__(self, *, step_attr_type: Any):
        super().__init__(
            InvalidQueryStepAttrTypeException.format_msg(step_attr_type=step_attr_type),
            {'step_attr_type': step_attr_type},
        )

    @staticmethod
    def format_msg(*, step_attr_type):
        '''Formats exception message'''

        return f'Query step attr value should be of type \'dict\'. Got \'{step_attr_type}\' instead'


class InvalidQueryStepAttrLenException(Exception):
    '''Raised by \'validate_query_step\' if Query step attr has more than one item'''

    status = 400

    def __init__(self, *, step_attr_items: tuple[str]):
        super().__init__(
            InvalidQueryStepAttrLenException.format_msg(
                step_attr_items=step_attr_items
            ),
            {'step_attr_items': step_attr_items},
        )

    @staticmethod
    def format_msg(*, step_attr_items):
        '''Formats exception message'''

        return (
            f'Query step attr can only have one item. Got \'{step_attr_items}\' instead'
        )


class InvalidQueryOperTypeException(Exception):
    '''Raised by \'validate_query_step\' if value of Query step attr is invalid'''

    status = 400

    def __init__(
        self,
        *,
        attr_name: str,
        attr_oper: Literal[
            '$ne',
            '$eq',
            '$gt',
            '$gte',
            '$lt',
            '$lte',
            '$all',
            '$in',
            '$nin',
            '$regex',
        ],
        attr_type: Any,
        attr_val: Any,
    ):
        super().__init__(
            InvalidQueryOperTypeException.format_msg(
                attr_name=attr_name,
                attr_oper=attr_oper,
                attr_type=attr_type,
                attr_val=attr_val,
            ),
            {
                'attr_name': attr_name,
                'attr_oper': attr_oper,
                'attr_type': attr_type,
                'attr_val': attr_val,
            },
        )

    @staticmethod
    def format_msg(*, attr_name, attr_oper, attr_type, attr_val):
        '''Formats exception message'''

        return f'Invalid value for Query Arg \'{attr_name}\' with Query Arg Oper \'{attr_oper}\' expecting type \'{attr_type}\' but got \'{attr_val}\''


class UnknownQueryOperException(Exception):
    '''Raised by \'validate_query_step\' if an unknown \'Query Arg\' is detected'''

    status = 400

    def __init__(
        self,
        *,
        attr_name: str,
        attr_oper: Literal[
            '$ne',
            '$eq',
            '$gt',
            '$gte',
            '$lt',
            '$lte',
            '$all',
            '$in',
            '$nin',
            '$regex',
        ],
    ):
        super().__init__(
            UnknownQueryOperException.format_msg(
                attr_name=attr_name, attr_oper=attr_oper
            ),
            {'attr_name': attr_name, 'attr_oper': attr_oper},
        )

    @staticmethod
    def format_msg(*, attr_name, attr_oper):
        '''Formats exception message'''

        return f'Unknown Query Arg Oper \'{attr_oper}\' for Query Arg \'{attr_name}\''
