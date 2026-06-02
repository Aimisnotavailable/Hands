import json
import sys
from pathlib import Path
#TODO attach the hand landmarks to the skeleton rigs
# Use phantom hand tracker by git installing it
# Add interpolation and smoothing
# LOL need to abandon this project for a while to grind leetcode that was the worst interview ever

def remove_animations(gltf_path, output_path=None):
    """
    Removes the 'animations' key from a glTF JSON file.
    If output_path is None, overwrites the original.
    """
    path = Path(gltf_path)
    data = json.loads(path.read_text(encoding="utf-8"))

    if "animations" in data:
        del data["animations"]
        print(f"Removed animations from {path.name}")
    else:
        print("No animations found — nothing to remove.")

    out = Path(output_path or gltf_path)
    out.write_text(json.dumps(data, indent=2), encoding="utf-8")
    if out != path:
        print(f"Saved cleaned file to {out}")
    else:
        print(f"Overwritten original {out}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python clean_gltf.py model.gltf [output.gltf]")
        sys.exit(1)
    src = sys.argv[1]
    dst = sys.argv[2] if len(sys.argv) > 2 else None
    remove_animations(src, dst)