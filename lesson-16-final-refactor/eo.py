from pystac_client import Client


def find_satellite_image(latitude, longitude, start_date, end_date):

    catalog = Client.open(
        "https://earth-search.aws.element84.com/v1"
    )

    search = catalog.search(
        collections=["sentinel-2-l2a"],
        intersects={
            "type": "Point",
            "coordinates": [longitude, latitude]
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