import clr
clr.AddReference('System.Core')
clr.AddReference('RhinoInside.Revit')
clr.AddReference('RevitAPI') 
clr.AddReference('RevitAPIUI')

from System import Enum

import rhinoscriptsyntax as rs
import Rhino
import RhinoInside
import Grasshopper
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML
from RhinoInside.Revit import Revit, Convert
# add extensions methods as well
# this allows calling .ToXXX() convertor methods on Revit objects
clr.ImportExtensions(Convert.Geometry)
from Autodesk.Revit import DB

# active Revit verison
REVIT_VERSION = Revit.ActiveUIApplication.Application.VersionNumber

# access the active document object
doc = Revit.ActiveDBDocument

def show_warning(msg):
    ghenv.Component.AddRuntimeMessage(RML.Warning, msg)

def show_error(msg):
    ghenv.Component.AddRuntimeMessage(RML.Error, msg)

def show_remark(msg):
    ghenv.Component.AddRuntimeMessage(RML.Remark, msg)

SFU = DB.Structure.StructuralFramingUtils

t = DB.Transaction(doc, 'Update End Joins')
t.Start()
try:
    if isinstance(E, DB.FamilyInstance):
        # if structural beam
        if True:
            for state, endidx in zip([JS, JE], [0, 1]):
                print(state, endidx)
                if state:
                    SFU.AllowJoinAtEnd(E, endidx)
                else:
                    SFU.DisallowJoinAtEnd(E, endidx)
    t.Commit()
except Exception as txn_err:
    show_error(str(txn_err))
    t.RollBack()