import os

import numpy as np
import rasterio

from PIL import Image, ImageFilter

from rasterio.windows import Window
from rasterio.warp import transform


def create_rgb_image(item, latitude, longitude, year):

    red_url = item.assets["red"].href
    green_url = item.assets["green"].href
    blue_url = item.assets["blue"].href

    # -----------------------------------
    # Find pixel position
    # -----------------------------------

    with rasterio.open(red_url) as src:

        x, y = transform(
            "EPSG:4326",
            src.crs,
            [longitude],
            [latitude]
        )

        row, col = src.index(
            x[0],
            y[0]
        )

        # -----------------------------------
        # Crop 500 x 500 pixels
        # -----------------------------------

        crop_size = 500
        half = crop_size // 2

        window = Window(
            col - half,
            row - half,
            crop_size,
            crop_size
        )

        red = src.read(
            1,
            window=window
        )

    # -----------------------------------
    # Read Green band
    # -----------------------------------

    with rasterio.open(green_url) as src:

        green = src.read(
            1,
            window=window
        )

    # -----------------------------------
    # Read Blue band
    # -----------------------------------

    with rasterio.open(blue_url) as src:

        blue = src.read(
            1,
            window=window
        )

    # -----------------------------------
    # Create RGB image
    # -----------------------------------

    rgb = np.dstack(
        (
            red,
            green,
            blue
        )
    ).astype(np.float32)

    # -----------------------------------
    # Percentile normalization
    # -----------------------------------

    low = np.percentile(
        rgb,
        2
    )

    high = np.percentile(
        rgb,
        98
    )

    rgb = (
        (rgb - low)
        / (high - low)
    )

    rgb = np.clip(
        rgb,
        0,
        1
    )

    # -----------------------------------
    # Gamma enhancement
    # -----------------------------------

    rgb = np.power(
        rgb,
        0.7
    )

    rgb = (
        rgb * 255
    ).astype(
        np.uint8
    )

    # -----------------------------------
    # Convert to PIL image
    # -----------------------------------

    image = Image.fromarray(
        rgb
    )

    # -----------------------------------
    # 2x display upscale
    # -----------------------------------

    image = image.resize(
        (
            image.width * 2,
            image.height * 2
        ),
        Image.Resampling.LANCZOS
    )

    # -----------------------------------
    # Sharpen
    # -----------------------------------

    image = image.filter(
        ImageFilter.UnsharpMask(
            radius=1.2,
            percent=120,
            threshold=3
        )
    )

    # -----------------------------------
    # Output path
    # -----------------------------------

    base_dir = os.path.dirname(
        os.path.abspath(__file__)
    )

    output_dir = os.path.join(
        base_dir,
        "static",
        "outputs"
    )

    os.makedirs(
        output_dir,
        exist_ok=True
    )

    output_file = os.path.join(
        output_dir,
        f"sentinel_{year}.png"
    )

    image.save(
        output_file
    )

    return {
        "image": f"/static/outputs/sentinel_{year}.png"
    }