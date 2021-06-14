"""Provides a scripting component.
    Inputs:
        x: The x script variable
        y: The y script variable
    Output:
        a: The a output variable"""

__author__ = "ykish"
__version__ = "2021.06.13"


# Common-Language-Runtime module provided by IronPython
import clr

clr.AddReference('RhinoCommon')

# add reference to base system types e.g. Enum
clr.AddReference('System.Core')

# add reference to API provided by Rhino.Inside.Revit
clr.AddReference('RhinoInside.Revit')

# add reference to Revit API (two DLLs)
clr.AddReference('RevitAPI') 
clr.AddReference('RevitAPIUI')
# from System.Core DLL
from System import Enum, Action

# Rhino.Inside.Revit API
import RhinoInside
from RhinoInside.Revit import Revit, Convert

import rhinoscriptsyntax as rs
import Grasshopper
import Rhino
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML

# add extensions methods as well
# this allows calling .ToXXX() convertor methods on Revit objects
clr.ImportExtensions(Convert.Geometry)

# Revit API
#from Autodesk.Revit import DB
from Autodesk.Revit import UI
from Autodesk.Revit.DB import Transaction, Element, ElementId, BuiltInCategory, DirectShape, FilteredElementCollector,FamilySymbol,FamilyInstance,Structure,Line,BuiltInParameter

#Linq
import System
clr.ImportExtensions(System.Linq)

def show_warning(msg):
    ghenv.Component.AddRuntimeMessage(RML.Warning, msg)

def show_error(msg):
    ghenv.Component.AddRuntimeMessage(RML.Error, msg)

def show_remark(msg):
    ghenv.Component.AddRuntimeMessage(RML.Remark, msg)


def create_brace(doc, lines):
    braces = []
    ids = []
    level = doc.ActiveView.GenLevel
    fsymbol = doc.GetElement(ElementId(T))
    if fsymbol.IsActive is False:
        fsymbol.Activate()
    if Bake == False:
        i = 0
        for line in lines:
            brace = doc.Create.NewFamilyInstance(Line.GetEndPoint(line,0), fsymbol, level, Structure.StructuralType.Brace)
            braceCurve1 = brace.Location
            braceCurve1.Curve = line

        
            elem_param = brace.get_Parameter(BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS)
            elem_param.Set(ApplicationId)
            
            elem_param = brace.get_Parameter(BuiltInParameter.ALL_MODEL_MARK)
            elem_param.Set(I[i])

            braces.append(brace)
            ids.append(brace.Id)
            i = i+1
    return braces, ids

def get_symbol(doc):
    symbols = []
    
    allcollector = DB.FilteredElementCollector(doc).OfClass(DB.FamilySymbol)
    allelementlist = allcollector.ToElementIds()
    symbols = allcollector.ToElements()

    for i in symbols:
        if DB.Element.Name.GetValue(i) == T:
            fsymbol = i

def convert_lines():
    lines = []
    for line in L:
        l = RhinoInside.Revit.Convert.Geometry.GeometryEncoder.ToLine(line)
        lines.append(l)
    return lines

doc = Revit.ActiveDBDocument
ApplicationId = ghenv.Component.ComponentGuid.ToString()
ApplicationDataId = ghenv.Component.InstanceGuid.ToString()

lines = convert_lines()
ids = []

# Delete previous run results
if ghenv.Component.RunCount == 1:
    
    with Transaction(doc, ghenv.Component.NickName) as trans:
        trans.Start()
        
        with FilteredElementCollector(doc).OfClass(FamilyInstance).WhereElementIsNotElementType() as collector:
            #E = collector.ToElements()
            doc.Delete(collector.ToElements().Where(lambda x: x.get_Parameter(BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS).AsString() == ApplicationId).Select(lambda x: x.Id).ToList[ElementId]())
            
            els = collector.ToElements()
            vals = []
            for e in els:
                
                vals.append( e.GetParameters('コメント')[0].AsString())
                vals.append( e.Symbol.Family.Name)
                vals.append( e.Name)
            E = vals
            
        trans.Commit()


if L is not None:
    with Transaction(doc, ghenv.Component.NickName) as trans:
        trans.Start()

        braces, ids = create_brace(doc,lines)

        trans.Commit()
        
        

E = braces
Id = ids
