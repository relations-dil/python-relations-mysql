import unittest
import unittest.mock

import relations
from relations_mysql import *


class Simple(relations.Model):
    id = int
    name = str

class Meta(relations.Model):
    id = int, {"auto": True}
    name = str
    flag = bool
    spend = float
    people = set
    stuff = list
    things = dict, {"extract": "for__0____1"}
    push = str, {"inject": "stuff___1__relations.io____1"},
    tied = str, {"store": False}

    INDEX = "spend"


class TestTABLE(unittest.TestCase):

    maxDiff = None

    def test_create(self):

        ddl = TABLE(**Meta.thy().define())
        ddl.args = []

        ddl.create(indent=2)
        self.assertEqual(ddl.sql, """CREATE TABLE IF NOT EXISTS `meta` (
  `id` BIGINT AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `flag` TINYINT,
  `spend` DOUBLE,
  `people` JSON NOT NULL,
  `stuff` JSON NOT NULL,
  `things` JSON NOT NULL,
  `things__for__0____1` VARCHAR(255) AS (`things`->>'$.for[0]."1"'),
  PRIMARY KEY (`id`),
  INDEX `spend` (`spend`),
  UNIQUE `name` (`name`)
);
""")

    def test_schema(self):

        sql = []

        ddl = TABLE(
            migration={
                "name": "good",
                "schema": "dreaming"
            },
            definition={
                "name": "evil",
                "schema": "scheming"
            }
        )

        ddl.schema(sql)
        self.assertEqual(sql, ["""RENAME TABLE `scheming`.`evil` TO `dreaming`.`good`"""])

    def test_store(self):

        sql = []

        ddl = TABLE(
            migration={
                "name": "good"
            },
            definition={
                "name": "evil",
                "schema": "scheming"
            }
        )

        ddl.store(sql)
        self.assertEqual(sql, ["""RENAME TABLE `scheming`.`evil` TO `scheming`.`good`"""])

    def test_modify(self):

        ddl = TABLE(
            migration={
                "name": "good",
                "schema": "dreaming"
            },
            definition={
                "name": "evil",
                "schema": "scheming"
            }
        )

        ddl.generate()
        self.assertEqual(ddl.sql, """RENAME TABLE `scheming`.`evil` TO `dreaming`.`good`;
""")
        self.assertEqual(ddl.args, [])

        ddl = TABLE(
            migration={
                "fields": {
                    "add": Meta.thy().define()["fields"][-3:]
                }
            },
            definition=Simple.thy().define()
        )

        ddl.generate()
        self.assertEqual(ddl.sql,
            """ALTER TABLE `simple` ADD `things` JSON NOT NULL,"""
            """ADD `things__for__0____1` VARCHAR(255) AS (`things`->>'$.for[0]."1"');\n"""
        )
        self.assertEqual(ddl.args, [])

        ddl.generate(indent=2)
        self.assertEqual(ddl.sql, """ALTER TABLE `simple`
  ADD `things` JSON NOT NULL,
  ADD `things__for__0____1` VARCHAR(255) AS (`things`->>'$.for[0]."1"');
""")
        self.assertEqual(ddl.args, [])

        ddl = TABLE(
            migration={
                "fields": {
                    "change": {
                        "push": {
                            "name": "push",
                            "store": "pull"
                        },
                        "spend": {
                            "default": 1.25
                        },
                        "things": {
                            "store": "thingies"
                        }
                    }
                }
            },
            definition={
                "name": "yep",
                "fields": Meta.thy().define()["fields"]
            }
        )

        ddl.generate()
        self.assertEqual(ddl.sql,
            """ALTER TABLE `yep` """
            """CHANGE `spend` `spend` DOUBLE DEFAULT 1.25,"""
            """CHANGE `things` `thingies` JSON NOT NULL,"""
            """CHANGE `things__for__0____1` `thingies__for__0____1` VARCHAR(255) AS (`thingies`->>'$.for[0]."1"');\n"""
        )
        self.assertEqual(ddl.args, [])

        ddl = TABLE(
            migration={
                "fields": {
                    "change": {
                        "push": {
                            "name": "push",
                            "store": "pull"
                        },
                        "spend": {
                            "default": 1.25
                        },
                        "things": {
                            "store": "thingies"
                        }
                    }
                }
            },
            definition={
                "name": "yep",
                "fields": Meta.thy().define()["fields"]
            }
        )

        ddl.generate(indent=2)
        self.assertEqual(ddl.sql, """ALTER TABLE `yep`
  CHANGE `spend` `spend` DOUBLE DEFAULT 1.25,
  CHANGE `things` `thingies` JSON NOT NULL,
  CHANGE `things__for__0____1` `thingies__for__0____1` VARCHAR(255) AS (`thingies`->>'$.for[0]."1"');
""")
        self.assertEqual(ddl.args, [])

        ddl = TABLE(
            migration={
                "fields": {
                    "remove": [
                        "things",
                        "push"
                    ]
                }
            },
            definition={
                "name": "yep",
                "fields": Meta.thy().define()["fields"]
            }
        )

        ddl.generate()
        self.assertEqual(ddl.sql, """ALTER TABLE `yep` DROP `things`,DROP `things__for__0____1`;\n""")
        self.assertEqual(ddl.args, [])

        ddl = TABLE(
            migration={
                "fields": {
                    "remove": [
                        "things",
                        "push"
                    ]
                }
            },
            definition={
                "name": "yep",
                "fields": Meta.thy().define()["fields"]
            }
        )

        ddl.generate(indent=2)
        self.assertEqual(ddl.sql, """ALTER TABLE `yep`
  DROP `things`,
  DROP `things__for__0____1`;
""")
        self.assertEqual(ddl.args, [])

        ddl = TABLE(
            migration={
                "index": {
                    "add": {
                        "flag": ["flag"]
                    },
                    "remove": [
                        "price"
                    ]
                },
                "unique": {
                    "add": {
                        "flag": ["flag"]
                    },
                    "remove": [
                        "name"
                    ]
                }
            },
            definition={
                "name": "yep",
                "index": Meta.thy().define()["index"],
                "unique": Meta.thy().define()["unique"]
            }
        )

        ddl.generate()
        self.assertEqual(ddl.sql, """ALTER TABLE `yep` ADD INDEX `flag` (`flag`),DROP INDEX `price`,ADD UNIQUE `flag` (`flag`),DROP INDEX `name`;\n""")
        self.assertEqual(ddl.args, [])

        ddl.generate(indent=2)
        self.assertEqual(ddl.sql, """ALTER TABLE `yep`
  ADD INDEX `flag` (`flag`),
  DROP INDEX `price`,
  ADD UNIQUE `flag` (`flag`),
  DROP INDEX `name`;
""")
        self.assertEqual(ddl.args, [])

    def test_drop(self):

        ddl = TABLE(
            definition={
                "name": "yep"
            }
        )

        ddl.generate()
        self.assertEqual(ddl.sql, """DROP TABLE IF EXISTS `yep`;\n""")
        self.assertEqual(ddl.args, [])
