from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


class SceneObjectNotRegisteredError(Exception):
    """Exception that is raised when no scene object is registered for a given data type."""


class NoSceneObjectContextError(Exception):
    """Exception that is raised when no scene object context is assigned is registered for a given data type."""

    def __init__(self):
        error_message = "No context defined."
        error_message += "\n\nThis usually means that the script that you are running requires"
        error_message += "\na CAD environment but it is being ran as a standalone script"
        error_message += "\n(ie. from the command line or code editor)."
        super(NoSceneObjectContextError, self).__init__(error_message)
