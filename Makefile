POETRY := $(shell command -v poetry 2> /dev/null)

default: help

.PHONY: help
help:
	@awk '/^#/{c=substr($$0,3);next}c&&/^[[:alpha:]][[:alnum:]_-]+:/{print substr($$1,1,index($$1,":")),c}1{c=0}' $(MAKEFILE_LIST) | column -s: -t



.PHONY: pypoetry_installed
pypoetry_installed:
ifndef POETRY
    $(error "poetry is not available please install it")
endif

# Run ipython shell
shell: pypoetry_installed
	poetry run ipython

# Run tests
test: pypoetry_installed
	poetry run py.test

.PHONY: package
# Build Python wheels and source distribution
package:
	poetry build

.PHONY: clean
# Delete the build artifact
clean:
	-rm -rf dist/

.PHONY: fixtures
# Display pytest available fixtures
fixtures:
	poetry run python -m pytest --fixtures
