from re import A
import pytest
from scenario_tool_interface import ScenarioToolInterface
import json
import time
import os

__author__ = "Christian Urich"
__copyright__ = "Christian Urich"
__license__ = "mit"


# USERNAME = "christian.urich@gmail.com"#os.getenv('USERNAME')
# PASSWORD = "rejudo01" #os.getenv('PASSWORD')

USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

USERNAME_GUEST = os.getenv('USERNAME_GUEST')
PASSWORD_GUEST = os.getenv('PASSWORD_GUEST')
PASSWORD_ADMIN = os.getenv('PASSWORD_ADMIN')
USERNAME_ADMIN = os.getenv('USERNAME_ADMIN')


def run_tutorial(queue="default"):
    sti = ScenarioToolInterface()
    # Login with your username and password
    sti.login(USERNAME, PASSWORD)

    project_id = sti.create_project()
    assert type(project_id) is int

    # Obtain region code
    region_id = sti.get_region("Melbourne")
    assert type(region_id) is int

    # Load geoson file
    with open("./resources/test.geojson", 'r') as file:
        geojson_file = json.loads(file.read())

    # Upload boundary
    geojson_id = sti.upload_geojson(geojson_file, project_id)

    # Set project parameters
    sti.update_project(project_id, {
        "name": "my project",
        "active": True,
        'region_id': region_id,
        "case_study_area_id": geojson_id,
    })

    # Setup data model
    region_parameters = sti.get_default_region_parameters(region_id)

    assert type(region_parameters) is dict

    sti.set_project_data_model(project_id, region_parameters)

    # Add assessment models
    lst_model = sti.get_assessment_model( "Land Surface Temperature")
    assert type(lst_model) is dict

    # Set assessment models
    sti.set_project_assessment_models(project_id, [lst_model])

    # Create and run baseline
    baseline_id = sti.create_scenario(project_id, None)
    assert type(baseline_id) is int
    sti.execute_scenario(baseline_id)

    # Scenarios are executed asynchronous.
    while True:
        # A status code smaller than 7 means the simulation is still executed.
        r = sti.check_status(baseline_id)
        status = r["status"]
        if status > 6:
            break
        time.sleep(1)


    # Print a list of available nodes
    sti.show_nodes()

    # Nodes are defined as below
    residential_node = {
        "node_type_id": sti.get_node_id("Urban Form"),
        "area": geojson_id,
        "parameters": sti.get_default_parameter_dict(sti.get_node_id("Urban Form"))
    }

    nodes = []
    # Several nodes can are combined to a workflow be adding them to a vector. The
    # nodes are executed in the order the are added
    nodes.append(residential_node)

    # Scenarios need a parent. In this case we use the base line scenario created before
    baseline_scenario_id = sti.get_baseline(project_id)

    # Crate a new scenario
    scenario_id = sti.create_scenario( project_id, baseline_scenario_id, "my new scenario")
    assert type(scenario_id) is int
    # Set workflow
    sti.set_scenario_workflow(scenario_id, nodes)

    # Execute scenario
    sti.execute_scenario(scenario_id, queue=queue)

    # Scenarios are executed asynchronous
    while True:
        # A status code smaller than 7 means the simulation is still executed.
        r = sti.check_status(scenario_id)
        status = r["status"]
        if status > 6:
            break

        time.sleep(1)

    while True:
        r = sti.run_query(scenario_id,
                          "SELECT avg(tree_cover_fraction) as tf from micro_climate_grid")

        if r['status'] == 'loaded':
            # Break the loop when query is loaded
            break
        time.sleep(1)
    print(r['data'])
    assert r['data'][0]['tf'] == 0.0726961320006131


    # Should through an exception because access
    # with pytest.raises(Exception) as e_info:
    #     sti.get_project_databases(project_id)


def test_login():
    sti = ScenarioToolInterface()
    sti.login(USERNAME, PASSWORD)
    assert type(sti.token) is str
    with pytest.raises(Exception) as e_info:
        sti.login(USERNAME, "passwod")
#
def test_guest_login():
    sti = ScenarioToolInterface()
    sti.login(USERNAME_GUEST, PASSWORD_GUEST)
    assert type(sti.token) is str

def test_admin_login():
    sti = ScenarioToolInterface()
    sti.login(USERNAME_ADMIN, PASSWORD_ADMIN)
    assert type(sti.token) is str

def test_get_region():
    sti = ScenarioToolInterface()
    sti.login(USERNAME, PASSWORD)

    assert type(sti.get_region("melbourne")) is int

def test_get_assessment_model():
    sti = ScenarioToolInterface()
    sti.login(USERNAME, PASSWORD)

    assert type(sti.get_assessment_model("Land Surface Temperature")) is dict


def test_get_assessment_model_water_cycle():
    sti = ScenarioToolInterface()
    sti.login(USERNAME, PASSWORD)

    assert type(sti.get_assessment_model("Water Cycle Model")) is dict
#
# # def test_nodes():
# #     # Login with your username and password
# #     token = sti.login(USERNAME, PASSWORD)
# #
# #     assert type(token) is str
# #
# #     model_id = sti.upload_dynamind_model(token, "test node", "resources/nodes/test_node.dyn")
# #
# #     assert type(model_id) is int
# #
# #     node_id = sti.create_node(token, "resources/nodes/test_node.json", model_id)
# #
# #     assert type(node_id) is int
# #
# #     n_id = sti.get_node_id(token, "test node")
# #
# #     assert type(n_id)
# #
# #     with pytest.raises(Exception) as e_info:
# #         sti.get_node_id(token, "test nod")
# #
# #     model_id = sti.upload_dynamind_model(token, "test node", "resources/nodes/test_node.dyn")
# #
# #     assert type(model_id) is int
# #
# #     node_version_id = sti.update_node(token, node_id, "resources/nodes/test_node.json", model_id)
# #
# #     assert type(node_version_id) is int
# #
# #     sti.deactivate_node(token, node_id)
# #
# #     with pytest.raises(Exception) as e_info:
# #         sti.get_node_id(token, "test node")
#
#
#
# def test_assessment_models():
#     # Login with your username and password
#     token = sti.login(USERNAME, PASSWORD)
#
#     assert type(token) is str
#
#     model_id = sti.upload_dynamind_model(token, "test node", "resources/assessment_nodes/test_assessment_model.dyn")
#
#     assert type(model_id) is int
#
#     node_id = sti.create_assessment_model(token, "resources/assessment_nodes/test_assessment_model.json", model_id)
#
#     assert type(node_id) is int
#
#     model_id = sti.upload_dynamind_model(token, "test node", "resources/assessment_nodes/test_assessment_model.dyn")
#
#     assert type(model_id) is int
#
#     node_version_id = sti.update_assessment_model(token, node_id, "resources/assessment_nodes/test_assessment_model.json", model_id)
#
#     assert type(node_version_id) is int
#
#
def test_run_tutorial():
    run_tutorial()
#
def test_run_tutorial_slow():
    run_tutorial(queue="slow")

# def test_node_access_level():
#     # Login with your username and password
#     token = sti.login(USERNAME, PASSWORD)
#     assert type(token) is str
#
#     #Upload test model
#     model_id = sti.upload_dynamind_model(token, "test node", "resources/nodes/test_node.dyn")
#
#     assert type(model_id) is int
#
#     n_id = sti.create_node(token, "resources/nodes/test_node.json", model_id)
#     assert type(n_id) is int
#
#     token = sti.login(USERNAME_GUEST, PASSWORD_GUEST)
#     assert type(token) is str
#
#     # Create a new project
#     project_id = sti.create_project(token)
#     assert type(project_id) is int
#
#     # Obtain region code
#     region_id = sti.get_region(token, "melbourne")
#     assert type(region_id) is int
#
#     # Load geoson file
#     with open("resources/test_small.geojson", 'r') as file:
#         geojson_file = json.loads(file.read())
#
#     # Upload boundary
#     geojson_id = sti.upload_geojson(token, geojson_file, project_id)
#
#     # Set project parameters
#     sti.update_project(token, project_id, {
#         "name": "my project small",
#         "active": True,
#         'region_id': region_id,
#         "case_study_area_id": geojson_id,
#     })
#
#     # Add assessment models
#     lst_model = sti.get_assessment_model(token, "Land Surface Temperature")
#     assert type(lst_model) is int
#
#     # Set assessment models
#     sti.set_project_assessment_models(token, project_id, [{"assessment_model_id": lst_model}])
#
#     # Create and run baseline
#     baseline_id = sti.create_scenario(token, project_id, None)
#     assert type(baseline_id) is int
#     sti.execute_scenario(token, baseline_id)
#
#     # Scenarios are executed asynchronous.
#     while True:
#         # A status code smaller than 7 means the simulation is still executed.
#         r = sti.check_status(token, baseline_id)
#         status = r["status"]
#         if status > 6:
#             break
#         time.sleep(1)
#
#
#
#     # Nodes are defined as below
#     test_nodes = {
#         "node_type_id": n_id,
#         "area": geojson_id,
#         "parameters":
#             {
#             }
#     }
#     nodes = []
#     # Several nodes can are combined to a workflow be adding them to a vector. The
#     # nodes are executed in the order the are added
#     nodes.append(test_nodes)
#
#     # Scenarios need a parent. In this case we use the base line scenario created before
#     baseline_scenario_id = sti.get_baseline(token, project_id)
#
#     # Crate a new scenario
#     scenario_id = sti.create_scenario(token, project_id, baseline_scenario_id, "my new scenario")
#     assert type(scenario_id) is int
#     # Set workflow
#     with pytest.raises(Exception) as e_info:
#         sti.set_scenario_workflow(token, scenario_id, nodes)
#
#     # Give me access to the node
#     sti.set_node_access_level(sti.login(USERNAME, PASSWORD), n_id, sti.AccessLevel.DEMO.value)
#     sti.set_scenario_workflow(token, scenario_id, nodes)
#
#     # Execute scenario
#     sti.execute_scenario(token, scenario_id)
#
#     # Remove node
#     sti.deactivate_node(token,  n_id)
#
#     with pytest.raises(Exception) as e_info:
#         sti.get_node_id(token, "test node")
#
#     # Scenarios are executed asynchronous
#     while True:
#         # A status code smaller than 7 means the simulation is still executed.
#         r = sti.check_status(token, scenario_id)
#         status = r["status"]
#         if status > 6:
#             break
#
#         time.sleep(1)





