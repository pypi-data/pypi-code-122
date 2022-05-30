__all__ = ('OperationDescriptionPoint', 'CommissionCalculatorPoint',
           'DepositFromBankCardPoint', 'WithdrawToBankCardPoint',
           )

from expressmoney.api import *

SERVICE = 'wallets'
APP = 'operations'


class OperationDescriptionReadContract(Contract):
    TO_WALLET_FROM_BANK_CARD = 'TO_WALLET_FROM_BANK_CARD'
    FROM_WALLTET_TO_BANK_CARD = 'FROM_WALLTET_TO_BANK_CARD'
    FROM_WALLTET_TO_WALLET = 'FROM_WALLTET_TO_WALLET'
    TO_WALLTET_FROM_WALLET = 'TO_WALLTET_FROM_WALLET'
    NAME_CHOICES = (
        (TO_WALLET_FROM_BANK_CARD, TO_WALLET_FROM_BANK_CARD),
        (FROM_WALLTET_TO_BANK_CARD, FROM_WALLTET_TO_BANK_CARD),
        (FROM_WALLTET_TO_WALLET, FROM_WALLTET_TO_WALLET),
        (TO_WALLTET_FROM_WALLET, TO_WALLTET_FROM_WALLET),
    )
    RUB = 'RUB'
    USD = 'USD'
    CURRENCY_CODE_CHOICES = (
        (RUB, RUB),
        (USD, USD),
    )
    id = serializers.IntegerField(min_value=1)
    created = serializers.DateTimeField()
    updated = serializers.DateTimeField()
    name = serializers.ChoiceField(choices=NAME_CHOICES)
    currency_code = serializers.ChoiceField(choices=CURRENCY_CODE_CHOICES)
    commission_rate = serializers.DecimalField(max_digits=2, decimal_places=2)
    commission_min = serializers.DecimalField(max_digits=16, decimal_places=0)
    amount_min = serializers.DecimalField(max_digits=16, decimal_places=0)
    amount_max = serializers.DecimalField(max_digits=16, decimal_places=0)
    wallet_limit = serializers.DecimalField(max_digits=16, decimal_places=0)


class CommissionCalculatorCreateContract(Contract):
    name = serializers.ChoiceField(choices=OperationDescriptionReadContract.NAME_CHOICES)
    currency_code = serializers.ChoiceField(choices=OperationDescriptionReadContract.CURRENCY_CODE_CHOICES)
    amount = serializers.DecimalField(max_digits=16, decimal_places=0)


class CommissionCalculatorResponseContract(Contract):
    commission = serializers.DecimalField(max_digits=16, decimal_places=0)


class DepositFromBankCardCreateContract(Contract):
    wallet = serializers.IntegerField(min_value=1)
    amount = serializers.DecimalField(max_digits=16, decimal_places=0)
    bank_card_id = serializers.IntegerField(min_value=1)


class WithdrawToBankCardCreateContract(DepositFromBankCardCreateContract):
    pass


class OperationDescriptionID(ID):
    _service = SERVICE
    _app = APP
    _view_set = 'operation_description'


class CommissionCalculatorID(ID):
    _service = SERVICE
    _app = APP
    _view_set = 'commission_calculator'


class DepositFromBankCardID(ID):
    _service = SERVICE
    _app = APP
    _view_set = 'deposit_from_bankcard'


class WithdrawToBankCardID(ID):
    _service = SERVICE
    _app = APP
    _view_set = 'withdraw_to_bankcard'


class OperationDescriptionPoint(ListPointMixin, ContractPoint):
    _point_id = OperationDescriptionID()
    _read_contract = OperationDescriptionReadContract


class CommissionCalculatorPoint(ResponseMixin, CreatePointMixin, ContractPoint):
    _point_id = CommissionCalculatorID()
    _create_contract = CommissionCalculatorCreateContract
    _response_contract = CommissionCalculatorResponseContract


class DepositFromBankCardPoint(CreatePointMixin, ContractPoint):
    _point_id = DepositFromBankCardID()
    _create_contract = DepositFromBankCardCreateContract


class WithdrawToBankCardPoint(CreatePointMixin, ContractPoint):
    _point_id = WithdrawToBankCardID()
    _create_contract = WithdrawToBankCardCreateContract
