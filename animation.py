#
#   Script to generate animation based on the iteration frames
#   Source: https://stackoverflow.com/a/57751793
#
import glob
import contextlib
from PIL import Image


# Parameters
fp_in = "images/iter_*.png" # Input files
fp_out = "animation.gif"    # Output file (animation)


with contextlib.ExitStack() as stack:
    # Lazily load images
    imgs = (stack.enter_context(Image.open(f))
            for f in sorted(glob.glob(fp_in)))

    # Extract first image from iterator
    img = next(imgs)

    # https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif
    img.save(fp=fp_out, format='GIF', append_images=imgs,
             save_all=True, duration=600)