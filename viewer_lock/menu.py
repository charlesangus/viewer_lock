import nuke
import nukescripts
import viewer_lock


# patch builtin method
connect_selected_to_viewer_OLD = nukescripts.connect_selected_to_viewer
nukescripts.connect_selected_to_viewer = viewer_lock.connect_selected_to_viewer


def setup_menus():
    menu = nuke.menu("Nuke")
    viewer_menu = nuke.menu("Viewer")
    lock_menu = menu.addMenu("Viewer/Lock Input", index=4)
    unlock_menu = menu.addMenu("Viewer/Unlock Input", index=5)
    for i in range(10):
        # display version of the index
        j = i + 1
        menu.addCommand(
            f"Viewer/Connect to A Side/Using Input {j}",
            f"viewer_lock.connect_selected_to_viewer({i})",
            f"{j % 10}",
            shortcutContext=2
        )
        menu.addCommand(
            f"Viewer/Connect to B Side/Using Input {j}",
            f"viewer_lock.connect_selected_to_viewer({i + 10})",
            f"shift+{j % 10}",
            shortcutContext=2
        )
        # for some reason the shortcuts don't appear if using the
        # more conventional "Alt-1" or "Shift-Alt-1", it only works
        # if you use the "+#1" syntax.
        menu.addCommand(
            f"Viewer/Lock Input/Lock Input {j}",
            f"viewer_lock.lock_connection({i})",
            f"#{j % 10}",
            shortcutContext=2
        )
        menu.addCommand(
            f"Viewer/Unlock Input/Unlock Input {j}",
            f"viewer_lock.unlock_connection({i})",
            f"+#{j % 10}",
            shortcutContext=2
        )


setup_menus()
