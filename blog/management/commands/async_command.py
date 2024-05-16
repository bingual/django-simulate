import asyncio
from typing import List

from asgiref.sync import sync_to_async
from django.core.management import BaseCommand
from django.db import transaction

from blog.models import Post, Comment
import nest_asyncio

nest_asyncio.apply()


class Command(BaseCommand):

    def handle(self, *args, **options):
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        asyncio.run(self.main())

    @classmethod
    async def main(cls):
        post_instances = await cls.create_post_instances(size=100)
        comment_instances = await cls.create_comment_instances(post_instances, size=100)
        await sync_to_async(cls.save_to_db)(post_instances, comment_instances)

    @classmethod
    async def create_post_instances(cls, size: int = 100) -> List[Post]:
        post_instances = []
        for i in range(1, size + 1):
            post_instances.append(
                Post(title=f"Test post title{i}", content=f"Test post content{i}")
            )
        return post_instances

    @classmethod
    async def create_comment_instances(
        cls, post_list: List[Post], size: int = 10
    ) -> List[Comment]:
        comment_instances = []
        for post in post_list:
            for i in range(1, size + 1):
                comment_instances.append(
                    Comment(post=post, content=f"Test comment content{i}")
                )
        return comment_instances

    @classmethod
    def save_to_db(cls, post_instances: List[Post], comment_instances: List[Comment]):
        with transaction.atomic():
            Post.objects.bulk_create(post_instances)
            Comment.objects.bulk_create(comment_instances)
