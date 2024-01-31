This script will lock the given Viewer buffer to the selected node in Foundry's Nuke to avoid inadvertent changes.

I generally use `1` and `2` while I'm working for the "things I'm looking at", and the other buffers for e.g. the plate, the final comp, the previous render, a reference image/master shot, etc. With Nuke's default behaviour, it is _very_ easy to inadvertently change buffer. E.g. I have `3` set to the plate, and I want to check the plate against the thing I'm working on, but whoops, a node was selected, now `3` is pointing at that random node, and I have to jump to the plate, reset buffer `3`, and then jump back to where I was. Infuriating.

# Basic Usage

With a node selected, use `Alt-<1-0>` to lock that Viewer buffer to the selected node.

Use `Shift-Alt-<1-0> to unlock that Viewer buffer. 

If the Viewer buffer is locked, pressing the related number will always recall the locked node to the Viewer, even if another node is selected when you push the button.

# Suggested Usage

My personal usage:

1. The thing I'm working on - never locked.
2. Something else I'm working on/comparing with - never locked.
3. Locked to the plate.
4. Locked to the final output of the comp.
5. Locked to the previous render/publish of the comp.
6. Locked to a reference image, master shot, or lighting slap.
7. 7+ - Locked to other reference images, master shots, etc.

This lets me quickly move around the comp, using the handiest buffers (`1` and `2`) the most often, and keeps the plate and previous version second-closest. As I work, I'm constantly doing stuff like `1-2-1-2` as I compare before and after the node I'm working on to see its local effects, then `3-4-3-4` to compare the plate and the final comp, and then `4-5-4-5` to compare my current comp to the previous comp to ensure I haven't "wandered off" too far from where we were before (which is liable to provoke new and unwanted notes!).

# Installation

Put `viewer_lock.py` and `menu.py` in a folder called `viewer_lock` in your `~/.nuke` folder.

Add this line to your `init.py`:

```
nuke.pluginAddPath(viewer_lock)
```
