import KratosMultiphysics
with open("ProjectParameters.json",'r') as parameter_file:
	parameters = KratosMultiphysics.Parameters(parameter_file.read())
input_filename='Meshes/'+parameters["solver_settings"]["model_import_settings"]["input_filename"].GetString()
model=KratosMultiphysics.Model()
model_part=model.CreateModelPart('main')
KratosMultiphysics.ModelPartIO(input_filename).ReadModelPart(model_part)
if not model_part.HasSubModelPart('Body2D_Body'):
    body_sub_model=model_part.CreateSubModelPart('Body2D_Body')
    node_id_list=[]
    condition_id_list=[]
    for subs in model_part.SubModelParts:
        if "Upper" in subs.Name or "Lower" in subs.Name:
            for node in subs.Nodes:
                if not node.Id in node_id_list:
                    body_sub_model.Nodes.append(node)
                    node_id_list.append(node.Id)
                else:
                    print("Ignoring repeated node id:",node.Id)
            for condition in subs.Conditions:
                if not condition.Id in condition_id_list:
                    body_sub_model.Conditions.append(condition)
                    condition_id_list.append(condition.Id)
                else:
                    print("Ignoring repeated condition id:",condition.Id)
    node_id_list.sort()
    condition_id_list.sort()
    with open(input_filename+'.mdpa', 'a') as mdpa_file:
                mdpa_file.write("\n\n")
                mdpa_file.write("Begin SubModelPart Body2D_Body \n")
                mdpa_file.write("   Begin SubModelPartNodes \n")
                for node in node_id_list:
                    mdpa_file.write('     {}\n'.format(node))
                mdpa_file.write("   End SubModelPartNodes \n")
                mdpa_file.write("   Begin SubModelPartElements \n")
                mdpa_file.write("   End SubModelPartElements \n")
                mdpa_file.write("   Begin SubModelPartConditions \n")
                for condition in condition_id_list:
                    mdpa_file.write('     {}\n'.format(condition))
                mdpa_file.write("   End SubModelPartConditions \n")
                mdpa_file.write("End SubModelPart \n")




print(model_part)


# def ImportModelPart(self):
#     # we can use the default implementation in the base class
#     self._ImportModelPart(self.main_model_part,self.settings["model_import_settings"])

#     if not self.main_model_part.HasSubModelPart('Body2D_Body'):
#         body_sub_model=self.main_model_part.CreateSubModelPart('Body2D_Body')
#         node_id_list=[]
#         condition_id_list=[]
#         for subs in self.main_model_part.SubModelParts:
#             if "Upper" in subs.Name or "Lower" in subs.Name:
#                 for node in subs.Nodes:
#                     if not node.Id in node_id_list:
#                         body_sub_model.Nodes.append(node)
#                         node_id_list.append(node.Id)
#                     else:
#                         print("Ignoring repeated node id:",node.Id)
#                 for condition in subs.Conditions:
#                     if not condition.Id in condition_id_list:
#                         body_sub_model.Conditions.append(condition)
#                         condition_id_list.append(condition.Id)
#                     else:
#                         print("Ignoring repeated condition id:",condition.Id)