import KratosMultiphysics
import KratosMultiphysics.CompressiblePotentialFlowApplication
import math

model = KratosMultiphysics.Model()
main_model_part = model.CreateModelPart("main")
main_model_part.AddNodalSolutionStepVariable(KratosMultiphysics.DISTANCE)
# KratosMultiphysics.ModelPartIO("rhomboid").ReadModelPart(main_model_part)
problem_domain = KratosMultiphysics.Hexahedra3D8(
    KratosMultiphysics.Node(1, -0.25, -0.75, -0.5),
    KratosMultiphysics.Node(2,  2.25, -0.75, -0.5),
    KratosMultiphysics.Node(3,  2.25,  0.75, -0.5),
    KratosMultiphysics.Node(4, -0.25,  0.75, -0.5),
    KratosMultiphysics.Node(5, -0.25, -0.75,  0.5),
    KratosMultiphysics.Node(6,  2.25, -0.75,  0.5),
    KratosMultiphysics.Node(7,  2.25,  0.75,  0.5),
    KratosMultiphysics.Node(8, -0.25,  0.75,  0.5))
parameters = KratosMultiphysics.Parameters("{}")
parameters.AddEmptyValue("element_name").SetString("Element3D4N")
parameters.AddEmptyValue("condition_name").SetString("Condition3D3N")
parameters.AddEmptyValue("create_skin_sub_model_part").SetBool(False)
parameters.AddEmptyValue("number_of_divisions").SetInt(26)
KratosMultiphysics.StructuredMeshGeneratorProcess(problem_domain, main_model_part, parameters).Execute()

from stl import mesh #this requires numpy-stl
wake_stl_mesh = mesh.Mesh.from_multi_file("rhomboid_wake.stl")
wake_model_part = model.CreateModelPart("wake")

dummy_property = wake_model_part.Properties[0]
node_id = 1
elem_id = 1
z=0.1
# Looping over stl meshes
for stl_mesh in wake_stl_mesh:
    for vertex in stl_mesh.points:
        node1 = wake_model_part.CreateNewNode(node_id, float(vertex[0]), float(vertex[1]), float(vertex[2])+z)
        node_id+=1
        node2 = wake_model_part.CreateNewNode(node_id, float(vertex[3]), float(vertex[4]), float(vertex[5])+z)
        node_id+=1
        node3 = wake_model_part.CreateNewNode(node_id, float(vertex[6]), float(vertex[7]), float(vertex[8])+z)
        node_id+=1

        wake_model_part.CreateNewElement("Element3D3N", elem_id,  [
                                        node1.Id, node2.Id, node3.Id], dummy_property)
        elem_id += 1


# wake_model_part.CreateNewNode(1, 0.0, 1.0, 0.1)
# wake_model_part.CreateNewNode(2, 30.0, 1.0, 0.1)
# wake_model_part.CreateNewNode(3, 30.0, -1.0, 0.1)
# wake_model_part.CreateNewNode(4, 0.0, -1.0, 0.1)
# wake_model_part.CreateNewElement("Element3D3N", 1, [1,2,3], KratosMultiphysics.Properties(0))
# wake_model_part.CreateNewElement("Element3D3N", 2, [1,3,4], KratosMultiphysics.Properties(0))

# moving_params = KratosMultiphysics.Parameters("""{
#                     "origin"                        : [-0.5,0.0,0.0],
#                     "rotation_point"                : [-0.25,0.0,0.0],
                #     "rotation_angle"                : 0.0,
                #     "sizing_multiplier"             : 1.0
                # }""")
# angle=math.radians(-moving_params["rotation_angle"].GetDouble())
# moving_params["rotation_angle"].SetDouble(angle)
# KratosMultiphysics.CompressiblePotentialFlowApplication.MoveModelPartProcess(wake_model_part, moving_params).Execute()

use_discontinuous = False #Set to false to use continuous distance process

if use_discontinuous:
    for element in main_model_part.Elements:
            for node in element.GetNodes():
                node.SetSolutionStepValue(KratosMultiphysics.DISTANCE,100.0)
    KratosMultiphysics.CalculateDiscontinuousDistanceToSkinProcess3D(main_model_part,wake_model_part).Execute()
    for element in main_model_part.Elements:
        distances = element.GetValue(KratosMultiphysics.ELEMENTAL_DISTANCES)
        counter = 0

        npos = 0
        nneg = 0
        for counter in range(0,4):
            if distances[counter] > 0.0:
                npos += 1
            else:
                nneg += 1
        counter = 0
        if (npos>0 and nneg >0):
            print(distances)
            element.Set(KratosMultiphysics.BOUNDARY,True)
            for node in element.GetNodes():
                node.SetSolutionStepValue(KratosMultiphysics.DISTANCE,distances[counter])
                counter += 1


else:
    # Continuous distance process (does not work for volumeless bodies)
    KratosMultiphysics.CalculateDistanceToSkinProcess3D(main_model_part,wake_model_part).Execute()
    for node in main_model_part.Nodes:
        node.SetValue(KratosMultiphysics.LAMBDA, 100)
    # OPTION 1
    # Save elemental distances in all the elements
    for element in main_model_part.Elements:
        distances = element.GetValue(KratosMultiphysics.ELEMENTAL_DISTANCES)
        counter = 0
        for node in element.GetNodes():
            node.SetValue(KratosMultiphysics.LAMBDA, distances[counter])
            counter += 1

    # OPTION 2
    # Save elemental distances only in cut elements
    number_of_cut_elements = 0
    for element in main_model_part.Elements:
        if(element.Is(KratosMultiphysics.TO_SPLIT)):
            number_of_cut_elements += 1
            distances = element.GetValue(KratosMultiphysics.ELEMENTAL_DISTANCES)
            counter = 0
            for node in element.GetNodes():
                node.SetValue(KratosMultiphysics.LAMBDA, distances[counter])
                counter += 1
            print(element.Id)


print('number_of_cut_elements = ', number_of_cut_elements)


from gid_output_process import GiDOutputProcess
gid_output = GiDOutputProcess(main_model_part,
                            "distance_test_CONTINUO",
                            KratosMultiphysics.Parameters("""
                                {
                                    "result_file_configuration" : {
                                        "gidpost_flags": {
                                            "GiDPostMode": "GiD_PostBinary",
                                            "WriteDeformedMeshFlag": "WriteUndeformed",
                                            "WriteConditionsFlag": "WriteConditions",
                                            "MultiFileFlag": "SingleFile"
                                        },
                                        "nodal_results" : ["DISTANCE"],
                                        "elemental_conditional_flags_results" : ["BOUNDARY"],
                                        "nodal_nonhistorical_results" : ["LAMBDA"],
                                        "plane_output"        : [
                                            {"point": [0.0, 0.0, 0.0],
                                            "normal": [0.0, 1.0, 0.0]}]
                                    }
                                }
                                """)
                            )

gid_output.ExecuteInitialize()
gid_output.ExecuteBeforeSolutionLoop()
gid_output.ExecuteInitializeSolutionStep()
gid_output.PrintOutput()
gid_output.ExecuteFinalizeSolutionStep()
gid_output.ExecuteFinalize()

