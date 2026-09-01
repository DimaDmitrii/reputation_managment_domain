import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.media import Media


class MediaRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        *,
        media_id: uuid.UUID,
        filename: str,
        object_key: str,
        content_type: str,
        expected_size: int,
    ) -> Media:

        media = Media(
            id=media_id,
            original_filename=filename,
            object_key=object_key,
            content_type=content_type,
            expected_size=expected_size,
            status="uploading",
        )

        self.session.add(media)

        await self.session.commit()
        await self.session.refresh(media)

        return media

    async def get(
        self,
        media_id: uuid.UUID,
    ) -> Media | None:

        result = await self.session.execute(
            select(Media).where(
                Media.id == media_id
            )
        )

        return result.scalar_one_or_none()

    async def mark_uploaded(
        self,
        media: Media,
        actual_size: int,
    ) -> Media:

        media.status = "uploaded"
        media.actual_size = actual_size

        await self.session.commit()
        await self.session.refresh(media)

        return media
