from pystac_client import Client
import rasterio
from rasterio.warp import transform
from rasterio.windows import Window
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


def create_crop(latitude, longitude):

    item = find_satellite_image(
        latitude,
        longitude
    )

    red_url = item.assets["red"].href

    os.makedirs(
        "static/outputs",
        exist_ok=True
    )

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

        crop_size = 500
        half = crop_size // 2

        row_start = row - half
        row_end = row + half

        col_start = col - half
        col_end = col + half

        window = Window(
            col_start,
            row_start,
            crop_size,
            crop_size
        )

        crop = src.read(
            1,
            window=window
        )

        print("Crop shape:", crop.shape)

        output_file = (
            "static/outputs/red_crop.tif"
        )

        profile = src.profile.copy()

        profile.update(
            width=crop.shape[1],
            height=crop.shape[0],
            transform=src.window_transform(window)
        )

        with rasterio.open(
            output_file,
            "w",
            **profile
        ) as dst:

            dst.write(
                crop,
                1
            )

        print(
            "Saved:",
            output_file
        )


if __name__ == "__main__":

    latitude = 13.0827
    longitude = 80.2707

    create_crop(
        latitude,
        longitude
    )