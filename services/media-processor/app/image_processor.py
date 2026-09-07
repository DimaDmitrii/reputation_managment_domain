from io import BytesIO

from PIL import (
    Image,
    ImageDraw,
    ImageOps,
    UnidentifiedImageError,
)


class InvalidImageError(Exception):
    pass


def _open_image(data: bytes) -> Image.Image:
    try:
        image = Image.open(
            BytesIO(data)
        )

        image.verify()

        image = Image.open(
            BytesIO(data)
        )

        image = ImageOps.exif_transpose(
            image
        )

        return image.convert("RGB")

    except (
        UnidentifiedImageError,
        OSError,
    ) as exc:
        raise InvalidImageError(
            "Invalid image"
        ) from exc


def _add_watermark(
    image: Image.Image,
) -> None:

    text = "reputation-mvp"

    draw = ImageDraw.Draw(image)

    bbox = draw.textbbox(
        (0, 0),
        text,
    )

    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]

    padding = 12

    x = image.width - width - padding
    y = image.height - height - padding

    draw.text(
        (x, y),
        text,
        fill=(255, 255, 255),
        stroke_width=1,
        stroke_fill=(0, 0, 0),
    )


def create_variant(
    source: bytes,
    *,
    max_side: int,
    watermark: bool,
    quality: int = 82,
) -> bytes:

    image = _open_image(source)

    image.thumbnail(
        (max_side, max_side),
        Image.Resampling.LANCZOS,
    )

    if watermark:
        _add_watermark(image)

    output = BytesIO()

    image.save(
        output,
        format="WEBP",
        quality=quality,
        method=6,
    )

    return output.getvalue()
