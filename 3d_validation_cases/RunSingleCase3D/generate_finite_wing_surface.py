# -*- coding: utf-8 -*-

###
### This file is generated automatically by SALOME v8.4.0 with dump python functionality
###

# Indicate parameters:
# Geometry
AOA = 5.0
Wing_span = 4.0

# Mesh
Airfoil_Mesh_Size = 0.01
Biggest_Airfoil_Mesh_Size = 0.05
Growth_Rate = 0.1

import sys
import salome

salome.salome_init()
theStudy = salome.myStudy

import salome_notebook
notebook = salome_notebook.NoteBook(theStudy)
import os
script_path = os.path.dirname(os.path.realpath(__file__))

###
### GEOM component
###

import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS


geompy = geomBuilder.New(theStudy)

# Create origin and axis
O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)

# Create naca 0012
Curve_UpperSurface_LE = geompy.MakeCurveParametric("t - 0.5", "0.0", "0.6*(0.2969*sqrt(t) - 0.1260*t - 0.3516*t**2 + 0.2843*t**3 - 0.1036*t**4)", 0, 0.5, 999, GEOM.Interpolation, True)
Curve_UpperSurface_TE = geompy.MakeCurveParametric("t - 0.5", "0.0", "0.6*(0.2969*sqrt(t) - 0.1260*t - 0.3516*t**2 + 0.2843*t**3 - 0.1036*t**4)", 0.5, 1, 999, GEOM.Interpolation, True)
Curve_LowerSurface_TE = geompy.MakeCurveParametric("t - 0.5", "0.0", "-0.6*(0.2969*sqrt(t) - 0.1260*t - 0.3516*t**2 + 0.2843*t**3 - 0.1036*t**4)", 0.5, 1, 999, GEOM.Interpolation, True)
Curve_LowerSurface_LE = geompy.MakeCurveParametric("t - 0.5", "0.0", "-0.6*(0.2969*sqrt(t) - 0.1260*t - 0.3516*t**2 + 0.2843*t**3 - 0.1036*t**4)", 0, 0.5, 999, GEOM.Interpolation, True)

# Put edges together
Wire_Airfoil = geompy.MakeWire([Curve_UpperSurface_LE, Curve_UpperSurface_TE, Curve_LowerSurface_TE, Curve_LowerSurface_LE], 1e-07)

# Rotate around center and angle AOA
geompy.Rotate(Wire_Airfoil, OY, AOA*math.pi/180.0)

# Extrude upper and lower surface
Extrusion_1 = geompy.MakePrismVecH(Wire_Airfoil, OY, Wing_span)

# Translate wire to make the face later on
Translation_Airfoil = geompy.MakeTranslationVectorDistance(Wire_Airfoil, OY, 4)

# Making lateral faces
Face_Airfoil_Left = geompy.MakeFaceWires([Wire_Airfoil], 1)
Face_Airfoil_Right = geompy.MakeFaceWires([Translation_Airfoil], 1)

# Fuse surfaces
Fuse_Wing = geompy.MakeFuseList([Extrusion_1, Face_Airfoil_Left, Face_Airfoil_Right], True, True)

# Explode edges
[Edge_LE,Edge_Left_LowerLE,Edge_Left_UpperLE,Edge_Right_LowerLE,Edge_Right_UpperLE,Edge_Middle_Lower,Edge_Middle_Upper,Edge_Left_LowerTE,Edge_Left_UpperTE,Edge_Right_LowerTE,Edge_Right_UpperTE,Edge_TE] = geompy.ExtractShapes(Fuse_Wing, geompy.ShapeType["EDGE"], True)

# Make groups for meshing later on

# Lateral leading edge airfoils
Auto_group_for_Sub_mesh_AirfoilLE = geompy.CreateGroup(Fuse_Wing, geompy.ShapeType["EDGE"])
geompy.UnionList(Auto_group_for_Sub_mesh_AirfoilLE, [Edge_Left_LowerLE, Edge_Left_UpperLE, Edge_Right_LowerLE, Edge_Right_UpperLE])

# Lateral trailing edge airfoils
Auto_group_for_Sub_mesh_AirfoilTE = geompy.CreateGroup(Fuse_Wing, geompy.ShapeType["EDGE"])
geompy.UnionList(Auto_group_for_Sub_mesh_AirfoilTE, [Edge_Left_LowerTE, Edge_Left_UpperTE, Edge_Right_LowerTE, Edge_Right_UpperTE])

# Leading and trailing edge
Auto_group_for_Sub_mesh_LETE = geompy.CreateGroup(Fuse_Wing, geompy.ShapeType["EDGE"])
geompy.UnionList(Auto_group_for_Sub_mesh_LETE, [Edge_LE, Edge_TE])

# Middle edges
Auto_group_for_Sub_mesh_Middle = geompy.CreateGroup(Fuse_Wing, geompy.ShapeType["EDGE"])
geompy.UnionList(Auto_group_for_Sub_mesh_Middle, [Edge_Middle_Lower, Edge_Middle_Upper])

# Adding to study to see in GUI
geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )
geompy.addToStudy( Curve_UpperSurface_LE, 'Curve_UpperSurface_LE' )
geompy.addToStudy( Curve_UpperSurface_TE, 'Curve_UpperSurface_TE' )
geompy.addToStudy( Curve_LowerSurface_TE, 'Curve_LowerSurface_TE' )
geompy.addToStudy( Curve_LowerSurface_LE, 'Curve_LowerSurface_LE' )
geompy.addToStudy( Wire_Airfoil, 'Wire_Airfoil' )
geompy.addToStudy( Extrusion_1, 'Extrusion_1' )
geompy.addToStudy( Translation_Airfoil, 'Translation_Airfoil' )
geompy.addToStudy( Face_Airfoil_Left, 'Face_Airfoil_Left' )
geompy.addToStudy( Face_Airfoil_Right, 'Face_Airfoil_Right' )
geompy.addToStudy( Fuse_Wing, 'Fuse_Wing' )
geompy.addToStudyInFather( Fuse_Wing, Edge_LE, 'Edge_LE' )
geompy.addToStudyInFather( Fuse_Wing, Edge_Left_LowerLE, 'Edge_Left_LowerLE' )
geompy.addToStudyInFather( Fuse_Wing, Edge_Left_UpperLE, 'Edge_Left_UpperLE' )
geompy.addToStudyInFather( Fuse_Wing, Edge_Right_LowerLE, 'Edge_Right_LowerLE' )
geompy.addToStudyInFather( Fuse_Wing, Edge_Right_UpperLE, 'Edge_Right_UpperLE' )
geompy.addToStudyInFather( Fuse_Wing, Edge_Middle_Lower, 'Edge_Middle_Lower' )
geompy.addToStudyInFather( Fuse_Wing, Edge_Middle_Upper, 'Edge_Middle_Upper' )
geompy.addToStudyInFather( Fuse_Wing, Edge_Left_LowerTE, 'Edge_Left_LowerTE' )
geompy.addToStudyInFather( Fuse_Wing, Edge_Left_UpperTE, 'Edge_Left_UpperTE' )
geompy.addToStudyInFather( Fuse_Wing, Edge_Right_LowerTE, 'Edge_Right_LowerTE' )
geompy.addToStudyInFather( Fuse_Wing, Edge_Right_UpperTE, 'Edge_Right_UpperTE' )
geompy.addToStudyInFather( Fuse_Wing, Edge_TE, 'Edge_TE' )
geompy.addToStudyInFather( Fuse_Wing, Auto_group_for_Sub_mesh_AirfoilLE, 'Auto_group_for_Sub-mesh_AirfoilLE' )
geompy.addToStudyInFather( Fuse_Wing, Auto_group_for_Sub_mesh_AirfoilTE, 'Auto_group_for_Sub-mesh_AirfoilTE' )
geompy.addToStudyInFather( Fuse_Wing, Auto_group_for_Sub_mesh_LETE, 'Auto_group_for_Sub-mesh_LETE' )
geompy.addToStudyInFather( Fuse_Wing, Auto_group_for_Sub_mesh_Middle, 'Auto_group_for_Sub-mesh_Middle' )

###
### SMESH component
###

import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder

# 2D mesh parameters
smesh = smeshBuilder.New(theStudy)
Mesh_Wing = smesh.Mesh(Fuse_Wing)
NETGEN_2D = Mesh_Wing.Triangle(algo=smeshBuilder.NETGEN_2D)
NETGEN_2D_Parameters_1 = NETGEN_2D.Parameters()
NETGEN_2D_Parameters_1.SetMaxSize( Biggest_Airfoil_Mesh_Size )
NETGEN_2D_Parameters_1.SetOptimize( 1 )
NETGEN_2D_Parameters_1.SetFineness( 5 )
NETGEN_2D_Parameters_1.SetGrowthRate( Growth_Rate )
NETGEN_2D_Parameters_1.SetMinSize( Airfoil_Mesh_Size )
NETGEN_2D_Parameters_1.SetUseSurfaceCurvature( 1 )
NETGEN_2D_Parameters_1.SetQuadAllowed( 0 )
NETGEN_2D_Parameters_1.SetSecondOrder( 0 )
NETGEN_2D_Parameters_1.SetFuseEdges( 1 )

# Lateral leading edge airfoils
Regular_1D = Mesh_Wing.Segment(geom=Auto_group_for_Sub_mesh_AirfoilLE)
Start_and_End_Length_LE = Regular_1D.StartEndLength(Airfoil_Mesh_Size,Biggest_Airfoil_Mesh_Size,[])
Start_and_End_Length_LE.SetObjectEntry( 'Fuse_Wing' )

# Lateral trailing edge airfoils
Regular_1D_1 = Mesh_Wing.Segment(geom=Auto_group_for_Sub_mesh_AirfoilTE)
Start_and_End_Length_TE = Regular_1D_1.StartEndLength(Biggest_Airfoil_Mesh_Size,Airfoil_Mesh_Size,[])
Start_and_End_Length_TE.SetObjectEntry( 'Fuse_Wing' )

# Leading and trailing edge
Regular_1D_2 = Mesh_Wing.Segment(geom=Auto_group_for_Sub_mesh_LETE)
Local_Length_LETE = Regular_1D_2.LocalLength(Airfoil_Mesh_Size,None,1e-07)

# Middle edges
Regular_1D_3 = Mesh_Wing.Segment(geom=Auto_group_for_Sub_mesh_Middle)
Local_Length_Middle = Regular_1D_3.LocalLength(Biggest_Airfoil_Mesh_Size,None,1e-07)

# Compute mesh
isDone = Mesh_Wing.Compute()
Sub_mesh_AirfoilLE = Regular_1D.GetSubMesh()
Sub_mesh_AirfoilTE = Regular_1D_1.GetSubMesh()
Sub_mesh_LETE = Regular_1D_2.GetSubMesh()
Sub_mesh_Middle = Regular_1D_3.GetSubMesh()

NumberOfNodes = Mesh_Wing.NbNodes()
NumberOfElements = Mesh_Wing.NbTriangles()
print(' Information about volume mesh:')
print(' Number of nodes       :', NumberOfNodes)
print(' Number of elements    :', NumberOfElements)


## Set names of Mesh objects
smesh.SetName(NETGEN_2D.GetAlgorithm(), 'NETGEN 2D')
smesh.SetName(Regular_1D.GetAlgorithm(), 'Regular_1D')
smesh.SetName(Start_and_End_Length_LE, 'Start and End Length_LE')
smesh.SetName(NETGEN_2D_Parameters_1, 'NETGEN 2D Parameters_1')
smesh.SetName(Local_Length_Middle, 'Local Length_Middle')
smesh.SetName(Start_and_End_Length_TE, 'Start and End Length_TE')
smesh.SetName(Local_Length_LETE, 'Local Length_LETE')
smesh.SetName(Mesh_Wing.GetMesh(), 'Mesh_Wing')
smesh.SetName(Sub_mesh_LETE, 'Sub-mesh_LETE')
smesh.SetName(Sub_mesh_AirfoilTE, 'Sub-mesh_AirfoilTE')
smesh.SetName(Sub_mesh_AirfoilLE, 'Sub-mesh_AirfoilLE')
smesh.SetName(Sub_mesh_Middle, 'Sub-mesh_Middle')

# Export meshes into data files
try:
  Mesh_Wing.ExportDAT( script_path + '/salome_output/Mesh_Wing.dat' )
  pass
except:
  print 'ExportDAT() failed. Invalid file name?'

# Saving file to open from salome's gui
file_name = "/salome_files/generate_finite_wing_surface.hdf"
salome.myStudyManager.SaveAs(script_path + file_name, salome.myStudy, 0)

if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser(True)
