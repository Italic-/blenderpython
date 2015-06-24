from .align_tools import VIEW3D_MT_align_tools

if "bpy" in locals():
    import importlib
    importlib.reload(analyse_dicom_3d_models)
    importlib.reload(display_tools)
    importlib.reload(select_vis_tools)
    importlib.reload(quick_prefs)

else:
    from . import analyse_dicom_3d_models
    from . import display_tools
    from . import quick_prefs


import bpy

