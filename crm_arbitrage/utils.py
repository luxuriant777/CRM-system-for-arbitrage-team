from drf_yasg import openapi


def get_authorization_parameter():
    return openapi.Parameter(
        name="Authorization",
        in_=openapi.IN_HEADER,
        type=openapi.TYPE_STRING,
        description="Enter the token you received upon login request. Add it with 'Bearer ' at the beginning, "
                    "like this: 'Bearer eyJhbGciOiJI...IyADGDjKQrVQ-wCaI'",
        required=True,
    )
