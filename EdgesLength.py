bl_info = \
    {
        "name" : "Edges length",
        "author" : "Pawel Mogila",
        "version" : (1, 0, 0),
        "blender" : (2, 7, 9),
        "location" : "View 3D > Edit Mode > Tool Shelf",
        "description" :
        "Calculate sum of all selected edges",
        "warning" : "",
        "wiki_url" : "",
        "tracker_url" : "",
        "category" : "Add Mesh",
    }


import math
import bpy
import mathutils

class EdgesLengthPanel(bpy.types.Panel) :
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "mesh_edit"
    bl_category = "Tools"
    bl_label = "Edges lengths"

    def draw(self, context) :
        TheCol = self.layout.column(align = True)
        TheCol.operator("mesh.edges_length", text = "Calculate edges length")
        TheCol.prop(context.scene, "sum_edges_length")
 
class CalculateEdgesLength(bpy.types.Operator) :

    bl_idname = "mesh.edges_length"
    bl_label = "Calculate edges length"
    bl_options = {"UNDO"}

    def invoke(self, context, event) :
        bpy.ops.object.mode_set(mode="OBJECT")
        object_data = bpy.context.active_object.data
        selected_edges = [edge for edge in object_data.edges if edge.select]
       
        edge_length = 0.0
        for edge in selected_edges:
            vert1 = edge.vertices[0]
            vert2 = edge.vertices[1]
            co1 = object_data.vertices[vert1].co  
            co2 = object_data.vertices[vert2].co  
            edge_length += (co1-co2).length
             
        
        
        context.scene.sum_edges_length=edge_length
        print("combined length: ", edge_length)
        bpy.ops.object.mode_set(mode="EDIT")

        return {"FINISHED"}
    #end invoke

def get_total_edges_length(self):
    return self['total_edges_length']
	
def register() :
    bpy.utils.register_class(CalculateEdgesLength)
    bpy.utils.register_class(EdgesLengthPanel)

    bpy.types.Scene.sum_edges_length = bpy.props.FloatProperty \
      (
        name = "Sum length",
        default = 0.0,
        precision=3
      )


def unregister() :
    bpy.utils.unregister_class(CalculateEdgesLength)
    bpy.utils.unregister_class(EdgesLengthPanel)
    del bpy.types.Scene.sum_edges_length
#end unregister

if __name__ == "__main__" :
    register()
#end if