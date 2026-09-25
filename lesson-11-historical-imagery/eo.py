from pystac_client import Client


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


def find_historical_images(
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

    return {
        "2018": image_2018,
        "2026": image_2026
    }