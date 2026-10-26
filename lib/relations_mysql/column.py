"""
Module for Column DDL
"""

# pylint: disable=unused-argument

import json

import relations_sql
import relations_mysql

class COLUMN(relations_mysql.DDL, relations_sql.COLUMN):
    """
    COLUMN DDL
    """

    KINDS = {
        "bool": "TINYINT",
        "int": "BIGINT",
        "float": "DOUBLE",
        "str": "VARCHAR(255)",
        "json": "JSON"
    }

    COLUMN_NAME = relations_mysql.COLUMN_NAME

    AUTO = """BIGINT AUTO_INCREMENT"""
    EXTRACT = """AS (%s)"""
    BINARY = """COLLATE utf8mb4_bin"""

    def __init__(self, migration=None, definition=None, added=False, **kwargs):

        super().__init__(migration, definition, added, **kwargs)

        if self.migration and self.migration.get("kind") == "bool" and "default" in self.migration:
            self.migration["default"] = int(self.migration["default"])

    @staticmethod
    def varchar(length):
        """
        The string kind, as long as the length says, the default when there isn't one
        """

        return f"VARCHAR({length})" if length else COLUMN.KINDS["str"]

    def create(self, **kwargs):
        """
        CREATE DLL, a string as long as its length says, a readonly one (a key) compared as bytes, the default
        collation folds case and accents
        """

        super().create(**kwargs)

        migration = self.migration

        if migration.get("kind") == "str" and not migration.get("auto") and "__" not in migration["store"]:

            kind = self.varchar(migration.get("length"))

            if migration.get("readonly"):
                kind = f"{kind} {self.BINARY}"

            self.sql = self.sql.replace(self.KINDS["str"], kind, 1)

    def modify(self, **kwargs): # pylint: disable=arguments-differ
        """
        MODIFY DLL
        """

        sql = [self.name()]

        kind = self.migration.get("kind", self.definition["kind"])
        store = self.migration.get("store", self.definition["store"])
        auto = self.migration.get("auto", self.definition.get("auto")) and kind == "int"
        readonly = self.migration.get("readonly", self.definition.get("readonly"))
        none = self.migration.get("none", self.definition.get("none"))
        default = self.migration.get("default", self.definition.get("default"))

        if "__" in store:

            self.extract(kind, sql, **kwargs)

        else:

            if auto:

                sql.append(self.AUTO)

            else:

                if kind == "str":
                    sql.append(self.varchar(self.migration.get("length", self.definition.get("length"))))
                else:
                    sql.append(self.KINDS.get(kind, self.KINDS["json"]))

                if kind == "str" and readonly:
                    sql.append(self.BINARY)

                if not none:
                    sql.append("NOT NULL")

            if default is not None:
                if not isinstance(default, (bool, int, float, str)):
                    default = json.dumps(default)
                quote = self.STR if isinstance(default, str) else ''
                sql.append(f"DEFAULT {quote}{default}{quote}")

        self.sql = " ".join(sql)

        self.sql = f"CHANGE {self.name(definition=True)} {self.sql}"
