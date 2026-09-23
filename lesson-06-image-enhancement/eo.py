from pystac_client import Client
import rasterio
from rasterio.warp import transform
from rasterio.windows import Window
import numpy as np
from PIL import Image, ImageFilter
import os


def find_satellite_image(latitude, longitude):

    catalog = Client.open(
        "https://earth-search.aws.element84.com/v1"
    )

    search = catalog.search(
        collections=["sentinel-2-l2a"],
        intersects={
            "type": "Point",
            "coordinates": [
                longitude,
                latitude
            ]
        },
        datetime="2026-01-01/2026-12-31",
        query={
            "eo:cloud_cover": {
                "lt": 20
            }
        },
        max_items=1
    )

    items = list(search.items())

    if not items:
        raise Exception(
            "No suitable Sentinel-2 image found."
        )

    return items[0]


def create_rgb_image(latitude, longitude):

    item = find_satellite_image(
        latitude,
        longitude
    )

    red_url = item.assets["red"].href
    green_url = item.assets["green"].href
    blue_url = item.assets["blue"].href

    os.makedirs(
        "static/outputs",
        exist_ok=True
    )

    crop_size = 500
    half = crop_size // 2

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

        print("Pixel row:", row)
        print("Pixel column:", col)

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

    with rasterio.open(green_url) as src:

        green = src.read(
            1,
            window=window
        )

    with rasterio.open(blue_url) as src:

        blue = src.read(
            1,
            window=window
        )

    print("Red shape:", red.shape)
    print("Green shape:", green.shape)
    print("Blue shape:", blue.shape)

    rgb = np.dstack(
        (
            red,
            green,
            blue
        )
    )

    print("RGB shape:", rgb.shape)

    rgb = rgb.astype(float)

    valid = rgb[rgb > 0]

    if len(valid) == 0:
        raise Exception(
            "No valid pixels found."
        )

    low, high = np.percentile(
        valid,
        (2, 98)
    )

    rgb = np.clip(
        (rgb - low) / (high - low),
        0,
        1
    )

    # Gamma correction
    rgb = np.power(
        rgb,
        0.7
    )

    rgb = (
        rgb * 255
    ).astype(np.uint8)

    image = Image.fromarray(
        rgb
    )

    print(
        "Original image size:",
        image.size
    )

    # 2x upscale
    image = image.resize(
        (
            image.width * 2,
            image.height * 2
        ),
        Image.Resampling.LANCZOS
    )

    print(
        "Upscaled image size:",
        image.size
    )

    # Mild sharpening
    image = image.filter(
        ImageFilter.UnsharpMask(
            radius=1.2,
            percent=120,
            threshold=3
        )
    )

    output_file = (
        "static/outputs/"
        "sentinel_enhanced.png"
    )

    image.save(
        output_file
    )

    print(
        "Saved:",
        output_file
    )


if __name__ == "__main__":

    latitude = 13.0827
    longitude = 80.2707

    create_rgb_image(
        latitude,
        longitude
    )