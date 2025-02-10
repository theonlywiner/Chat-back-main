from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.BigIntField(pk=True)
    username = fields.CharField(max_length=80, unique=True)
    password = fields.CharField(max_length=120)

    class Meta:
        table = "user"  # 指定数据库中的表名


class BookSeries(Model):
    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=80)

    class Meta:
        table = "bookseries"  # 指定数据库中的表名


class Books(Model):
    id = fields.BigIntField(pk=True)
    series = fields.ForeignKeyField('models.BookSeries', related_name='books', null=True)
    name = fields.CharField(max_length=80)

    class Meta:
        table = "books"  # 指定数据库中的表名


class Authors(Model):
    id = fields.BigIntField(pk=True)
    info = fields.TextField()
    name = fields.CharField(max_length=80)
    dynasty = fields.CharField(max_length=80)

    class Meta:
        table = "authors"  # 指定数据库中的表名


class Chapters(Model):
    id = fields.BigIntField(pk=True)
    book = fields.ForeignKeyField('models.Books', related_name='chapters', null=True)
    name = fields.TextField()
    author = fields.ForeignKeyField('models.Authors', related_name='chapters', null=True)
    full_ancient_content = fields.TextField()
    full_modern_content = fields.TextField()

    class Meta:
        table = "chapters"  # 指定数据库中的表名


class Paragraphs(Model):
    id = fields.BigIntField(pk=True)
    chapter = fields.ForeignKeyField('models.Chapters', related_name='paragraphs')
    ancient_text = fields.TextField()
    modern_text = fields.TextField()

    class Meta:
        table = "paragraphs"  # 指定数据库中的表名
