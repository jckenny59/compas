# type: ignore
import os
import compas

try:
    import bpy
except ImportError:
    pass
else:
    from .utilities import *  # noqa: F401 F403


def clear(guids=None):
    """Clear all scene objects."""
    if guids is None:
        # delete all objects
        bpy.ops.object.select_all(action="SELECT")
        bpy.ops.object.delete(use_global=True, confirm=False)
        # delete data
        delete_unused_data()  # noqa: F405
        # delete collections
        for collection in bpy.context.scene.collection.children:
            bpy.context.scene.collection.children.unlink(collection)
        for block in bpy.data.collections:
            objects = [o for o in block.objects if o.users]
            while objects:
                bpy.data.objects.remove(objects.pop())
            for collection in block.children:
                block.children.unlink(collection)
            if block.users == 0:
                bpy.data.collections.remove(block)
    else:
        for obj in guids:
            bpy.data.objects.remove(obj, do_unlink=True)


def redraw():
    """Trigger a redraw."""
    bpy.ops.wm.redraw_timer(type="DRAW_WIN_SWAP", iterations=1)


__version__ = "2.0.0-alpha.2"


def _check_blender_version(version):
    supported_versions = ["2.83", "2.93", "3.1"]

    if not version:
        return "2.93"

    if version not in supported_versions:
        raise Exception("Unsupported Blender version: {}".format(version))

    return version


def _get_default_blender_installation_path(version):
    version = _check_blender_version(version)

    if compas.OSX:
        path = _get_default_blender_installation_path_mac(version)
    elif compas.WINDOWS:
        path = _get_default_blender_installation_path_windows(version)
    else:
        raise Exception("Unsupported platform.")

    if not os.path.exists(path):
        raise Exception("The default installation folder for Blender {} doesn't exist.".format(version))

    return path


def _get_default_blender_installation_path_mac(version):
    return "/Applications/Blender.app/Contents/Resources/{}".format(version)


def _get_default_blender_installation_path_windows(version):
    return os.path.expandvars("%PROGRAMFILES%/Blender Foundation/Blender {}/{}".format(version, version))


__all__ = [name for name in dir() if not name.startswith("_")]

__all_plugins__ = [
    "compas_blender.geometry.booleans",
    "compas_blender.scene",
]
