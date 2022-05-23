import bpy
import random
from bpy.props import *

def main(size):
    
    if "material_red" not in bpy.data.materials:
        # create new material
        red_mat = bpy.data.materials.new(name = "material_red")

        # using nodes for connecting emission shader
        red_mat.use_nodes = True
        nodes = red_mat.node_tree.nodes

        material_output = nodes.get("Material Output")

        # creating and setting values of emission shader
        node_emission = nodes.new(type = "ShaderNodeEmission")
        node_emission.inputs[0].default_value = (0.7, 0.1, 0.2, 1)
        node_emission.inputs[1].default_value = 5

        # connecting emission shader to the material
        links = red_mat.node_tree.links
        red_mat_link = links.new(node_emission.outputs[0], material_output.inputs[0])

    if "material_steel" not in bpy.data.materials:
        # creating material and setting its properties
        steel_mat = bpy.data.materials.new(name = "material_steel")
        steel_mat.metallic = 1.0
        steel_mat.roughness = 0.0
    
    spacing = 2.2

    for x in range(size):
        for y in range(size):
            # calculate location
            location = (x*spacing, y*spacing, random.random()*3)
            
            # add cube
            bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=location, scale=(1, 1, 1))
            
            # select the cube
            item = bpy.context.object
            
            # choose a material for the cube
            if random.random() > 0.02:
                item.data.materials.append(bpy.data.materials["material_steel"])
            else:
                item.data.materials.append(bpy.data.materials["material_red"])


class SimpleOperator(bpy.types.Operator):
    bl_idname = "object.simple_operator"
    bl_label = "Simple Object Operator"
    bl_options = {'REGISTER', 'UNDO'}
    
    square_size: IntProperty(
        name = "Square Size",
        description = "Size of the square grid.",
        default = 2,
        min = 1,
        max = 10
    )

    def execute(self, context):
        main(self.square_size)
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(SimpleOperator.bl_idname, text=SimpleOperator.bl_label)

# Register and add to the "object" menu (required to also use F3 search "Simple Object Operator" for quick access)
def register():
    bpy.utils.register_class(SimpleOperator)
    bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
    bpy.utils.unregister_class(SimpleOperator)
    bpy.types.VIEW3D_MT_object.remove(menu_func)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.simple_operator()