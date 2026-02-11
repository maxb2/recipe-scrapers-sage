PHONY=fmt
fmt:
	uv run --group dev isort --ca --profile=black .
	uv run --group dev black .

PHONY=check-types
check-types:
	uv run --group dev ty check recipe_scrapers_sage

PHONY=ruff
ruff:
	uv run --group dev ruff check .

PHONY=check-api
check-api:
	uv run --group dev griffe check recipe_scrapers_sage

PHONY=check
check: ruff check-types

PHONY=test
test:
	uv run --group dev pytest --cov=recipe_scrapers_sage --cov-report=xml

PHONY=changelog
changelog:
	uvx git-changelog --convention conventional --template keepachangelog --parse-trailers --bump auto --in-place --output CHANGELOG.md .

PHONY=release
release:
	uvx git-changelog --convention conventional --template keepachangelog --parse-trailers --bump auto --in-place --output CHANGELOG.md . && \
	NEXT_VERSION=$$(grep -oE '## \[[0-9]+\.[0-9]+\.[0-9]+\]' CHANGELOG.md | head -1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+') && \
	uvx --from=toml-cli toml set --toml-path=pyproject.toml project.version $$NEXT_VERSION && \
	git add pyproject.toml CHANGELOG.md && \
	git commit -m "chore: Prepare release $$NEXT_VERSION" && \
	uv build && \
	uv publish && \
	git tag $$NEXT_VERSION && \
	git push && \
	git push --tags
