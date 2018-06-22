## Contributing to kcauto-kai

* Before opening a PR, open an issue ticket in the [kcauto-kai issue tracker](https://github.com/mrmin123/kcauto-kai/issues) referencing the work you are doing. Please reference the ticket by its # in the PR.

* All PRs should be made to the `staging` branch. Only code tested and verified in `staging` will be merged into `master` for release.

* All PRs should be up to date with `staging` at time of submission. It is up to the PR submitter to keep their branch up to date.

* Please abide by the Python and JavaScript style and linting rules. kcauto-kai uses the [Flake8](http://flake8.pycqa.org/en/latest/) and an extended version of the [AirBnB JavaScript Style Guide](https://github.com/airbnb/javascript) for Python and JavasScript, respectively. Please use your favorite linter to ensure consistency. `setup.cfg` also includes a list of Flake8 rules to ignore, which your linter should pick up automatically.

* If changes are being made to the config or to the acceptable values of the config, please either update the frontend code or make note that the frontend must be updated in the PR.

* The JavaScript bundle for the frontend web UI is generated pre-push to master directly on staging. Please do not submit a PR with an updated `bundle.js`. If you've generated an updated `bundle.js`, check the file out back from the `staging` branch to reset it.
