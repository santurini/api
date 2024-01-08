#!/usr/bin/env bash

real_script_path="$(realpath "$0")"
app_home="$(realpath "$(dirname "$real_script_path")")"

docker-compose -f "$app_home/../docker-compose.yml" up --remove-orphans -V --build -d
