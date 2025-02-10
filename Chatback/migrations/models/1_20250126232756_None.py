from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `authors` (
    `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `info` LONGTEXT NOT NULL,
    `name` VARCHAR(80) NOT NULL UNIQUE,
    `dynasty` VARCHAR(80) NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `bookseries` (
    `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(80) NOT NULL UNIQUE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `books` (
    `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(80) NOT NULL UNIQUE,
    `series_id` BIGINT NOT NULL,
    CONSTRAINT `fk_books_bookseri_42fd48c9` FOREIGN KEY (`series_id`) REFERENCES `bookseries` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `chapters` (
    `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` LONGTEXT NOT NULL,
    `full_ancient_content` LONGTEXT NOT NULL,
    `full_modern_content` LONGTEXT NOT NULL,
    `author_id` BIGINT NOT NULL,
    `book_id` BIGINT NOT NULL,
    CONSTRAINT `fk_chapters_authors_e7aa5ec7` FOREIGN KEY (`author_id`) REFERENCES `authors` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_chapters_books_b0a6ae73` FOREIGN KEY (`book_id`) REFERENCES `books` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `paragraphs` (
    `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `ancient_text` LONGTEXT NOT NULL,
    `modern_text` LONGTEXT NOT NULL,
    `chapter_id` BIGINT NOT NULL,
    CONSTRAINT `fk_paragrap_chapters_493a5888` FOREIGN KEY (`chapter_id`) REFERENCES `chapters` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `user` (
    `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `username` VARCHAR(80) NOT NULL UNIQUE,
    `password` VARCHAR(120) NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
