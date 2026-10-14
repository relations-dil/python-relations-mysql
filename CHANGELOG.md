# Changelog

All notable changes to python-relations-mysql are recorded here, newest first. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow [SemVer](https://semver.org/).

## [Unreleased]

### Added
- `make help` lists every target with what it does (each target has a `## description` after it), and is what a bare `make` runs.
- Release tooling, the same as relations-dil's (relations-dil/python-relations#77): `make new` starts a release, `make version` sets the version, `make release-check` says where a release is up to and what would stop it, `make release` does what's left (checks, TestPyPI and a clean install from it, PyPI, the tag), `make dist-check` builds and checks the distributions, and `make test-release` tests the scripts against a throwaway repo and fake indexes. The work is in `scripts/`.
- A `VERSION` file as the one place the version is set: the `Makefile` reads it and mounts it, `testpypi` and `pypi` pass it as `BUILD_VERSION`, and `setup.py` reads `BUILD_VERSION` or the file.

### Changed
- Every `docker run` in the `Makefile` uses `--rm`, and a replaced database container is removed with its volume (`docker rm --force -v`), so builds and test runs leave no stopped containers or volumes behind.
- `testpypi` and `pypi` run in the current `python` image with `build` and `twine` installed on the fly, so the custom `gaf3/pypi` image is no longer used.

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
