from pystac_client import Client


def search_sentinel2(latitude, longitude):

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
        datetime="2025-01-01/2026-12-31",
        query={
            "eo:cloud_cover": {
                "lt": 20
            }
        },
        max_items=5
    )

    items = list(search.items())

    return items


if __name__ == "__main__":

    latitude = 13.0827
    longitude = 80.2707

    items = search_sentinel2(
        latitude,
        longitude
    )

    print("Images found:", len(items))

    for item in items:

        print("-----------------------------")
        print("ID:", item.id)
        print("Date:", item.properties.get("datetime"))
        print(
            "Cloud cover:",
            item.properties.get("eo:cloud_cover")
        )