import os

import numpy as np
import rasterio

from PIL import Image, ImageFilter
from pystac_client import Client
from rasterio.windows import Window
from rasterio.warp import transform


def find_satellite_image(
    latitude,
    longitude,
    start_date,
    end_date
):
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
        datetime=f"{start_date}/{end_date}",
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


def create_historical_image(
    item,
    latitude,
    longitude,
    year
):
    red_url = item.assets["red"].href
    green_url = item.assets["green"].href
    blue_url = item.assets["blue"].href

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

    rgb = np.dstack(
        (
            red,
            green,
            blue
        )
    ).astype(np.float32)

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
        /
        (high - low)
    )

    rgb = np.clip(
        rgb,
        0,
        1
    )

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

    image = image.resize(
        (
            image.width * 2,
            image.height * 2
        ),
        Image.Resampling.LANCZOS
    )

    image = image.filter(
        ImageFilter.UnsharpMask(
            radius=1.2,
            percent=120,
            threshold=3
        )
    )

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
        "image": f"/static/outputs/sentinel_{year}.png",
        "scene": item.id,
        "date": item.properties.get(
            "datetime"
        ),
        "cloud_cover": item.properties.get(
            "eo:cloud_cover"
        )
    }


def create_historical_images(
    latitude,
    longitude
):
    image_2018 = find_satellite_image(
        latitude,
        longitude,
        "2018-01-01",
        "2018-12-31"
    )

    image_2026 = find_satellite_image(
        latitude,
        longitude,
        "2026-01-01",
        "2026-12-31"
    )

    result_2018 = create_historical_image(
        image_2018,
        latitude,
        longitude,
        2018
    )

    result_2026 = create_historical_image(
        image_2026,
        latitude,
        longitude,
        2026
    )

    return {
        "2018": result_2018,
        "2026": result_2026
    }