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
sys.path.insert( 0, r'/home/inigo/simulations/wing/01_only_wing_for_embedded')

###
### GEOM component
###

import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS


geompy = geomBuilder.New(theStudy)

O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)
Curve_UpperSurface_LE = geompy.MakeCurveParametric("t - 0.5", "0.0", "0.6*(0.2969*sqrt(t) - 0.1260*t - 0.3516*t**2 + 0.2843*t**3 - 0.1036*t**4)", 0, 0.5, 999, GEOM.Interpolation, True)
Curve_UpperSurface_TE = geompy.MakeCurveParametric("t - 0.5", "0.0", "0.6*(0.2969*sqrt(t) - 0.1260*t - 0.3516*t**2 + 0.2843*t**3 - 0.1036*t**4)", 0.5, 1, 999, GEOM.Interpolation, True)
Curve_LowerSurface_TE = geompy.MakeCurveParametric("t - 0.5", "0.0", "-0.6*(0.2969*sqrt(t) - 0.1260*t - 0.3516*t**2 + 0.2843*t**3 - 0.1036*t**4)", 0.5, 1, 999, GEOM.Interpolation, True)
Curve_LowerSurface_LE = geompy.MakeCurveParametric("t - 0.5", "0.0", "-0.6*(0.2969*sqrt(t) - 0.1260*t - 0.3516*t**2 + 0.2843*t**3 - 0.1036*t**4)", 0, 0.5, 999, GEOM.Interpolation, True)
Wire_Airfoil = geompy.MakeWire([Curve_UpperSurface_LE, Curve_UpperSurface_TE, Curve_LowerSurface_TE, Curve_LowerSurface_LE], 1e-07)
geompy.Rotate(Wire_Airfoil, OY, 5*math.pi/180.0)
Extrusion_1 = geompy.MakePrismVecH(Wire_Airfoil, OY, 4)
Translation_Airfoil = geompy.MakeTranslationVectorDistance(Wire_Airfoil, OY, 4)
Face_Airfoil_Left = geompy.MakeFaceWires([Wire_Airfoil], 1)
Face_Airfoil_Right = geompy.MakeFaceWires([Translation_Airfoil], 1)
Fuse_Wing = geompy.MakeFuseList([Extrusion_1, Face_Airfoil_Left, Face_Airfoil_Right], True, True)
[Edge_LE,Edge_Left_LowerLE,Edge_Left_UpperLE,Edge_Right_LowerLE,Edge_Right_UpperLE,Edge_Middle_Lower,Edge_Middle_Upper,Edge_Left_LowerTE,Edge_Left_UpperTE,Edge_Right_LowerTE,Edge_Right_UpperTE,Edge_TE] = geompy.ExtractShapes(Fuse_Wing, geompy.ShapeType["EDGE"], True)
Auto_group_for_Sub_mesh_AirfoilLE = geompy.CreateGroup(Fuse_Wing, geompy.ShapeType["EDGE"])
geompy.UnionList(Auto_group_for_Sub_mesh_AirfoilLE, [Edge_Left_LowerLE, Edge_Left_UpperLE, Edge_Right_LowerLE, Edge_Right_UpperLE])
Auto_group_for_Sub_mesh_AirfoilTE = geompy.CreateGroup(Fuse_Wing, geompy.ShapeType["EDGE"])
geompy.UnionList(Auto_group_for_Sub_mesh_AirfoilTE, [Edge_Left_LowerTE, Edge_Left_UpperTE, Edge_Right_LowerTE, Edge_Right_UpperTE])
Auto_group_for_Sub_mesh_LETE = geompy.CreateGroup(Fuse_Wing, geompy.ShapeType["EDGE"])
geompy.UnionList(Auto_group_for_Sub_mesh_LETE, [Edge_LE, Edge_TE])
Auto_group_for_Sub_mesh_Middle = geompy.CreateGroup(Fuse_Wing, geompy.ShapeType["EDGE"])
geompy.UnionList(Auto_group_for_Sub_mesh_Middle, [Edge_Middle_Lower, Edge_Middle_Upper])
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

smesh = smeshBuilder.New(theStudy)
Mesh_1 = smesh.Mesh(Fuse_Wing)
NETGEN_2D = Mesh_1.Triangle(algo=smeshBuilder.NETGEN_2D)
NETGEN_2D_Parameters_1 = NETGEN_2D.Parameters()
NETGEN_2D_Parameters_1.SetMaxSize( 0.05 )
NETGEN_2D_Parameters_1.SetOptimize( 1 )
NETGEN_2D_Parameters_1.SetFineness( 2 )
NETGEN_2D_Parameters_1.SetMinSize( 0.01 )
NETGEN_2D_Parameters_1.SetUseSurfaceCurvature( 1 )
NETGEN_2D_Parameters_1.SetQuadAllowed( 0 )
NETGEN_2D_Parameters_1.SetSecondOrder( 143 )
NETGEN_2D_Parameters_1.SetFuseEdges( 128 )
Regular_1D = Mesh_1.Segment(geom=Auto_group_for_Sub_mesh_AirfoilLE)
Start_and_End_Length_LE = Regular_1D.StartEndLength(0.01,0.05,[])
Start_and_End_Length_LE.SetObjectEntry( 'Fuse_Wing' )
Regular_1D_1 = Mesh_1.Segment(geom=Auto_group_for_Sub_mesh_AirfoilTE)
Start_and_End_Length_TE = Regular_1D_1.StartEndLength(0.05,0.01,[])
Start_and_End_Length_TE.SetObjectEntry( 'Fuse_Wing' )
Regular_1D_2 = Mesh_1.Segment(geom=Auto_group_for_Sub_mesh_LETE)
Local_Length_LETE = Regular_1D_2.LocalLength(0.01,None,1e-07)
Regular_1D_3 = Mesh_1.Segment(geom=Auto_group_for_Sub_mesh_Middle)
Local_Length_Middle = Regular_1D_3.LocalLength(0.05,None,1e-07)
isDone = Mesh_1.Compute()
Sub_mesh_AirfoilLE = Regular_1D.GetSubMesh()
Sub_mesh_AirfoilTE = Regular_1D_1.GetSubMesh()
Sub_mesh_LETE = Regular_1D_2.GetSubMesh()
Sub_mesh_Middle = Regular_1D_3.GetSubMesh()


## Set names of Mesh objects
smesh.SetName(NETGEN_2D.GetAlgorithm(), 'NETGEN 2D')
smesh.SetName(Regular_1D.GetAlgorithm(), 'Regular_1D')
smesh.SetName(Start_and_End_Length_LE, 'Start and End Length_LE')
smesh.SetName(NETGEN_2D_Parameters_1, 'NETGEN 2D Parameters_1')
smesh.SetName(Local_Length_Middle, 'Local Length_Middle')
smesh.SetName(Start_and_End_Length_TE, 'Start and End Length_TE')
smesh.SetName(Local_Length_LETE, 'Local Length_LETE')
smesh.SetName(Mesh_1.GetMesh(), 'Mesh_1')
smesh.SetName(Sub_mesh_LETE, 'Sub-mesh_LETE')
smesh.SetName(Sub_mesh_AirfoilTE, 'Sub-mesh_AirfoilTE')
smesh.SetName(Sub_mesh_AirfoilLE, 'Sub-mesh_AirfoilLE')
smesh.SetName(Sub_mesh_Middle, 'Sub-mesh_Middle')


if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser(True)
