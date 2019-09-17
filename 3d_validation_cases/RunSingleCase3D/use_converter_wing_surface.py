# Note that this has to be on the path in order to work, or you manually specify the path
import kratos_io_utilities as kratos_utils
import global_utilities as global_utils
from math import log10, floor
import os

def round_to_1(x):
    return round(x, -int(floor(log10(abs(x)))))

script_path = os.path.dirname(os.path.realpath(__file__))
salome_output_path = script_path + '/salome_output'
mdpa_path = script_path + '/case'


print('Writing mdpa...')
model = kratos_utils.MainModelPart() # Main mesh object to which we will add the submeshes (Kratos Name: ModelPart)

# Specifying the names of the submeshes (Kratos Name: SubModelPart)
smp_dict_body_surface   = {"smp_name": "Body3D_Body_Auto1"}

file_name_body_surface = salome_output_path + '/Mesh_Wing.dat'

def ReadDatFile(file_name):
    valid_file, nodes, geom_entities = global_utils.ReadAndParseSalomeDatFile(os.path.join(os.getcwd(),file_name))
    if not valid_file:
        raise Exception("Invalid File!\n" + file_name)
    return nodes, geom_entities

nodes_body_surface,     geom_entities_body_surface  = ReadDatFile(file_name_body_surface)

# Here we specify which Kratos-entities will be created from the general geometric entities
mesh_dict_body_surface = {'write_smp': 1,
                       'entity_creation': {203: {'Condition': {'SurfaceCondition3D3N': '0'}}}}

model.AddMesh(smp_dict_body_surface,   mesh_dict_body_surface,    nodes_body_surface,    geom_entities_body_surface)

mdpa_info = "mdpa for demonstration purposes"
mdpa_file_name = mdpa_path + '/salome_wing_surface'

model.WriteMesh(mdpa_file_name, mdpa_info)
