# Changelog

All notable changes to python-relations-mysql are recorded here, newest first. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow [SemVer](https://semver.org/).

## [Unreleased]

### Changed
- `make new` works on the ticket branch you're on: it writes VERSION and the changelog section there and commits, makes no branch of its own, and refuses on main, since we branch from the ticket. `B=` and `BRANCH_PREFIX` are gone (relations-dil/python-relations#98).

## [0.6.6] - 2026-10-26

### Added
- Jenkins releases on a merge to `main`: a `release` stage (only on `main`) runs `make release`, which does nothing for a version that is already released and otherwise does the test release, the release and the tag. It pushes the tag with the `github` credential, as Leroy Jenkins, one build at a time, with a two hour timeout (relations-dil/python-relations#80). The package builds run in a copy with only the files they use mounted read-only, so nothing root-owned is left in the workspace, and `make tag` stops on a failure instead of ignoring it. The release scripts work with the older git on the Jenkins host.
- `make help` lists every target with what it does (each target has a `## description` after it), and is what a bare `make` runs.
- Release tooling, the same as relations-dil's (relations-dil/python-relations#77): `make new` starts a release, `make version` sets the version, `make release-check` says where a release is up to and what would stop it, `make release` does what's left (checks, TestPyPI and a clean install from it, PyPI, the tag), `make dist-check` builds and checks the distributions, and `make test-release` tests the scripts against a throwaway repo and fake indexes. The work is in `scripts/`.
- A `VERSION` file as the one place the version is set: the `Makefile` reads it and mounts it, `testpypi` and `pypi` pass it as `BUILD_VERSION`, and `setup.py` reads `BUILD_VERSION` or the file.

### Changed
- `make release-check` and `make release` don't run `build`, `test`, `lint` and `setup` again: the Jenkins stages have just run them before the release stage, so it was the same work twice. Run them yourself before checking by hand, as `make release-check` is only the checks and `dist-check` now (relations-dil/python-relations#90).
- Every `docker run` in the `Makefile` uses `--rm`, and a replaced database container is removed with its volume (`docker rm --force -v`), so builds and test runs leave no stopped containers or volumes behind.
- `testpypi` and `pypi` run in the current `python` image with `build` and `twine` installed on the fly, so the custom `gaf3/pypi` image is no longer used.

### Fixed
- A string column is `VARCHAR(length)` when its field has a `length`, instead of always `VARCHAR(255)`, so composite keys can fit under InnoDB's 3072 byte limit. Without a length it is still `VARCHAR(255)` (relations-dil/python-relations-mysql#17).
- Requires relations-sql 0.6.11, so changing only a column's `length` on an existing table generates the `ALTER`.

## [0.6.5] - 2026-10-14

### Fixed
- A readonly string column, the key for a string id (relations-dil 0.6.18), is created with `COLLATE utf8mb4_bin` so it is compared as bytes. MySQL's default collation folds case and accents, so `abc` and `ABC` were the same key and the second was refused, unlike every other source.
- Changing a column from int to another kind drops its `AUTO_INCREMENT`, whether or not the migration says `auto` is gone, and a readonly string gets the same collation.

## [0.6.4] - 2026-06-06

- Bumped the `relations-sql` requirement to 0.6.8 and `relations-dil` to 0.6.14, supporting stores for many-to-many relations.
- Installed git in the Dockerfile; tests in `test_table.py` were updated.

## [0.6.3] - 2022-11-25

- Switched to the PyPI `relations-sql` release (0.6.7) and required `relations-dil` 0.6.12 in the requirements file.
- Renamed the distribution to `relations-mysql` and corrected wording in the README and PyPI description.

## [0.6.2] - 2022-08-05

- Prepared the package for PyPI with a `LICENSE.txt`, a `PYPI.md` description, and `testpypi` and `pypi` Makefile targets.
- Removed the git-based installs from the Dockerfile and setup step.

## [0.6.1] - 2022-04-30

- Fixed the test MySQL start script to look up the host and fail on errors so it stops looping while waiting for the database; no library changes.

## [0.6.0] - 2022-03-14

- Fixed index migrations: the MySQL `INDEX` class now generates an `ADD` prefix on `create` when altering an existing table.
- Updated dependencies to `python-relations` 0.6.9 and `relations-sql` 0.6.5, and replaced the pymysql test module with an execute test module.

## [0.5.0] - 2022-03-13

- Updated the `python-relations` requirement to 0.6.8 and `relations-sql` to 0.6.4, adding support for familial access.

## [0.4.1] - 2022-03-10

- Switched the test database image from MySQL 5.7 to MySQL 8.0.

## [0.4.0] - 2022-02-18

- Updated the `python-relations` requirement to 0.6.7 and `relations-sql` to 0.6.3, which changed labels to titles.

## [0.3.0] - 2021-11-21

- Renamed the package to `python-relations-mysql` and moved its dependencies to the relations-dil organization (`python-relations` 0.6.6, `relations-sql` 0.6.2).

## [0.2.0] - 2021-11-13

- Updated the `python-relations` requirement to 0.6.5 and `relations-sql` to 0.6.1 after the library renames.

## [0.1.0] - 2021-11-12

- Initial release of the MySQL dialect for `relations-sql`, providing MySQL versions of the expression, criterion, criteria, clause and query classes, with backtick quoting and MySQL value handling.
- Added MySQL DDL classes for `COLUMN`, `INDEX` and `TABLE`, with column kinds mapped to `TINYINT`, `BIGINT`, `DOUBLE`, `VARCHAR(255)` and `JSON`, `BIGINT AUTO_INCREMENT` for auto ids, and generated (`AS (...)`) columns for extracted JSON values.
- Included execution tests against a MySQL server, a `mysql.sh` helper, and Dockerfile, Jenkinsfile and Makefile.
