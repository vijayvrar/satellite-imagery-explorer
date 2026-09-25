from eo import find_satellite_image
from image_processing import create_rgb_image


def create_historical_images(latitude, longitude):

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

    result_2018 = create_rgb_image(
        image_2018,
        latitude,
        longitude,
        2018
    )

    result_2026 = create_rgb_image(
        image_2026,
        latitude,
        longitude,
        2026
    )

    return {
        "2018": {
            **result_2018,
            "scene": image_2018.id,
            "date": image_2018.properties.get("datetime"),
            "cloud_cover": image_2018.properties.get(
                "eo:cloud_cover"
            )
        },

        "2026": {
            **result_2026,
            "scene": image_2026.id,
            "date": image_2026.properties.get("datetime"),
            "cloud_cover": image_2026.properties.get(
                "eo:cloud_cover"
            )
        }
    }