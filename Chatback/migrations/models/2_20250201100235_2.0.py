from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `books` DROP INDEX `name`;
        ALTER TABLE `bookseries` DROP INDEX `name`;
        ALTER TABLE `authors` DROP INDEX `name`;
        ALTER TABLE `books` MODIFY COLUMN `series_id` BIGINT;
        ALTER TABLE `chapters` MODIFY COLUMN `author_id` BIGINT;
        ALTER TABLE `chapters` MODIFY COLUMN `book_id` BIGINT;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `books` MODIFY COLUMN `series_id` BIGINT NOT NULL;
        ALTER TABLE `chapters` MODIFY COLUMN `author_id` BIGINT NOT NULL;
        ALTER TABLE `chapters` MODIFY COLUMN `book_id` BIGINT NOT NULL;
        ALTER TABLE `books` ADD UNIQUE INDEX `name` (`name`);
        ALTER TABLE `authors` ADD UNIQUE INDEX `name` (`name`);
        ALTER TABLE `bookseries` ADD UNIQUE INDEX `name` (`name`);"""
