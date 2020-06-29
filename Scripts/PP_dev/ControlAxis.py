"""
Script for the ElevatorShaft.py
"""

import NemAll_Python_Geometry as AllplanGeo
import GeometryValidate as GeometryValidate
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_Reinforcement as AllplanReinf

from StdReinfShapeBuilder.RotationAngles import RotationAngles
from ModularConstructionSystem.PP_Interpret_Basics import Select_Basics
from PythonPart import View2D3D, PythonPart

import math

print('Load ControlAxis.py')

# Method for checking the supported versions
def check_allplan_version(build_ele, version):
    """
    Check the current Allplan version

    Args:
        build_ele: the building element.
        version:   the current Allplan version

    Returns:
        True/False if version is supported by this script
    """

    return True


def create_element(build_ele, doc):
    """
    Create the element

    Args:
        build_ele:  the building element with the table data.
        doc:        Input document
    """
    element = ControlAxisGeo(build_ele, doc)

    return element.create(build_ele)


def move_handle(build_ele, handle_prop, input_pnt, doc):
    """
    Modify the element geometry by handles

    Args:
        build_ele:  the building element.
        handle_prop handle properties
        input_pnt:  input point
        doc:        input document
    """
    return create_element(build_ele, doc)


class ControlAxisGeo() :
    """
    Implementation of the pi_plates class
    """

    def __init__(self, build_ele, doc):
        """
        Initialisation of class pi_plates_geo

        Args:
            doc: Input document
        """
        self.model_ele_list = []
        self.handle_list    = []
        self.document = doc
        self.build_ele = build_ele

    def create(self, build_ele) : 
        """
        Create the elements

        Args:
            build_ele:  the building element.

        Returns:
            tuple  with created elements and handles.
        """
        #------------------ Create text propery element
        #props = self.create_text_prop (build_ele)


        #------------------ Create some text elements
        self.model_ele_list.append(
            self.create_text(build_ele.Text.value, 0, 0))

        #------------------ Return element- and handle-lists to python
        #framework
        return (self.model_ele_list, self.handle_list)

    def create_python_part(self):
        """
        PythonPart with attributes creation method
        
        Args:
        
        Returns:
            Model elements list
        """

        views = [View2D3D(self.m_model_ele_list)]

        pythonpart = PythonPart(str(self.__class__.__name__),
                                parameter_list=self.build_ele.get_params_list(),
                                hash_value=self.build_ele.get_hash(),
                                python_file=self.build_ele.pyp_file_name,
                                views=views)

        self.m_model_ele_list = pythonpart.create()

        return pythonpart

    def import_parameter_list(self, build_ele):
        """
        import all parameters from the pallete

        Args:
            build_ele:  the building element.
        """
        
        #------------------ assign the geometry parameter        
        #Select_Basics.import_geometry_values(self, build_ele_list)
        

        #------------------ assign the geometry parameter 
        self.axis_length = build_ele.ControlAxisLength.value

        #------------------ assign the style parameter
        self.com_prop = AllplanBaseElements.CommonProperties()
        self.com_prop.GetGlobalProperties()

        #------------------ assign the style parameter
        #Select_Basics.import_design_values(self, build_ele_list) 
        
    def create_geometry(self):
        """
        Create the geometry
        """
        #------------- Left side wall ----------------
        #pnt_1 = AllplanGeo.Point2D(0, self.axis_length/2)
        #pnt_2 = pnt_1 + AllplanGeo.Point2D(0, -self.shaft_length)

        #side_pol = AllplanGeo.Polygon2D()

        #side_pol += pnt_1

        

        #geo_body = back_wall
        #geo_body = front_wall
        #if(self.is_aperture_cb):
           # err, geo_body = AllplanGeo.MakeSubtraction(geo_body, aperture_wall)
        #err, geo_body = AllplanGeo.MakeUnion(geo_body, back_wall)
        #err, geo_body = AllplanGeo.MakeUnion(geo_body, right_side_wall)
        #err, geo_body = AllplanGeo.MakeUnion(geo_body, left_side_wall)
        
        #self.m_model_ele_list = [AllplanBasisElements.ModelElement3D(com_prop, geo_body)]

        return True


    def create_text(self
                    ,text
                    ,xlocation=0.0
                    ,ylocation=0.0
                    ,text_prop=AllplanBasisElements.TextProperties()):
        """
        Create one text element

        Args:
            text:                Text string for text element
            xlocation:           Global X coordinate for text element
            ylocation:           Global Y coordinate for text element
            text_prop:           Text property element
        Return:
            Created text element
        """
        text = '0'

        #------------------ Define common properties, take global Allplan
        com_prop = AllplanBaseElements.CommonProperties()
        com_prop.GetGlobalProperties()

        #------------------ Define Text
        location = AllplanGeo.Point2D(xlocation,ylocation)
        return AllplanBasisElements.TextElement(com_prop, text_prop, text, location)

    
    def create_text_prop(self, build_ele):
        """
        Create one text element

        Args:
            build_ele:  the building element.
        Return:
            Created text property element
        """

        #------------------ Define Text properties
        text_angle = AllplanGeo.Angle()
        text_angle.Deg = 90
        slope_angle = AllplanGeo.Angle()
        slope_angle.Deg = build_ele.ColumnSlopeAngle.value
        font_angle = AllplanGeo.Angle()
        font_angle.Deg = build_ele.FontAngle.value

        text_prop = AllplanBasisElements.TextProperties()
        text_prop.Height = 40
        text_prop.Width = 40
        text_prop.Alignment = self.alignment_type_converter(build_ele.Alignment.value)
        text_prop.TextAngle = text_angle
        text_prop.FontAngle = font_angle
        text_prop.ColumnSlopeAngle = slope_angle
        text_prop.LineFeed = build_ele.LineFeed.value
        text_prop.IsScaleDependent = build_ele.IsScaleDependent.value
        text_prop.HasTextFrame = build_ele.HasTextFrame.value
        if build_ele.HasTextFrame.value:
            text_prop.TextFramePen = build_ele.FramePen.value
            text_prop.TextFrameStroke = build_ele.FrameStroke.value
            text_prop.TextFrameColor = build_ele.FrameColor.value
        text_prop.HasBackgroundColor = build_ele.HasBackgroundColor.value
        if build_ele.HasBackgroundColor.value:
            text_prop.BackgroundColor = build_ele.BackgroundColor.value
        text_prop.Type = AllplanBasisElements.TextType.eNormalText
        text_prop.Font = build_ele.FontId.value
        text_prop.Expansion = 1

        return text_prop


   