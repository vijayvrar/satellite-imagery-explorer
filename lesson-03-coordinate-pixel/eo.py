from pystac_client import Client
import rasterio
from rasterio.warp import transform


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


def get_pixel_location(latitude, longitude):

    item = find_satellite_image(
        latitude,
        longitude
    )

    red_url = item.assets["red"].href

    print("Satellite image:")
    print(item.id)

    with rasterio.open(red_url) as src:

        print("CRS:")
        print(src.crs)

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

        print("Raster X:", x[0])
        print("Raster Y:", y[0])

        print("Pixel row:", row)
        print("Pixel column:", col)

        print("Image width:", src.width)
        print("Image height:", src.height)


if __name__ == "__main__":

    latitude = 13.0827
    longitude = 80.2707

    get_pixel_location(
        latitude,
        longitude
    )