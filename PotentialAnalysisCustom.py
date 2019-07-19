from __future__ import print_function, absolute_import, division #makes KratosMultiphysics backward compatible with python 2.6 and 2.7
import KratosMultiphysics
import KratosMultiphysics.MeshingApplication as KratosMeshing
from KratosMultiphysics.CompressiblePotentialFlowApplication.potential_flow_analysis import PotentialFlowAnalysis
import numpy as np
import os
import matplotlib.pyplot as plt



class PotentialAnalysisCustom(PotentialFlowAnalysis):

	def __init__(self,model,parameters):

		self.case=parameters["solver_settings"]["formulation"]["element_type"].GetString()
		self.input_file = parameters["solver_settings"]["model_import_settings"]["input_filename"].GetString()
		parameters["solver_settings"]["model_import_settings"]["input_filename"].SetString('./Meshes/'+self.input_file)
		boundary_processes=parameters["processes"]["boundary_conditions_process_list"]
		python_module=boundary_processes[0]["python_module"].GetString()

		if python_module == "level_set_remeshing_process":
			self.is_embedded = True
			rotation_angle=boundary_processes[0]["Parameters"]["moving_parameters"]["rotation_angle"].GetDouble()
			skin_model_part_name=boundary_processes[0]["Parameters"]["skin_model_part_name"].GetString()
			self.embedded_remeshing_flag = boundary_processes[0]["Parameters"]["remeshing_flag"].GetBool()
			self.problem_name=self.case+"_"+self.input_file+"_"+skin_model_part_name+"_"+str(rotation_angle)
			if self.embedded_remeshing_flag:
				self.problem_name=self.problem_name+"_REMESH_"+str(boundary_processes[0]["Parameters"]["metric_parameters"]["minimal_size"].GetDouble())
		else:
			self.embedded_remeshing_flag = False
			self.is_embedded = False
			self.problem_name=self.case+"_"+self.input_file

		self._CheckIfFileExists()

		if not os.path.exists('./gid_output/'):
			os.makedirs('./gid_output/')
		parameters["output_processes"]["gid_output"][0]["Parameters"]["output_name"].SetString('./gid_output/'+self.problem_name)

		super(PotentialAnalysisCustom,self).__init__(model, parameters)

		self.settings = parameters
		self.remeshing_flag =  False #parameters["custom_settings"]["remeshing_flag"].GetBool()


	def Finalize(self):
		super(PotentialAnalysisCustom,self).Finalize()

		if not os.path.exists('./json_output/'):
			os.makedirs('./json_output/')
		file=open('./json_output/'+self.problem_name+'.json','w')
		file.write(self.settings.PrettyPrintJsonString())

		if "embedded" in self.case:
			self._PostProcessEmbedded()
		else:
			pass

		if self.remeshing_flag:
			self._RefineMesh()


	def _CheckIfFileExists(self):
		counter=0
		output_name=self.problem_name
		while os.path.isfile('./gid_output/'+output_name+"_0.post.res") or os.path.isfile('./gid_output/'+output_name+".post.bin"):
			counter += 1
			output_name = self.problem_name+"_"+str(counter)
		self.problem_name = output_name

	def _PostProcessEmbedded(self):

		if not os.path.exists('./Figures/'):
			os.makedirs('./Figures/')

		x_upper=[]
		cp_upper=[]
		x_lower=[]
		cp_lower=[]
		for element in self._GetSolver().main_model_part.Elements:
			npos = 0
			nneg = 0
			for node in element.GetNodes():
				distance=node.GetSolutionStepValue(KratosMultiphysics.CompressiblePotentialFlowApplication.GEOMETRY_DISTANCE)
				if distance>0:
					npos += 1
				else:
					nneg += 1

			if npos>0 and nneg>0:
				gp_x=element.GetGeometry().Center().X
				pressure=element.GetValue(KratosMultiphysics.PRESSURE_COEFFICIENT)
				normal=element.GetValue(KratosMultiphysics.NORMAL)
				if normal[1]<=0:
					x_upper.append(gp_x)
					cp_upper.append(pressure)
				else:
					x_lower.append(gp_x)
					cp_lower.append(pressure)
		max_x=max(max(x_upper),max(x_lower))
		min_x=min(min(x_upper),min(x_lower))
		for i in range(0,len(x_upper)):
			x_upper[i]=(x_upper[i]-min_x)/abs(max_x-min_x)
		for i in range(0,len(x_lower)):
			x_lower[i]=(x_lower[i]-min_x)/abs(max_x-min_x)

		plt.plot(x_upper,cp_upper,'.',label='Upper surface')
		plt.plot(x_lower,cp_lower,'r.',label='Lower surface')

		Cl=self._GetSolver().main_model_part.ProcessInfo.GetValue(KratosMultiphysics.CompressiblePotentialFlowApplication.LIFT_COEFFICIENT)
		Cd=self._GetSolver().main_model_part.ProcessInfo.GetValue(KratosMultiphysics.CompressiblePotentialFlowApplication.DRAG_COEFFICIENT)
		title="Cl: %.5f, Cd: %.5f" % (Cl,Cd)
		plt.title(title)
		plt.legend()
		plt.gca().invert_yaxis()
		plt.savefig('Figures/'+self.problem_name+'.png', bbox_inches='tight')
		plt.close('all')


		# with open('dats/cp_distribution_naca0012.dat') as file_cp_ref:
		# 	lines=file_cp_ref.readlines()
		# 	x_ref=[]
		# 	cp_ref=[]
		# 	for line in lines:
		# 		x_ref.append(float(line.split(' ')[0]))
		# 		cp_ref.append(float(line.split(' ')[1]))
		# max_x=max(x_ref)
		# min_x=min(x_ref)
		# for i in range(0,len(x_ref)):
		# 	x_ref[i]=(x_ref[i]-min_x)/abs(max_x-min_x)

		with open('dats/'+self.problem_name+'_UpperCP.dat','w') as dat_file:
			for i in range(len(x_upper)):
				dat_file.write('%f %f \n' % (x_upper[i], cp_upper[i]))
		with open('dats/'+self.problem_name+'_LowerCP.dat','w') as dat_file:
			for i in range(len(x_lower)):
				dat_file.write('%f %f \n' % (x_lower[i], cp_lower[i]))

		# plt.plot(x_upper,cp_upper,'.',label='Upper surface')
		# plt.plot(x_lower,cp_lower,'r.',label='Lower surface')
		# plt.plot(x_ref, cp_ref ,'k.',label='Body fitted')
		# title="Cl: %.5f, Cd: %.5f" % (Cl,Cd)
		# plt.title(title)
		# plt.legend()
		# plt.gca().invert_yaxis()
		# plt.savefig('Figures/'+self.problem_name+'_COMPARISON.png', bbox_inches='tight')
		# plt.close('all')

		self._CreateGidControlOutput("embedded_all_active")

		if self.embedded_remeshing_flag:
			computational_name = self._GetSolver().GetComputingModelPart().Name
			self._GetSolver().main_model_part.RemoveSubModelPart(computational_name)
			self._GetSolver().main_model_part.RemoveSubModelPart("trailing_edge_model_part")
			self._GetSolver().main_model_part.RemoveSubModelPart("deactivated")
			self._GetSolver().main_model_part.RemoveSubModelPart("boundary")

			self._GetSolver().main_model_part.CreateNewProperties(0)
			# self._GetSolver().main_model_part.CreateNewProperties(1)
			KratosMultiphysics.ModelPartIO('./Meshes/'+self.problem_name, KratosMultiphysics.IO.WRITE | KratosMultiphysics.IO.MESH_ONLY).WriteModelPart(self._GetSolver().main_model_part)
			print("Remeshed mesh saved as: ", self.problem_name)

	def _ComputeHessianMetric(self):
		metric_parameters = KratosMultiphysics.Parameters("""
			{
				"minimal_size"                        : 0.00001,
				"maximal_size"                        : 1000.0,
				"enforce_current"                     : false,
				"hessian_strategy_parameters":
				{
					"metric_variable"                  : ["VELOCITY_POTENTIAL"],
					"estimate_interpolation_error"         : false,
					"interpolation_error"                  : 1e-3
				},
				"anisotropy_remeshing"                : true
			}    """)

		hessian_metric = KratosMeshing.ComputeHessianSolMetricProcess(self._GetSolver().main_model_part,KratosMultiphysics.CompressiblePotentialFlowApplication.VELOCITY_POTENTIAL, metric_parameters)

		hessian_metric.Execute()
	def _ComputeCustomHessianMetric(self):
		custom_gradient = KratosMultiphysics.CompressiblePotentialFlowApplication.ComputeCustomNodalGradientProcess(self._GetSolver().main_model_part,KratosMultiphysics.VELOCITY, KratosMultiphysics.NODAL_AREA)
		custom_gradient.Execute()
		metric_parameters = KratosMultiphysics.Parameters("""
			{
				"minimal_size"                        : 0.001,
				"maximal_size"                        : 1000.0,
				"enforce_current"                     : false,
				"hessian_strategy_parameters":
				{
					"estimate_interpolation_error"         : false,
					"interpolation_error"                  : 1e-2
				},
				"anisotropy_remeshing"                : true
			}    """)

		# for node in self._GetSolver().main_model_part.Nodes:
		# 	vector=node.GetValue(KratosMultiphysics.CompressiblePotentialFlowApplication.VELOCITY_LOWER)
		# 	norm=np.linalg.norm(vector)
		# 	node.SetSolutionStepValue(KratosMultiphysics.PRESSURE,norm)
		print(self._GetSolver().main_model_part)
		metric = KratosMultiphysics.MeshingApplication.ComputeHessianSolMetricProcess(self._GetSolver().main_model_part,KratosMultiphysics.VELOCITY_X, metric_parameters)
		metric.Execute()
		metric = KratosMultiphysics.MeshingApplication.ComputeHessianSolMetricProcess(self._GetSolver().main_model_part,KratosMultiphysics.VELOCITY_Y, metric_parameters)
		metric.Execute()
		if self.is_embedded:
			find_nodal_h = KratosMultiphysics.FindNodalHNonHistoricalProcess(self._GetSolver().main_model_part)
			find_nodal_h.Execute()
			metric_tensor_2d = KratosMultiphysics.Vector(3)
			for node in self._GetSolver().main_model_part.Nodes:
				if node.GetSolutionStepValue(KratosMultiphysics.CompressiblePotentialFlowApplication.GEOMETRY_DISTANCE)<0.00:
					nodal_h = node.GetValue(KratosMultiphysics.NODAL_H)
					metric_tensor_2d[0] = 1.0/nodal_h/nodal_h
					metric_tensor_2d[1] = 1.0/nodal_h/nodal_h
					metric_tensor_2d[2] = 0.0
					node.SetValue(KratosMultiphysics.MeshingApplication.METRIC_TENSOR_2D,metric_tensor_2d)
	def _RefineMesh(self):
		# Compute nodal_h
		find_nodal_h = KratosMultiphysics.FindNodalHNonHistoricalProcess(self._GetSolver().main_model_part)
		find_nodal_h.Execute()
		self._ComputeCustomHessianMetric()
		self._CreateGidControlOutput("hessian_metric")
		# Execute remeshing process

		mmg_parameters = KratosMultiphysics.Parameters("""
        {
            "discretization_type"                  : "STANDARD",
            "save_external_files"              : false,
            "initialize_entities"              : false,
            "echo_level"                       : 0
        }
        """)
		MmgProcess = KratosMeshing.MmgProcess2D(self._GetSolver().main_model_part,mmg_parameters)
		MmgProcess.Execute()
		if not self.embedded_remeshing_flag:
			computational_name = self._GetSolver().GetComputingModelPart().Name
			self._GetSolver().main_model_part.RemoveSubModelPart(computational_name)

		if self.is_embedded:
			self._GetSolver().main_model_part.RemoveSubModelPart("trailing_edge_model_part")
			self._GetSolver().main_model_part.RemoveSubModelPart("deactivated")
			self._GetSolver().main_model_part.RemoveSubModelPart("boundary")

		self._CreateGidControlOutput("remeshed_hessian")
		KratosMultiphysics.ModelPartIO('Meshes/'+self.input_file+'_HESSIANED', KratosMultiphysics.IO.WRITE | KratosMultiphysics.IO.MESH_ONLY).WriteModelPart(self._GetSolver().main_model_part)
		print("Remeshed mesh saved as: ", self.input_file+'_HESSIANED')

	def _CreateGidControlOutput(self, output_name):
		for element in self._GetSolver().main_model_part.Elements:
			element.Set(KratosMultiphysics.INLET,False)
			if element.IsNot(KratosMultiphysics.ACTIVE):
				element.Set(KratosMultiphysics.INLET,True)
			element.Set(KratosMultiphysics.ACTIVE,True)
		from gid_output_process import GiDOutputProcess
		gid_output = GiDOutputProcess(
				self._GetSolver().main_model_part,
				output_name,
				KratosMultiphysics.Parameters("""
					{
						"result_file_configuration" : {
							"gidpost_flags": {
								"GiDPostMode": "GiD_PostBinary",
								"MultiFileFlag": "SingleFile"
							},
							"nodal_results"       : ["VELOCITY_POTENTIAL","AUXILIARY_VELOCITY_POTENTIAL","GEOMETRY_DISTANCE"],
							"nodal_nonhistorical_results": ["METRIC_TENSOR_2D","TEMPERATURE","DISTANCE","TRAILING_EDGE"],
                        	"gauss_point_results" : ["PRESSURE_COEFFICIENT","VELOCITY","WAKE","KUTTA"],
							"nodal_flags_results": [],
                        	"elemental_conditional_flags_results": ["TO_SPLIT","THERMAL","STRUCTURE"]
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

		for element in self._GetSolver().main_model_part.Elements:
			if element.Is(KratosMultiphysics.INLET):
				element.Set(KratosMultiphysics.ACTIVE,False)

if __name__ == "__main__":
	from sys import argv

	if len(argv) > 2:
		err_msg =  'Too many input arguments!\n'
		err_msg += 'Use this script in the following way:\n'
		err_msg += '- With default parameter file (assumed to be called "ProjectParameters.json"):\n'
		err_msg += '    "python fluid_dynamics_analysis.py"\n'
		err_msg += '- With custom parameter file:\n'
		err_msg += '    "python fluid_dynamics_analysis.py <my-parameter-file>.json"\n'
		raise Exception(err_msg)

	if len(argv) == 2: # ProjectParameters is being passed from outside
		parameter_file_name = argv[1]
	else: # using default name
		parameter_file_name = "ProjectParameters.json"

	import time
	ini_time = time.time()
	with open(parameter_file_name,'r') as parameter_file:
		parameters = KratosMultiphysics.Parameters(parameter_file.read())
	model = KratosMultiphysics.Model()
	simulation = PotentialAnalysisCustom(model, parameters)
	simulation.Run()
	print("Time elapsed:", time.time()-ini_time)




