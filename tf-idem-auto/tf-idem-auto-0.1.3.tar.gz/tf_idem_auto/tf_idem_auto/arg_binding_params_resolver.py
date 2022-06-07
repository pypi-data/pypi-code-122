"""
This function tries to find argument binding in terraform and try to
add argument binding instead of resolved static values
"""
import json
import re
from collections import ChainMap

from ruamel.yaml.comments import CommentedMap
from ruamel.yaml.main import round_trip_dump as yaml_dump

attributes_to_ignore = ["resource_id", "name", "tags", "arn"]


def resolve_argument_bindings(
    hub,
    sls_file_data,
    complete_tf_resource_map,
    complete_resource_map,
    complete_dict_of_variables,
    file,
    dumper,
):
    idem_resource_type_resource_id_separator = (
        hub.tf_idem_auto.utils.idem_resource_type_resource_id_separator
    )
    for item in sls_file_data:
        list_of_comments = []
        resource_attributes = list(sls_file_data[item].values())[0]
        idem_resource_type = list(sls_file_data[item].keys())[0].replace(".present", "")
        idem_resource_map = dict(ChainMap(*resource_attributes))
        tf_resource = complete_tf_resource_map.get(
            f"{idem_resource_type}{idem_resource_type_resource_id_separator}{idem_resource_map.get('resource_id')}"
        )
        for resource_attribute in resource_attributes:
            for resource_attribute_key in resource_attribute:
                resource_attribute_value = resource_attribute[resource_attribute_key]
                if resource_attribute_key not in attributes_to_ignore:
                    resource_attribute[
                        resource_attribute_key
                    ] = check_if_eligible_for_argument_binding(
                        hub,
                        complete_resource_map,
                        idem_resource_type,
                        resource_attribute_value,
                        complete_dict_of_variables,
                    )
                if resource_attribute_key == "resource_id":
                    sls_resource_data = complete_resource_map.get(
                        f"{idem_resource_type}{idem_resource_type_resource_id_separator}{idem_resource_map.get('resource_id')}"
                    )
                    if sls_resource_data:
                        resource_attribute[
                            resource_attribute_key
                        ] = f"{{{{ params.get(\"{sls_resource_data.get('resource_path')}\")}}}}"

                if tf_resource:
                    (
                        tf_resource_value,
                        is_attribute_different,
                    ) = hub.tf_idem_auto.utils.get_tf_equivalent_idem_attribute(
                        tf_resource, list(tf_resource.keys())[0], resource_attribute_key
                    )
                    # tf_resource_value = list(list(tf_resource.values())[0].values())[
                    #     0
                    # ].get(resource_attribute_key)
                    if isinstance(tf_resource_value, str) and re.search(
                        r"\${jsonencode\(var\.[\w-]+\)}", tf_resource_value
                    ):
                        tf_resource_value = re.sub(
                            r"\${jsonencode\(var\.[\w-]+\)}",
                            lambda jsonencode_string: f'"${{var.{jsonencode_string.group()[17:-2]}}}"',
                            tf_resource_value,
                        )
                    if tf_resource_value:
                        parameterized_value = check_if_eligible_for_parameter_binding(
                            hub,
                            tf_resource_value,
                            resource_attribute_key,
                            resource_attribute_value,
                            resource_attribute_value,
                            complete_resource_map,
                            complete_tf_resource_map,
                        )
                        if parameterized_value:
                            if is_attribute_different:
                                hub.tf_idem_auto.utils.set_tf_equivalent_idem_attribute(
                                    resource_attribute_key,
                                    parameterized_value,
                                    list(tf_resource.keys())[0],
                                    resource_attribute_key,
                                    resource_attribute,
                                )
                            else:
                                resource_attribute[
                                    resource_attribute_key
                                ] = parameterized_value
        if tf_resource:
            list_of_comments.extend(
                look_for_possible_improvements(hub, tf_resource, resource_attributes)
            )
            sls_file_data_with_comment = CommentedMap({item: sls_file_data[item]})
            if len(list_of_comments) > 0:
                sls_file_data_with_comment.yaml_set_start_comment(
                    "\n" + "\n".join(list_of_comments)
                )
            else:
                sls_file_data_with_comment.yaml_set_start_comment("\n")

            yaml_dump(sls_file_data_with_comment, file, Dumper=dumper)


def look_for_possible_improvements(hub, tf_resource, resource_attributes):
    list_of_comments = []
    conditional_pattern = re.compile(
        r'["$.{{\s\w\d()\/}}+\*-]+\?["$.{{\s\w\d()\/}}+\*-]+\:["$.{{\s\w\d()\/}}+\*-]+'
    )
    data_pattern = re.compile(r"[\w${.\s\d-]+data\.")
    for resource_attribute in resource_attributes:
        for resource_attribute_key in resource_attribute:
            (
                tf_resource_value,
                is_attribute_different,
            ) = hub.tf_idem_auto.utils.get_tf_equivalent_idem_attribute(
                tf_resource, list(tf_resource.keys())[0], resource_attribute_key
            )
            if isinstance(tf_resource_value, str) and data_pattern.search(
                tf_resource_value
            ):
                list_of_comments.append(
                    hub.tf_idem_auto.utils.DATA_COMMENT.format(
                        resource=resource_attribute_key
                    )
                )
            if (
                isinstance(tf_resource_value, str)
                and "count.index" in tf_resource_value
            ):
                list_of_comments.append(
                    hub.tf_idem_auto.utils.COUNT_COMMENT.format(
                        resource=resource_attribute_key
                    )
                )
            if isinstance(tf_resource_value, str) and conditional_pattern.search(
                tf_resource_value
            ):
                list_of_comments.append(
                    hub.tf_idem_auto.utils.CONDITIONAL_COMMENT.format(
                        resource=resource_attribute_key
                    )
                )
    return list_of_comments


def check_if_eligible_for_argument_binding(
    hub,
    complete_resource_map,
    complete_tf_resource_map,
    attribute_value,
    complete_dict_of_variables=None,
):
    if isinstance(attribute_value, dict) or isinstance(attribute_value, list):
        if isinstance(attribute_value, dict):
            for item in attribute_value:
                attribute_value[item] = check_if_eligible_for_argument_binding(
                    hub,
                    complete_resource_map,
                    complete_tf_resource_map,
                    attribute_value[item],
                    complete_dict_of_variables,
                )
            return attribute_value
        else:
            new_attributes = []
            for item in attribute_value:
                arg_binded_item = check_if_eligible_for_argument_binding(
                    hub,
                    complete_resource_map,
                    complete_tf_resource_map,
                    item,
                    complete_dict_of_variables,
                )
                new_attributes.append(arg_binded_item)
            return new_attributes
    else:
        if isinstance(attribute_value, str) and attribute_value.startswith("{"):
            attribute_value = json.loads(attribute_value)
            for item in attribute_value:
                attribute_value[item] = check_if_eligible_for_argument_binding(
                    hub,
                    complete_resource_map,
                    complete_tf_resource_map,
                    attribute_value[item],
                    complete_dict_of_variables,
                )
            return json.dumps(attribute_value)
        return check_argument_binding(
            hub,
            complete_resource_map,
            complete_tf_resource_map,
            attribute_value,
            complete_dict_of_variables,
        )


def check_if_eligible_for_parameter_binding(
    hub,
    tf_resource_val,
    attribute_key,
    attribute_value,
    attribute_val_itr,
    complete_resource_map,
    complete_tf_resource_map,
):
    if isinstance(tf_resource_val, dict) or isinstance(tf_resource_val, list):
        if isinstance(tf_resource_val, dict):
            for item in tf_resource_val:
                updated_parameterized_val = check_if_eligible_for_parameter_binding(
                    hub,
                    tf_resource_val[item],
                    attribute_key,
                    attribute_value,
                    attribute_val_itr.get(item)
                    if isinstance(attribute_val_itr, dict)
                    else None,
                    complete_resource_map,
                    complete_tf_resource_map,
                )
                if updated_parameterized_val:
                    tf_resource_val[item] = updated_parameterized_val
            if attribute_key == "tags" and isinstance(attribute_value, list):
                tf_resource_val = convert_tags_dict_list(tf_resource_val)
            return tf_resource_val
        else:
            new_attributes = []
            for item in tf_resource_val:
                if tf_resource_val.index(item) >= len(attribute_val_itr):
                    ret = None
                else:
                    ret = attribute_val_itr[tf_resource_val.index(item)]
                arg_binded_item = check_if_eligible_for_parameter_binding(
                    hub,
                    item,
                    attribute_key,
                    attribute_value,
                    ret,
                    complete_resource_map,
                    complete_tf_resource_map,
                )
                new_attributes.append(arg_binded_item if arg_binded_item else item)
            return new_attributes
    elif isinstance(tf_resource_val, str):
        if tf_resource_val.startswith("{"):
            tf_resource_val = json.loads(tf_resource_val)
            attribute_val_itr = json.loads(attribute_val_itr)
            for item in tf_resource_val:
                parameterized_value = check_if_eligible_for_parameter_binding(
                    hub,
                    tf_resource_val[item],
                    attribute_key,
                    attribute_value,
                    attribute_val_itr.get(item),
                    complete_resource_map,
                    complete_tf_resource_map,
                )
                if parameterized_value:
                    tf_resource_val[item] = parameterized_value
                if attribute_key == "tags" and isinstance(attribute_value, list):
                    tf_resource_val = convert_tags_dict_list(tf_resource_val)
            return json.dumps(tf_resource_val)
        if isinstance(attribute_val_itr, str) and tf_resource_val.startswith("${aws"):
            return check_argument_binding(
                hub, complete_resource_map, complete_tf_resource_map, attribute_val_itr
            )
        return parameterize(tf_resource_val, attribute_key, attribute_value)


def is_attr_value_in_variables(idem_resource_val, complete_dict_of_variables):
    for attr_key, attribute_value in complete_dict_of_variables.items():
        if isinstance(attribute_value, str) and attribute_value == idem_resource_val:
            return attr_key
    return None


def check_argument_binding(
    hub,
    complete_resource_map,
    idem_resource_type,
    attribute_value,
    complete_dict_of_variables=None,
):
    idem_resource_type_resource_id_separator = (
        hub.tf_idem_auto.utils.idem_resource_type_resource_id_separator
    )
    tf_idem_resource_type_map = hub.tf_idem_auto.utils.tf_idem_resource_type_map
    tf_auto_supported_resource_types = list(tf_idem_resource_type_map.values())
    for tf_auto_supported_resource_type in tf_auto_supported_resource_types:
        if (
            tf_auto_supported_resource_type != idem_resource_type
            and f"{tf_auto_supported_resource_type}{idem_resource_type_resource_id_separator}{attribute_value}"
            in complete_resource_map
        ):
            referred_resource_dict = complete_resource_map[
                f"{tf_auto_supported_resource_type}{idem_resource_type_resource_id_separator}{attribute_value}"
            ]
            return f"${{{next(iter(referred_resource_dict['resource'])).replace('.present', '')}:{referred_resource_dict['resource_path']}:{referred_resource_dict['type']}}}"
        elif complete_dict_of_variables:
            attribute_in_variable = is_attr_value_in_variables(
                attribute_value, complete_dict_of_variables
            )
            if attribute_in_variable:
                return f'{{{{params.get("{attribute_in_variable}")}}}}'
    return attribute_value


def convert_var_to_param(var_input):
    variable_name = var_input.group()[6:-1]
    return f'{{{{ params.get("{variable_name}") }}}}'


def convert_local_to_param(var_input):
    variable_name = var_input.group()[2:-1]
    variable_name = variable_name.replace(".", "_")
    return f'{{{{ params.get("{variable_name}") }}}}'


def convert_local_to_param_dict(var_input):
    variable_name = var_input.group()[2:-1]
    variable_name = variable_name.replace(".", "_") + "_dict"
    return f'{{{{ params.get("{variable_name}") }}}}'


def handle_count_index_in_tags(additional_tags, attribute_value):
    attribute_value_dict = convert_tags_list_dict(attribute_value)
    additional_tags_updated = {}
    for tag_key in additional_tags:
        tag_value = additional_tags.get(tag_key)
        if "-${count.index}" in tag_key:
            tag_key = replace_count_index_in_tags(
                tag_key, attribute_value_dict.get(tag_key)
            )
        if "-${count.index}" in additional_tags.get(tag_key):
            tag_value = replace_count_index_in_tags(
                tag_value, attribute_value_dict.get(tag_key)
            )
        additional_tags_updated[tag_key] = tag_value
    return additional_tags_updated


def replace_count_index_in_tags(tag_key, original_tag_value):
    split_list = original_tag_value.split("-")
    for count_index in split_list:
        if count_index.isnumeric():
            tag_key = tag_key.replace("-${count.index}", f"-{count_index}")
    return tag_key


def parameterize(resolved_value, attribute_key, attribute_value):
    parameterized_value = None
    while re.search(r"\${var\.[\w-]+}", resolved_value):
        resolved_value = re.sub(
            r"\${var\.[\w-]+}", convert_var_to_param, resolved_value
        )
        parameterized_value = resolved_value
    if resolved_value and attribute_key == "tags":
        if re.search(r"\${merge\(", resolved_value):
            resolved_value = resolved_value.replace("'", '"')
            try:
                format_additional_tags_str = (
                    resolved_value.replace("${merge(local.tags,,", "")
                    .replace(",)}", "")
                    .replace("{{ ", "")
                    .replace("}} ", "")
                    .replace(" {{", "")
                    .replace(" }}", "")
                    .replace("{{", "")
                    .replace("}}", "")
                    .replace("'", '"')
                )

                format_additional_tags_str_p = format_additional_tags_str.replace(
                    '("', '(\\"'
                ).replace('")', '\\")')
                additional_tags = json.loads(format_additional_tags_str_p)
                if "-${count.index}" in format_additional_tags_str_p:
                    additional_tags = handle_count_index_in_tags(
                        additional_tags, attribute_value
                    )

                parameterized_value = (
                    f'{{{{ params.get("local_tags") + {adjust_format_of_additional_tags(json.dumps(convert_tags_dict_list(additional_tags)))}}}}}'
                    if isinstance(attribute_value, list)
                    else f'{{{{ params.get("local_tags_dict") + {adjust_format_of_additional_tags(json.dumps(dict(additional_tags)))}}}}}'
                )
            except Exception as e:
                print("Exception in loading additional tags :: ", e)
        elif "local." in resolved_value:
            json_loads = json.loads(json.dumps(resolved_value))
            if isinstance(attribute_value, list):
                parameterized_value = re.sub(
                    r"\${local.[\w-]+}", convert_local_to_param, str(json_loads)
                )
            else:
                parameterized_value = re.sub(
                    r"\${local.[\w-]+}", convert_local_to_param_dict, str(json_loads)
                )

    return parameterized_value


def convert_tags_list_dict(tags_list):
    tags_dict = {}
    for tag in tags_list:
        tags_dict[tag.get("Key")] = tag.get("Value")
    return tags_dict


def convert_tags_dict_list(tags_dict):
    tags_list = []
    for tag in tags_dict:
        tags_list.append(
            {
                "Key": fix_format_of_additional_tags(tag),
                "Value": fix_format_of_additional_tags(tags_dict[tag]),
            }
        )
    return tags_list


def adjust_format_of_additional_tags(tag_str):
    # Handle if params is  at beginning or ending or middle
    tag_str = tag_str.replace('params.get(\\"', '"+params.get("')
    tag_str = tag_str.replace('"params.get(\\"', 'params.get("')
    tag_str = tag_str.replace('"+params.get(\\"', 'params.get("')
    tag_str = tag_str.replace('\\")', '")+"')
    tag_str = tag_str.replace('+""', "")
    tag_str = tag_str.replace('""+', "")

    return tag_str


def fix_format_of_additional_tags(input_tag):
    if not any(substring in input_tag for substring in ["{{", "}}"]):
        return input_tag
    input_tag = re.sub("{{", '" + {{', input_tag)
    input_tag = re.sub("}}", '}} + "', input_tag)
    if input_tag.endswith(' + "'):
        input_tag = input_tag[:-4]
    if input_tag.startswith('" + '):
        input_tag = input_tag[4:]
    if not input_tag.endswith("}") and not input_tag.endswith('"'):
        input_tag = f'{input_tag}"'
    if not input_tag.startswith("{") and not input_tag.startswith('"'):
        input_tag = f'"{input_tag}'
    return input_tag
