import git
import FreeCAD
import os
if FreeCAD.GuiUp:
    import FreeCADGui

def commitchanges():
    """
    Commit the changes of the current active file
    """
    f = FreeCAD.ActiveDocument.FileName
    if len(f) == 0:
        # Not saved yet...
        return

    try:
        repo = git.Repo(os.path.dirname(f), search_parent_directories=True)
    except git.InvalidGitRepositoryError:
        FreeCAD.Console.PrintMessage(u"{} is not a git repo. do nothing.\n".format(os.path.dirname(f)))
        return
    except git.NoSuchPathError:
        FreeCAD.Console.PrintError(u"Ooops! The folder does not exist.\n")
        return

    # Add and commit the file
    index = repo.index
    index.add([f])
    index.commit("[FreeCAD autocommit]")


def initrepo():
    """
    Initialize a repo at the current file location
    """
    f = FreeCAD.ActiveDocument.FileName
    if len(f) == 0:
        # Not saved yet...
        return

    repo_dir = os.path.dirname(f)

    # TODO show dialogs, not just console output
    try:
        # TODO do we need this check? It seems like it doesnt matter if we init
        # again... Repo still there, no harm taken.
        repo = git.Repo(repo_dir, search_parent_directories=True)
        FreeCAD.Console.PrintMessage(u"{} is already a git repo. do nothing.\n".format(repo_dir))
        return
    except git.InvalidGitRepositoryError:
        pass

    repo = git.Repo.init(repo_dir)
    FreeCAD.Console.PrintMessage(u"Initialized a git repo at: {}".format(repo_dir))
    # A commit should work now
    commitchanges()


class CommandCommit:
    """
    Command to commit the current file
    """

    def GetResources(self):
        return {'Pixmap': os.path.join(os.path.dirname(__file__),"icons",'git-commit.svg'),
                'MenuText': "Commit",
                'ToolTip': 'Commit the current file in git',
                }

    def Activated(self):
        commitchanges()


class CommandTag:
    """
    Command to create a new tag
    """

    def GetResources(self):
        return {'Pixmap': os.path.join(os.path.dirname(__file__),"icons",'tag.svg'),
                'MenuText': "Tag",
                'ToolTip': 'Tag the current commit',
                }

    def Activated(self):
        # TODO show some dialog, enter a tag name, save
        pass


class CommandCreate:
    """
    Init a new git repo in the current folder
    """

    def GetResources(self):
        return {'Pixmap': os.path.join(os.path.dirname(__file__),"icons",'git.svg'),
                'MenuText': "Init",
                'ToolTip': 'Initialize a new git repository',
                }

    def Activated(self):
        initrepo()


if FreeCAD.GuiUp:
    FreeCADGui.addCommand('GitProject_CommandCommit',CommandCommit())
    FreeCADGui.addCommand('GitProject_CommandTag',CommandTag())
    FreeCADGui.addCommand('GitProject_CommandCreate',CommandCreate())
