import copy
import logging
from typing import (TYPE_CHECKING, Any, MutableMapping, Optional, Tuple, Union,
                    cast)

from bson import ObjectId

from nawah.config import Config

if TYPE_CHECKING:
    from nawah.classes import Attr, Query
    from nawah.types import (NawahQueryOperAnd, NawahQueryOperOr,
                             NawahQuerySpecialGroup, NawahQueryStep)

logger = logging.getLogger('nawah')


def _compile_query(
    *,
    attrs: MutableMapping[str, 'Attr'],
    query: 'Query',
) -> Tuple[
    Optional[int],
    Optional[int],
    MutableMapping[str, int],
    Optional[list['NawahQuerySpecialGroup']],
    list[Any],
]:
    aggregate_prefix: list[Any] = []
    aggregate_suffix: list[Any] = []
    aggregate_query: list[Any] = [{'$match': {'$and': []}}]
    aggregate_match = aggregate_query[0]['$match']['$and']
    skip: Optional[int] = None
    limit: Optional[int] = None
    sort: MutableMapping[str, int] = {'_id': -1}
    group: Optional[list['NawahQuerySpecialGroup']] = None
    logger.debug('attempting to process query: %s', query)

    query = copy.deepcopy(query)

    # Update variables per Doc Mode
    if '__deleted' not in query or query['__deleted'] is False:
        aggregate_prefix.append({'$match': {'__deleted': {'$exists': False}}})
    else:
        # This condition is expanded to allow __deleted = True, __deleted = None to have
        # del query[__deleted] be applied to both conditions
        if query['__deleted'][0] is True:
            aggregate_prefix.append({'$match': {'__deleted': {'$exists': True}}})
        del query['__deleted'][0]

    if '__create_draft' not in query or query['__create_draft'] is False:
        aggregate_prefix.append({'$match': {'__create_draft': {'$exists': False}}})
    else:
        if query['__create_draft'][0] is True:
            aggregate_prefix.append({'$match': {'__create_draft': {'$exists': True}}})
        del query['__create_draft'][0]

    if ('__update_draft' not in query and '__update_draft:$ne' not in query) or query[
        '__update_draft'
    ] is False:
        query_update_draft = False
        aggregate_prefix.append({'$match': {'__update_draft': {'$exists': False}}})
    else:
        query_update_draft = True
        aggregate_prefix.append({'$match': {'__update_draft': {'$exists': True}}})
        if '__update_draft' in query and isinstance(
            query['__update_draft'][0], ObjectId
        ):
            aggregate_prefix.append(
                {'$match': {'__update_draft': query['__update_draft'][0]}}
            )
        elif '__update_draft:$ne' in query and query['__update_draft:$ne'][0] is False:
            aggregate_prefix.append({'$match': {'__update_draft': {'$ne': False}}})
        try:
            del query['__update_draft'][0]
        except:
            del query['__update_draft:$ne'][0]

    # Update variables per Query Special Args
    if '$skip' in query:
        skip = query['$skip']
    if '$limit' in query:
        limit = query['$limit']
    if '$sort' in query:
        sort = query['$sort']
    if '$group' in query:
        group = query['$group']
    if '$search' in query:
        aggregate_prefix.insert(0, {'$match': {'$text': {'$search': query['$search']}}})
        project_query: MutableMapping[str, Any] = {
            attr: '$' + attr for attr in attrs.keys()
        }
        project_query['_id'] = '$_id'
        project_query['__score'] = {'$meta': 'textScore'}
        aggregate_suffix.append({'$project': project_query})
        aggregate_suffix.append({'$match': {'__score': {'$gt': 0.5}}})
    if '$geo_near' in query:
        aggregate_prefix.insert(
            0,
            {
                '$geoNear': {
                    'near': {
                        'type': 'Point',
                        'coordinates': query['$geo_near']['val'],
                    },
                    'distanceField': query['$geo_near']['attr'] + '.__distance',
                    'maxDistance': query['$geo_near']['dist'],
                    'spherical': True,
                }
            },
        )

    aggregate_match = query.pipe or []

    for step in aggregate_match:
        _compile_query_step(
            aggregate_prefix=aggregate_prefix,
            aggregate_suffix=aggregate_suffix,
            attrs=attrs,
            step=step,
        )

    if '$attrs' in query and isinstance(query['$attrs'], list):
        group_query: dict[str, Any] = {
            '_id': '$_id',
            **{
                attr: {'$first': f'${attr}'}
                for attr in query['$attrs']
                if attr in attrs.keys()
            },
        }
        # We need to expose __update_draft value if it is queried as this refers to the original
        # doc to be updated
        if query_update_draft:
            group_query['__update_draft'] = {'$first': '$__update_draft'}
        aggregate_suffix.append({'$group': group_query})
    else:
        group_query = {
            '_id': '$_id',
            **{attr: {'$first': f'${attr}'} for attr in attrs.keys()},
        }
        # We need to expose __update_draft value if it is queried as this refers to the original
        # doc to be updated
        if query_update_draft:
            group_query['__update_draft'] = {'$first': '$__update_draft'}
        aggregate_suffix.append({'$group': group_query})

    logger.debug(
        'processed query, aggregate_prefix:%s, aggregate_suffix:%s, aggregate_match:%s',
        aggregate_prefix,
        aggregate_suffix,
        aggregate_match,
    )
    if len(aggregate_match) == 1:
        aggregate_query = [{'$match': aggregate_match[0]}]
    elif len(aggregate_match) == 0:
        aggregate_query = []

    aggregate_query = aggregate_prefix + aggregate_query + aggregate_suffix
    return (skip, limit, sort, group, aggregate_query)


def _compile_query_step(
    *,
    aggregate_prefix: list[Any],
    aggregate_suffix: list[Any],
    attrs: MutableMapping[str, 'Attr'],
    step: Union['NawahQueryStep', 'NawahQueryOperOr', 'NawahQueryOperAnd'],
) -> None:
    for attr_name, attr_val in step.items():
        if isinstance(attr_val, list):
            for child_attr_val in attr_val:
                _compile_query_step(
                    aggregate_prefix=aggregate_prefix,
                    aggregate_suffix=aggregate_suffix,
                    attrs=attrs,
                    step=child_attr_val,
                )
            return

        if '.' not in attr_name:
            continue

        root_attr_name = attr_name.split('.')[0]

        if root_attr_name not in attrs or not attrs[root_attr_name].extn:
            continue

        # [TODO] Check if this works with EXTN as Attr Type TYPE
        # Don't attempt to extn attr that is already extended
        lookup_query = False
        for stage in aggregate_prefix:
            if '$lookup' in stage.keys() and stage['$lookup']['as'] == root_attr_name:
                lookup_query = True
                break
        if not lookup_query:
            extn_collection = Config.modules[
                attrs[root_attr_name].extn.module
            ].collection
            aggregate_prefix.append(
                {'$addFields': {root_attr_name: {'$toObjectId': root_attr_name}}}
            )
            aggregate_prefix.append(
                {
                    '$lookup': {
                        'from': extn_collection,
                        'localField': root_attr_name,
                        'foreignField': '_id',
                        'as': root_attr_name,
                    }
                }
            )
            aggregate_prefix.append({'$unwind': root_attr_name})
            group_query: MutableMapping[str, Any] = {
                attr: {'$first': f'${attr}'} for attr in attrs.keys()
            }
            group_query[root_attr_name] = {'$first': f'${root_attr_name}._id'}
            group_query['_id'] = '$_id'
            aggregate_suffix.append({'$group': group_query})
