# SPEC-0 Versions Action

This repository contains a Github Action to update python dependencies conform the SPEC 0 support schedule.
It also contains released versions of the schedule in various formats that that action can use to open PRs in your repository.

## Using the action

```yaml
name: Update SPEC 0 dependencies

on:
  workflow_dispatch:
  schedule:
    # At 00:00 on day-of-month 2 in every 3rd month. (i.e. every quarter)
    # Releases should happen on the first day of the month in scientific-python/spec-zero-tools
    # so allow one day as a buffer to avoid timing issues
    - cron: "0 0 2 */3 *"

permissions:
  contents: write
  pull-requests: write

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: scientific-python/spec-zero-tools@main
        with:
          token: ${{ secrets.GH_PAT }}
          target_branch: main
          tool: pixi
```

Whenever the action is triggered it will open a PR in your repository that will update the dependencies of SPEC 0 to the new lower bound. For this you will have to provide it with a PAT that has write permissions in the `contents` and `pull request` scopes. Please refer to the GitHub documentation for instructions on how to do this [here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens).

To help projects stay compliant with SPEC-0, we provide a `schedule.json` file that can be used by CI systems to determine new version boundaries.

Currently the action can take the following inputs:

| Name            | Description                                                                                                                                              | Required |
| --------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- |
| `token`         | The token that the action will use to create and update the pull request. See [token](https://github.com/marketplace/actions/create-pull-request#token). | Yes      |
| `tool`          | Which tool to use for managing your dependencies. Currently `pixi` is the only option.                                                                   | No       |
| `target_branch` | The branch to open a PR against with the updated versions. Defaults to `main`.                                                                           | No       |

## Limitations

This project is still in progress and thus it comes with some limitations we are working on. Hopefully this will be gone by the time you read this, but currently the limitations are:

- Only `pixi` is supported
- if you have a higher bound than the one listed in SPEC 0 this is overwritten
- higher bounds are deleted instead of maintained.
- dependency groups are not yet supported
