#!/bin/sh

tox -e cookiecutter -- \
    project_description="Hello world with Django" \
    project_name="Example Django" \
    container_platform=APPUiO \
    database=Postgres \
    framework=Django \
    vcs_account=appuio \
    license=GPL-3 \
    push=force \
    --no-input
