import bpy
import matplotlib

class EXAMPLE_OT_dummy_operator(bpy.types.Operator):
    bl_idname = "example.dummy_operator"
    bl_label = "Dummy Operator"
    bl_description = "This operator tries to use matplotlib."
    bl_options = {"REGISTER"}

    def execute(self, context):
        print(matplotlib.__version__)
        print(matplotlib.get_cachedir())
        return {"FINISHED"}


class EXAMPLE_PT_panel(bpy.types.Panel):
    bl_label = "Example Panel"
    bl_category = "Example Tab"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        layout.label(text=f"matplotlib {matplotlib.__version__}")
        layout.operator(EXAMPLE_OT_dummy_operator.bl_idname)


classes = (EXAMPLE_OT_dummy_operator,
           EXAMPLE_PT_panel)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
