import nuke
import nukescripts


def get_active_viewer_node():
    viewer_window = nuke.activeViewer()
    if viewer_window is None:
        old_selection = nuke.selectedNodes()
        viewer = nuke.createNode("Viewer")
        nukescripts.clear_selection_recursive()
        for node in old_selection:
            node["selected"].setValue(True)
    else:
        viewer = viewer_window.node()
    return viewer


def get_selection():
    selection = None
    try:
        selection = nuke.selectedNode()
    except ValueError:    # no node selected
        pass

    if selection is not None and selection.Class() == 'Viewer':
        selection = None

    return selection


def get_or_create_lock_tab():
    viewer = get_active_viewer_node()
    if "lock_tab" in viewer.knobs():
        return viewer["lock_tab"]
    else:
        lock_tab = nuke.Tab_Knob("lock_tab")
        lock_tab.setVisible(False)
        lock_tab.setFlag(nuke.INVISIBLE)
        viewer.addKnob(lock_tab)

def get_lock_knob_name(inputIndex):
    lock_knob_name = f"lock_input_{inputIndex}"
    return lock_knob_name


def get_or_create_lock_knob(inputIndex):
    viewer = get_active_viewer_node()
    lock_knob = get_lock_knob(inputIndex)
    if not lock_knob:
        lock_knob_name = get_lock_knob_name(inputIndex)
        lock_knob = nuke.String_Knob(lock_knob_name)
        lock_knob.setVisible(False)
        viewer.addKnob(lock_knob)
    return lock_knob


def get_lock_knob(inputIndex):
    viewer = get_active_viewer_node()
    lock_knob_name = get_lock_knob_name(inputIndex)
    if lock_knob_name in viewer.knobs():
        lock_knob = viewer[lock_knob_name]
        return lock_knob
    else:
        return None


def get_all_lock_knobs(viewer):
    lock_knobs = [
        viewer[knob_name]
        for knob_name in viewer.knobs()
        if knob_name.startswith("lock_input_")
    ]
    return lock_knobs


def update_colour_and_label(viewer):
    old_label = viewer["label"].getText()
    old_label_lines = [line for line in old_label.split("\n") if not line.startswith("Locked input")]
    new_label_lines = []
    remove_colour = True
    for knob in get_all_lock_knobs(viewer):
        if knob.getText() != "":
            remove_colour = False
            inputIndex = int(knob.name().replace("lock_input_", ""))
            lock_line = f"Locked input {inputIndex + 1} to {knob.getText()}"
            new_label_lines.append(lock_line)
    viewer["label"].setValue("\n".join(old_label_lines + new_label_lines))
    if remove_colour:
        viewer["tile_color"].setValue(nuke.defaultNodeColor('Viewer'))
    else:
        viewer["tile_color"].setValue(286331391)


def lock_connection(inputIndex):
    viewer = get_active_viewer_node()
    selection = get_selection()
    if not selection:
        return
    lock_tab = get_or_create_lock_tab()
    lock_knob = get_or_create_lock_knob(inputIndex)
    lock_knob.setValue(selection.fullName())
    connect_selected_to_viewer(inputIndex)
    update_colour_and_label(viewer)


def unlock_connection(inputIndex):
    viewer = get_active_viewer_node()
    lock_knob = get_lock_knob(inputIndex)
    if lock_knob:
        lock_knob.setText("")
    update_colour_and_label(viewer)


def connect_selected_to_viewer(inputIndex):
    """Patch for built-in nukescripts method.
Connects the selected node to the given viewer input index, ignoring errors if no node is selected."""
    viewer = get_active_viewer_node()
    selection = get_selection()
    lock_knob = get_lock_knob(inputIndex)
    if lock_knob:
        node_name = lock_knob.getText()
        node = nuke.toNode(node_name)
        if not node:
            unlock_connection(inputIndex)
        if node and node.Class() != 'Viewer':
            selection = node

    nuke.connectViewer(inputIndex, selection)
