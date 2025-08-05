#!/bin/bash


for line in $(jq 'map(select(.start_date |fromdateiso8601 |tonumber  < now))| sort_by("start_date") | reverse | .[0].packages | to_entries | map(.key + ":" + .value)[]' --raw-output schedule.json); do

    package=$(echo "$line" | cut -d ':' -f 1)
    spec_0_version=$(echo "$line" | cut -d ':' -f 2)

    if pixi list -x "^$package" 2> /dev/null | grep "No packages" -q -v; then
	echo "Updating $package"
	pixi add "$package>=$spec_0_version"
    fi
done
