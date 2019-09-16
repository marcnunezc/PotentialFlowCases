# -*- coding: utf-8 -*-

###
### This file is generated automatically by SALOME v8.4.0 with dump python functionality
###

import sys
import salome

salome.salome_init()
theStudy = salome.myStudy

import salome_notebook
notebook = salome_notebook.NoteBook(theStudy)
sys.path.insert( 0, r'/home/inigo/simulations/wing/02_finite_wing/salome_output')

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

# Create naca0012
Curve_UpperSurface_LE = geompy.MakeCurveParametric("t - 0.5", "0.0", "0.6*(0.2969*sqrt(t) - 0.1260*t - 0.3516*t**2 + 0.2843*t**3 - 0.1036*t**4)", 0, 0.5, 999, GEOM.Interpolation, True)
Curve_UpperSurface_TE = geompy.MakeCurveParametric("t - 0.5", "0.0", "0.6*(0.2969*sqrt(t) - 0.1260*t - 0.3516*t**2 + 0.2843*t**3 - 0.1036*t**4)", 0.5, 1, 999, GEOM.Interpolation, True)
Curve_LowerSurface_TE = geompy.MakeCurveParametric("t - 0.5", "0.0", "-0.6*(0.2969*sqrt(t) - 0.1260*t - 0.3516*t**2 + 0.2843*t**3 - 0.1036*t**4)", 0.5, 1, 999, GEOM.Interpolation, True)
Curve_LowerSurface_LE = geompy.MakeCurveParametric("t - 0.5", "0.0", "-0.6*(0.2969*sqrt(t) - 0.1260*t - 0.3516*t**2 + 0.2843*t**3 - 0.1036*t**4)", 0, 0.5, 999, GEOM.Interpolation, True)

# Create face
Face_Airfoil = geompy.MakeFaceWires([Curve_UpperSurface_LE, Curve_UpperSurface_TE, Curve_LowerSurface_TE, Curve_LowerSurface_LE], 1)

# Rotate around center to AOA
geompy.Rotate(Face_Airfoil, OY, 5*math.pi/180.0)

# Extrusion of the wing
Extrusion_Wing = geompy.MakePrismVecH2Ways(Face_Airfoil, OY, 2)

# Domain generation
Face_Domain = geompy.MakeFaceHW(10, 10, 3)
Extrusion_Domain = geompy.MakePrismVecH2Ways(Face_Domain, OY, 5)

# Cut wing from the domain
Cut_Domain = geompy.MakeCutList(Extrusion_Domain, [Extrusion_Wing], True)

# Explode faces and edges
[Face_Inlet,Face_Left_Wall,Face_Left_Wing,Face_Lower_LE,Face_Upper_LE,Face_Down_Wall,Face_Top_Wall,Face_Right_Wing,Face_Lower_TE,Face_Upper_TE,Face_Right_Wall,Face_Outlet] = geompy.ExtractShapes(Cut_Domain, geompy.ShapeType["FACE"], True)

# Extruding
[Edge_1,Edge_2,Edge_3,Edge_4] = geompy.ExtractShapes(Face_Inlet, geompy.ShapeType["EDGE"], True)
[Edge_Left_LowerLE,Edge_6,Edge_7,Edge_Left_UpperLE] = geompy.ExtractShapes(Face_Left_Wall, geompy.ShapeType["EDGE"], True)
[Edge_Left_LowerLE,Edge_Left_UpperLE,Edge_Left_Lower_TE,Edge_Left_Upper_TE] = geompy.ExtractShapes(Face_Left_Wing, geompy.ShapeType["EDGE"], True)
[Edge_LE,Edge_Right_LowerLE,Edge_Right_UpperLE,Edge_Middle_Lower] = geompy.ExtractShapes(Face_Lower_LE, geompy.ShapeType["EDGE"], True)
[Edge_Right_LowerLE,Edge_Right_UpperLE,Edge_Right_LowerTE,Edge_Middle_Upper] = geompy.ExtractShapes(Face_Upper_LE, geompy.ShapeType["EDGE"], True)
[Edge_Right_LowerLE,Edge_Right_UpperLE,Edge_Right_LowerTE,Edge_Right_UpperTE] = geompy.ExtractShapes(Face_Right_Wing, geompy.ShapeType["EDGE"], True)
[Edge_5,Edge_8,Edge_9,Edge_TE] = geompy.ExtractShapes(Face_Lower_TE, geompy.ShapeType["EDGE"], True)
[Edge_5,Edge_8,Edge_9,Edge_10] = geompy.ExtractShapes(Face_Right_Wall, geompy.ShapeType["EDGE"], True)
[Edge_5,Edge_10,Edge_11,Edge_12] = geompy.ExtractShapes(Face_Outlet, geompy.ShapeType["EDGE"], True)

# Making groups for submeshes

# Far field surface
Auto_group_for_Sub_mesh_Far_Field_Surface = geompy.CreateGroup(Cut_Domain, geompy.ShapeType["FACE"])
geompy.UnionList(Auto_group_for_Sub_mesh_Far_Field_Surface, [Face_Inlet, Face_Left_Wall, Face_Down_Wall, Face_Top_Wall, Face_Right_Wall, Face_Outlet])

# Wing surface
Auto_group_for_Sub_mesh_Wing_Surface = geompy.CreateGroup(Cut_Domain, geompy.ShapeType["FACE"])
geompy.UnionList(Auto_group_for_Sub_mesh_Wing_Surface, [Face_Left_Wing, Face_Lower_LE, Face_Upper_LE, Face_Right_Wing, Face_Lower_TE, Face_Upper_TE])

# Far field edges
Auto_group_for_Sub_mesh_Far_Field_Edges = geompy.CreateGroup(Cut_Domain, geompy.ShapeType["EDGE"])
geompy.UnionList(Auto_group_for_Sub_mesh_Far_Field_Edges, [Edge_1, Edge_2, Edge_3, Edge_4, Edge_6, Edge_7, Edge_8, Edge_9, Edge_5, Edge_10, Edge_11, Edge_12])

# TE Airfoil edges
Auto_group_for_Sub_mesh_LE_Airfoils = geompy.CreateGroup(Cut_Domain, geompy.ShapeType["EDGE"])
geompy.UnionList(Auto_group_for_Sub_mesh_LE_Airfoils, [Edge_Left_LowerLE, Edge_Left_UpperLE, Edge_Right_LowerLE, Edge_Right_UpperLE])

# LE Airfoil edges
Auto_group_for_Sub_mesh_TE_Airfoils = geompy.CreateGroup(Cut_Domain, geompy.ShapeType["EDGE"])
geompy.UnionList(Auto_group_for_Sub_mesh_TE_Airfoils, [Edge_Left_Lower_TE, Edge_Left_Upper_TE, Edge_Right_LowerTE, Edge_Right_UpperTE])

# LETE edges
Auto_group_for_Sub_mesh_LETE = geompy.CreateGroup(Cut_Domain, geompy.ShapeType["EDGE"])
geompy.UnionList(Auto_group_for_Sub_mesh_LETE, [Edge_LE, Edge_TE])

# Middle
Auto_group_for_Sub_mesh_Middle = geompy.CreateGroup(Cut_Domain, geompy.ShapeType["EDGE"])
geompy.UnionList(Auto_group_for_Sub_mesh_Middle, [Edge_Middle_Lower, Edge_Middle_Upper])

# Adding to study
geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )
geompy.addToStudy( Curve_UpperSurface_LE, 'Curve_UpperSurface_LE' )
geompy.addToStudy( Curve_UpperSurface_TE, 'Curve_UpperSurface_TE' )
geompy.addToStudy( Curve_LowerSurface_TE, 'Curve_LowerSurface_TE' )
geompy.addToStudy( Curve_LowerSurface_LE, 'Curve_LowerSurface_LE' )
geompy.addToStudy( Face_Airfoil, 'Face_Airfoil' )
geompy.addToStudy( Extrusion_Wing, 'Extrusion_Wing' )
geompy.addToStudy( Face_Domain, 'Face_Domain' )
geompy.addToStudy( Extrusion_Domain, 'Extrusion_Domain' )
geompy.addToStudy( Cut_Domain, 'Cut_Domain' )
geompy.addToStudyInFather( Cut_Domain, Face_Inlet, 'Face_Inlet' )
geompy.addToStudyInFather( Cut_Domain, Face_Left_Wall, 'Face_Left_Wall' )
geompy.addToStudyInFather( Cut_Domain, Face_Left_Wing, 'Face_Left_Wing' )
geompy.addToStudyInFather( Cut_Domain, Face_Lower_LE, 'Face_Lower_LE' )
geompy.addToStudyInFather( Cut_Domain, Face_Upper_LE, 'Face_Upper_LE' )
geompy.addToStudyInFather( Cut_Domain, Face_Down_Wall, 'Face_Down_Wall' )
geompy.addToStudyInFather( Cut_Domain, Face_Top_Wall, 'Face_Top_Wall' )
geompy.addToStudyInFather( Cut_Domain, Face_Right_Wing, 'Face_Right_Wing' )
geompy.addToStudyInFather( Cut_Domain, Face_Lower_TE, 'Face_Lower_TE' )
geompy.addToStudyInFather( Cut_Domain, Face_Upper_TE, 'Face_Upper_TE' )
geompy.addToStudyInFather( Cut_Domain, Face_Right_Wall, 'Face_Right_Wall' )
geompy.addToStudyInFather( Cut_Domain, Face_Outlet, 'Face_Outlet' )
geompy.addToStudyInFather( Face_Inlet, Edge_1, 'Edge_1' )
geompy.addToStudyInFather( Face_Inlet, Edge_2, 'Edge_2' )
geompy.addToStudyInFather( Face_Inlet, Edge_3, 'Edge_3' )
geompy.addToStudyInFather( Face_Inlet, Edge_4, 'Edge_4' )
geompy.addToStudyInFather( Face_Left_Wing, Edge_Left_LowerLE, 'Edge_Left_LowerLE' )
geompy.addToStudyInFather( Face_Left_Wall, Edge_6, 'Edge_6' )
geompy.addToStudyInFather( Face_Left_Wall, Edge_7, 'Edge_7' )
geompy.addToStudyInFather( Face_Left_Wing, Edge_Left_UpperLE, 'Edge_Left_UpperLE' )
geompy.addToStudyInFather( Face_Left_Wing, Edge_Left_Lower_TE, 'Edge_Left_Lower_TE' )
geompy.addToStudyInFather( Face_Left_Wing, Edge_Left_Upper_TE, 'Edge_Left_Upper_TE' )
geompy.addToStudyInFather( Face_Lower_LE, Edge_LE, 'Edge_LE' )
geompy.addToStudyInFather( Face_Right_Wing, Edge_Right_LowerLE, 'Edge_Right_LowerLE' )
geompy.addToStudyInFather( Face_Right_Wing, Edge_Right_UpperLE, 'Edge_Right_UpperLE' )
geompy.addToStudyInFather( Face_Lower_LE, Edge_Middle_Lower, 'Edge_Middle_Lower' )
geompy.addToStudyInFather( Face_Right_Wing, Edge_Right_LowerTE, 'Edge_Right_LowerTE' )
geompy.addToStudyInFather( Face_Upper_LE, Edge_Middle_Upper, 'Edge_Middle_Upper' )
geompy.addToStudyInFather( Face_Right_Wing, Edge_Right_UpperTE, 'Edge_Right_UpperTE' )
geompy.addToStudyInFather( Face_Outlet, Edge_5, 'Edge_5' )
geompy.addToStudyInFather( Face_Right_Wall, Edge_8, 'Edge_8' )
geompy.addToStudyInFather( Face_Right_Wall, Edge_9, 'Edge_9' )
geompy.addToStudyInFather( Face_Lower_TE, Edge_TE, 'Edge_TE' )
geompy.addToStudyInFather( Face_Outlet, Edge_10, 'Edge_10' )
geompy.addToStudyInFather( Face_Outlet, Edge_11, 'Edge_11' )
geompy.addToStudyInFather( Face_Outlet, Edge_12, 'Edge_12' )
geompy.addToStudyInFather( Cut_Domain, Auto_group_for_Sub_mesh_Far_Field_Surface, 'Auto_group_for_Sub-mesh_Far_Field_Surface' )
geompy.addToStudyInFather( Cut_Domain, Auto_group_for_Sub_mesh_Wing_Surface, 'Auto_group_for_Sub-mesh_Wing_Surface' )
geompy.addToStudyInFather( Cut_Domain, Auto_group_for_Sub_mesh_Far_Field_Edges, 'Auto_group_for_Sub-mesh_Far_Field_Edges' )
geompy.addToStudyInFather( Cut_Domain, Auto_group_for_Sub_mesh_LE_Airfoils, 'Auto_group_for_Sub-mesh_LE_Airfoils' )
geompy.addToStudyInFather( Cut_Domain, Auto_group_for_Sub_mesh_TE_Airfoils, 'Auto_group_for_Sub-mesh_TE_Airfoils' )
geompy.addToStudyInFather( Cut_Domain, Auto_group_for_Sub_mesh_LETE, 'Auto_group_for_Sub-mesh_LETE' )
geompy.addToStudyInFather( Cut_Domain, Auto_group_for_Sub_mesh_Middle, 'Auto_group_for_Sub-mesh_Middle' )

###
### SMESH component
###

import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder

smesh = smeshBuilder.New(theStudy)

# Set NETGEN 3D
Mesh_Domain = smesh.Mesh(Cut_Domain)
NETGEN_3D = Mesh_Domain.Tetrahedron()
NETGEN_3D_Parameters_1 = NETGEN_3D.Parameters()
NETGEN_3D_Parameters_1.SetMaxSize( 1 )
NETGEN_3D_Parameters_1.SetOptimize( 1 )
NETGEN_3D_Parameters_1.SetFineness( 5 )
NETGEN_3D_Parameters_1.SetGrowthRate( 0.7 )
NETGEN_3D_Parameters_1.SetNbSegPerEdge( 3 )
NETGEN_3D_Parameters_1.SetNbSegPerRadius( 5 )
NETGEN_3D_Parameters_1.SetMinSize( 0.01 )
NETGEN_3D_Parameters_1.SetUseSurfaceCurvature( 0 )
NETGEN_3D_Parameters_1.SetSecondOrder( 106 )
NETGEN_3D_Parameters_1.SetFuseEdges( 80 )
NETGEN_3D_Parameters_1.SetQuadAllowed( 127 )

# Far field surface
NETGEN_2D = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_2D,geom=Auto_group_for_Sub_mesh_Far_Field_Surface)
Sub_mesh_Far_Field_Surface = NETGEN_2D.GetSubMesh()
NETGEN_2D_Parameters_FarField = NETGEN_2D.Parameters()
NETGEN_2D_Parameters_FarField.SetMaxSize( 1 )
NETGEN_2D_Parameters_FarField.SetOptimize( 1 )
NETGEN_2D_Parameters_FarField.SetFineness( 0 )
NETGEN_2D_Parameters_FarField.SetMinSize( 0.9 )
NETGEN_2D_Parameters_FarField.SetUseSurfaceCurvature( 1 )
NETGEN_2D_Parameters_FarField.SetQuadAllowed( 0 )
NETGEN_2D_Parameters_FarField.SetSecondOrder( 106 )
NETGEN_2D_Parameters_FarField.SetFuseEdges( 80 )

# Wing surface
NETGEN_2D_1 = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_2D,geom=Auto_group_for_Sub_mesh_Wing_Surface)
Sub_mesh_Wing_Surface = NETGEN_2D_1.GetSubMesh()
NETGEN_2D_Parameters_Wing = NETGEN_2D_1.Parameters()
NETGEN_2D_Parameters_Wing.SetMaxSize( 0.05 )
NETGEN_2D_Parameters_Wing.SetOptimize( 1 )
NETGEN_2D_Parameters_Wing.SetFineness( 5 )
NETGEN_2D_Parameters_Wing.SetGrowthRate( 0.1 )
NETGEN_2D_Parameters_Wing.SetNbSegPerEdge( 6.92154e-310 )
NETGEN_2D_Parameters_Wing.SetNbSegPerRadius( 5.32336e-317 )
NETGEN_2D_Parameters_Wing.SetMinSize( 0.01 )
NETGEN_2D_Parameters_Wing.SetUseSurfaceCurvature( 1 )
NETGEN_2D_Parameters_Wing.SetQuadAllowed( 0 )
NETGEN_2D_Parameters_Wing.SetSecondOrder( 106 )
NETGEN_2D_Parameters_Wing.SetFuseEdges( 80 )

# Far field edges
Regular_1D = Mesh_Domain.Segment(geom=Auto_group_for_Sub_mesh_Far_Field_Edges)
Local_Length_Far_Field = Regular_1D.LocalLength(1,None,1e-07)

# LE Airfoils
Regular_1D_1 = Mesh_Domain.Segment(geom=Auto_group_for_Sub_mesh_LE_Airfoils)
Start_and_End_Length_LE = Regular_1D_1.StartEndLength(0.01,0.05,[])
Start_and_End_Length_LE.SetObjectEntry( 'Cut_Domain' )

# TE Airfoils
Regular_1D_2 = Mesh_Domain.Segment(geom=Auto_group_for_Sub_mesh_TE_Airfoils)
Start_and_End_Length_TE = Regular_1D_2.StartEndLength(0.05,0.01,[])
Start_and_End_Length_TE.SetObjectEntry( 'Cut_Domain' )

# LETE
Regular_1D_3 = Mesh_Domain.Segment(geom=Auto_group_for_Sub_mesh_LETE)
Sub_mesh_LETE = Regular_1D_3.GetSubMesh()
Local_Length_LETE = Regular_1D_3.LocalLength(0.01,None,1e-07)

# Middle
Regular_1D_4 = Mesh_Domain.Segment(geom=Auto_group_for_Sub_mesh_Middle)
Local_Length_Middle = Regular_1D_4.LocalLength(0.05,None,1e-07)

# Compute mesh
isDone = Mesh_Domain.Compute()

NumberOfNodes = Mesh_Domain.NbNodes()
NumberOfElements = Mesh_Domain.NbTetras()
print(' Information about volume mesh:')
print(' Number of nodes       :', NumberOfNodes)
print(' Number of elements    :', NumberOfElements)

# Export data files
try:
  Mesh_Domain.ExportDAT( script_path + '/salome_output/Mesh_Domain.dat' )
  pass
except:
  print 'ExportDAT() failed. Invalid file name?'
try:
  Mesh_Domain.ExportDAT( script_path + '/salome_output/Sub-mesh_Wing.dat', Sub_mesh_Wing_Surface )
  pass
except:
  print 'ExportPartToDAT() failed. Invalid file name?'
try:
  Mesh_Domain.ExportDAT( script_path + '/salome_output/Sub-mesh_FarField.dat', Sub_mesh_Far_Field_Surface )
  pass
except:
  print 'ExportPartToDAT() failed. Invalid file name?'
try:
  Mesh_Domain.ExportDAT( script_path + '/salome_output/Sub-mesh_TE.dat', Sub_mesh_LETE )
  pass
except:
  print 'ExportPartToDAT() failed. Invalid file name?'
Sub_mesh_Far_Field_Edges = Regular_1D.GetSubMesh()
Sub_mesh_LE_Airfoils = Regular_1D_1.GetSubMesh()
Sub_mesh_TE_Airfoils = Regular_1D_2.GetSubMesh()
Sub_mesh_Middle = Regular_1D_4.GetSubMesh()


## Set names of Mesh objects
smesh.SetName(NETGEN_3D.GetAlgorithm(), 'NETGEN 3D')
smesh.SetName(Regular_1D.GetAlgorithm(), 'Regular_1D')
smesh.SetName(NETGEN_2D.GetAlgorithm(), 'NETGEN 2D')
smesh.SetName(NETGEN_2D_Parameters_FarField, 'NETGEN 2D Parameters_FarField')
smesh.SetName(NETGEN_2D_Parameters_Wing, 'NETGEN 2D Parameters_Wing')
smesh.SetName(NETGEN_3D_Parameters_1, 'NETGEN 3D Parameters_1')
smesh.SetName(Start_and_End_Length_TE, 'Start and End Length_TE')
smesh.SetName(Local_Length_LETE, 'Local Length_LETE')
smesh.SetName(Local_Length_Far_Field, 'Local Length_Far_Field')
smesh.SetName(Start_and_End_Length_LE, 'Start and End Length_LE')
smesh.SetName(Local_Length_Middle, 'Local Length_Middle')
smesh.SetName(Mesh_Domain.GetMesh(), 'Mesh_Domain')
smesh.SetName(Sub_mesh_Far_Field_Edges, 'Sub-mesh_Far_Field_Edges')
smesh.SetName(Sub_mesh_Wing_Surface, 'Sub-mesh_Wing_Surface')
smesh.SetName(Sub_mesh_Far_Field_Surface, 'Sub-mesh_Far_Field_Surface')
smesh.SetName(Sub_mesh_Middle, 'Sub-mesh_Middle')
smesh.SetName(Sub_mesh_LETE, 'Sub-mesh_LETE')
smesh.SetName(Sub_mesh_TE_Airfoils, 'Sub-mesh_TE_Airfoils')
smesh.SetName(Sub_mesh_LE_Airfoils, 'Sub-mesh_LE_Airfoils')


if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser(True)
