# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: cosmos/feegrant/v1beta1/feegrant.proto, cosmos/feegrant/v1beta1/genesis.proto, cosmos/feegrant/v1beta1/query.proto, cosmos/feegrant/v1beta1/tx.proto
# plugin: python-betterproto
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List

import betterproto
from betterproto.grpc.grpclib_server import ServiceBase
import grpclib


@dataclass(eq=False, repr=False)
class MsgGrantAllowance(betterproto.Message):
    """
    MsgGrantAllowance adds permission for Grantee to spend up to Allowance of
    fees from the account of Granter.
    """

    # granter is the address of the user granting an allowance of their funds.
    granter: str = betterproto.string_field(1)
    # grantee is the address of the user being granted an allowance of another
    # user's funds.
    grantee: str = betterproto.string_field(2)
    # allowance can be any of basic and filtered fee allowance.
    allowance: "betterproto_lib_google_protobuf.Any" = betterproto.message_field(3)


@dataclass(eq=False, repr=False)
class MsgGrantAllowanceResponse(betterproto.Message):
    """
    MsgGrantAllowanceResponse defines the Msg/GrantAllowanceResponse response
    type.
    """

    pass


@dataclass(eq=False, repr=False)
class MsgRevokeAllowance(betterproto.Message):
    """
    MsgRevokeAllowance removes any existing Allowance from Granter to Grantee.
    """

    # granter is the address of the user granting an allowance of their funds.
    granter: str = betterproto.string_field(1)
    # grantee is the address of the user being granted an allowance of another
    # user's funds.
    grantee: str = betterproto.string_field(2)


@dataclass(eq=False, repr=False)
class MsgRevokeAllowanceResponse(betterproto.Message):
    """
    MsgRevokeAllowanceResponse defines the Msg/RevokeAllowanceResponse response
    type.
    """

    pass


@dataclass(eq=False, repr=False)
class BasicAllowance(betterproto.Message):
    """
    BasicAllowance implements Allowance with a one-time grant of tokens that
    optionally expires. The grantee can use up to SpendLimit to cover fees.
    """

    # spend_limit specifies the maximum amount of tokens that can be spent by
    # this allowance and will be updated as tokens are spent. If it is empty,
    # there is no spend limit and any amount of coins can be spent.
    spend_limit: List["__base_v1_beta1__.Coin"] = betterproto.message_field(1)
    # expiration specifies an optional time when this allowance expires
    expiration: datetime = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class PeriodicAllowance(betterproto.Message):
    """
    PeriodicAllowance extends Allowance to allow for both a maximum cap, as
    well as a limit per time period.
    """

    # basic specifies a struct of `BasicAllowance`
    basic: "BasicAllowance" = betterproto.message_field(1)
    # period specifies the time duration in which period_spend_limit coins can be
    # spent before that allowance is reset
    period: timedelta = betterproto.message_field(2)
    # period_spend_limit specifies the maximum number of coins that can be spent
    # in the period
    period_spend_limit: List["__base_v1_beta1__.Coin"] = betterproto.message_field(3)
    # period_can_spend is the number of coins left to be spent before the
    # period_reset time
    period_can_spend: List["__base_v1_beta1__.Coin"] = betterproto.message_field(4)
    # period_reset is the time at which this period resets and a new one begins,
    # it is calculated from the start time of the first transaction after the
    # last period ended
    period_reset: datetime = betterproto.message_field(5)


@dataclass(eq=False, repr=False)
class AllowedMsgAllowance(betterproto.Message):
    """
    AllowedMsgAllowance creates allowance only for specified message types.
    """

    # allowance can be any of basic and filtered fee allowance.
    allowance: "betterproto_lib_google_protobuf.Any" = betterproto.message_field(1)
    # allowed_messages are the messages for which the grantee has the access.
    allowed_messages: List[str] = betterproto.string_field(2)


@dataclass(eq=False, repr=False)
class Grant(betterproto.Message):
    """Grant is stored in the KVStore to record a grant with full context"""

    # granter is the address of the user granting an allowance of their funds.
    granter: str = betterproto.string_field(1)
    # grantee is the address of the user being granted an allowance of another
    # user's funds.
    grantee: str = betterproto.string_field(2)
    # allowance can be any of basic and filtered fee allowance.
    allowance: "betterproto_lib_google_protobuf.Any" = betterproto.message_field(3)


@dataclass(eq=False, repr=False)
class QueryAllowanceRequest(betterproto.Message):
    """
    QueryAllowanceRequest is the request type for the Query/Allowance RPC
    method.
    """

    # granter is the address of the user granting an allowance of their funds.
    granter: str = betterproto.string_field(1)
    # grantee is the address of the user being granted an allowance of another
    # user's funds.
    grantee: str = betterproto.string_field(2)


@dataclass(eq=False, repr=False)
class QueryAllowanceResponse(betterproto.Message):
    """
    QueryAllowanceResponse is the response type for the Query/Allowance RPC
    method.
    """

    # allowance is a allowance granted for grantee by granter.
    allowance: "Grant" = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class QueryAllowancesRequest(betterproto.Message):
    """
    QueryAllowancesRequest is the request type for the Query/Allowances RPC
    method.
    """

    grantee: str = betterproto.string_field(1)
    # pagination defines an pagination for the request.
    pagination: "__base_query_v1_beta1__.PageRequest" = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class QueryAllowancesResponse(betterproto.Message):
    """
    QueryAllowancesResponse is the response type for the Query/Allowances RPC
    method.
    """

    # allowances are allowance's granted for grantee by granter.
    allowances: List["Grant"] = betterproto.message_field(1)
    # pagination defines an pagination for the response.
    pagination: "__base_query_v1_beta1__.PageResponse" = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class GenesisState(betterproto.Message):
    """
    GenesisState contains a set of fee allowances, persisted from the store
    """

    allowances: List["Grant"] = betterproto.message_field(1)


class MsgStub(betterproto.ServiceStub):
    async def grant_allowance(
        self,
        *,
        granter: str = "",
        grantee: str = "",
        allowance: "betterproto_lib_google_protobuf.Any" = None
    ) -> "MsgGrantAllowanceResponse":

        request = MsgGrantAllowance()
        request.granter = granter
        request.grantee = grantee
        if allowance is not None:
            request.allowance = allowance

        return await self._unary_unary(
            "/cosmos.feegrant.v1beta1.Msg/GrantAllowance",
            request,
            MsgGrantAllowanceResponse,
        )

    async def revoke_allowance(
        self, *, granter: str = "", grantee: str = ""
    ) -> "MsgRevokeAllowanceResponse":

        request = MsgRevokeAllowance()
        request.granter = granter
        request.grantee = grantee

        return await self._unary_unary(
            "/cosmos.feegrant.v1beta1.Msg/RevokeAllowance",
            request,
            MsgRevokeAllowanceResponse,
        )


class QueryStub(betterproto.ServiceStub):
    async def allowance(
        self, *, granter: str = "", grantee: str = ""
    ) -> "QueryAllowanceResponse":

        request = QueryAllowanceRequest()
        request.granter = granter
        request.grantee = grantee

        return await self._unary_unary(
            "/cosmos.feegrant.v1beta1.Query/Allowance", request, QueryAllowanceResponse
        )

    async def allowances(
        self,
        *,
        grantee: str = "",
        pagination: "__base_query_v1_beta1__.PageRequest" = None
    ) -> "QueryAllowancesResponse":

        request = QueryAllowancesRequest()
        request.grantee = grantee
        if pagination is not None:
            request.pagination = pagination

        return await self._unary_unary(
            "/cosmos.feegrant.v1beta1.Query/Allowances",
            request,
            QueryAllowancesResponse,
        )


class MsgBase(ServiceBase):
    async def grant_allowance(
        self,
        granter: str,
        grantee: str,
        allowance: "betterproto_lib_google_protobuf.Any",
    ) -> "MsgGrantAllowanceResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def revoke_allowance(
        self, granter: str, grantee: str
    ) -> "MsgRevokeAllowanceResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def __rpc_grant_allowance(self, stream: grpclib.server.Stream) -> None:
        request = await stream.recv_message()

        request_kwargs = {
            "granter": request.granter,
            "grantee": request.grantee,
            "allowance": request.allowance,
        }

        response = await self.grant_allowance(**request_kwargs)
        await stream.send_message(response)

    async def __rpc_revoke_allowance(self, stream: grpclib.server.Stream) -> None:
        request = await stream.recv_message()

        request_kwargs = {
            "granter": request.granter,
            "grantee": request.grantee,
        }

        response = await self.revoke_allowance(**request_kwargs)
        await stream.send_message(response)

    def __mapping__(self) -> Dict[str, grpclib.const.Handler]:
        return {
            "/cosmos.feegrant.v1beta1.Msg/GrantAllowance": grpclib.const.Handler(
                self.__rpc_grant_allowance,
                grpclib.const.Cardinality.UNARY_UNARY,
                MsgGrantAllowance,
                MsgGrantAllowanceResponse,
            ),
            "/cosmos.feegrant.v1beta1.Msg/RevokeAllowance": grpclib.const.Handler(
                self.__rpc_revoke_allowance,
                grpclib.const.Cardinality.UNARY_UNARY,
                MsgRevokeAllowance,
                MsgRevokeAllowanceResponse,
            ),
        }


class QueryBase(ServiceBase):
    async def allowance(self, granter: str, grantee: str) -> "QueryAllowanceResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def allowances(
        self, grantee: str, pagination: "__base_query_v1_beta1__.PageRequest"
    ) -> "QueryAllowancesResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def __rpc_allowance(self, stream: grpclib.server.Stream) -> None:
        request = await stream.recv_message()

        request_kwargs = {
            "granter": request.granter,
            "grantee": request.grantee,
        }

        response = await self.allowance(**request_kwargs)
        await stream.send_message(response)

    async def __rpc_allowances(self, stream: grpclib.server.Stream) -> None:
        request = await stream.recv_message()

        request_kwargs = {
            "grantee": request.grantee,
            "pagination": request.pagination,
        }

        response = await self.allowances(**request_kwargs)
        await stream.send_message(response)

    def __mapping__(self) -> Dict[str, grpclib.const.Handler]:
        return {
            "/cosmos.feegrant.v1beta1.Query/Allowance": grpclib.const.Handler(
                self.__rpc_allowance,
                grpclib.const.Cardinality.UNARY_UNARY,
                QueryAllowanceRequest,
                QueryAllowanceResponse,
            ),
            "/cosmos.feegrant.v1beta1.Query/Allowances": grpclib.const.Handler(
                self.__rpc_allowances,
                grpclib.const.Cardinality.UNARY_UNARY,
                QueryAllowancesRequest,
                QueryAllowancesResponse,
            ),
        }


from ...base import v1beta1 as __base_v1_beta1__
from ...base.query import v1beta1 as __base_query_v1_beta1__
import betterproto.lib.google.protobuf as betterproto_lib_google_protobuf
