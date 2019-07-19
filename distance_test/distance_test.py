import KratosMultiphysics
import KratosMultiphysics.CompressiblePotentialFlowApplication
import math

model = KratosMultiphysics.Model()
main_model_part = model.CreateModelPart("main")
main_model_part.AddNodalSolutionStepVariable(KratosMultiphysics.DISTANCE)
KratosMultiphysics.ModelPartIO("background1").ReadModelPart(main_model_part)

wake_model_part = model.CreateModelPart("wake")
wake_model_part.CreateNewNode(1, 0.0, 0.0, 0.0)
wake_model_part.CreateNewNode(2, 200.0, 0.0, 0.0)
wake_model_part.CreateNewElement("Element2D2N", 1, [1,2], KratosMultiphysics.Properties(0))

moving_params = KratosMultiphysics.Parameters("""{
                    "origin"                        : [-0.5,0.0,0.0],
                    "rotation_point"                : [-0.25,0.0,0.0],
                    "rotation_angle"                : 0.0,
                    "sizing_multiplier"             : 1.0
                }""")
angle=math.radians(-moving_params["rotation_angle"].GetDouble())
moving_params["rotation_angle"].SetDouble(angle)
KratosMultiphysics.CompressiblePotentialFlowApplication.MoveModelPartProcess(wake_model_part, moving_params).Execute()

use_discontinuous = True #Set to false to use continuous distance process

if use_discontinuous:
    KratosMultiphysics.CalculateDiscontinuousDistanceToSkinProcess2D(main_model_part,wake_model_part).Execute()
    for element in main_model_part.Elements:
        distances = element.GetValue(KratosMultiphysics.ELEMENTAL_DISTANCES)
        counter = 0

        npos = 0
        nneg = 0
        for counter in range(0,3):
            if distances[counter] > 0.0:
                npos += 1
            else:
                nneg += 1
        counter = 0
        if (npos>0 and nneg >0):
            for node in element.GetNodes():
                node.SetSolutionStepValue(KratosMultiphysics.DISTANCE,distances[counter])
                counter += 1
else:
    # Continuous distance process (does not work for volumeless bodies)
    KratosMultiphysics.CalculateDistanceToSkinProcess2D(main_model_part,wake_model_part).Execute()





from gid_output_process import GiDOutputProcess
gid_output = GiDOutputProcess(main_model_part,
                            "distance_test",
                            KratosMultiphysics.Parameters("""
                                {
                                    "result_file_configuration" : {
                                        "gidpost_flags": {
                                            "GiDPostMode": "GiD_PostBinary",
                                            "WriteDeformedMeshFlag": "WriteUndeformed",
                                            "WriteConditionsFlag": "WriteConditions",
                                            "MultiFileFlag": "SingleFile"
                                        },
                                        "nodal_results" : ["DISTANCE"]
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

