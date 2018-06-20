## Contributing to kcauto-kai

* All Pull Requests should be made to the `staging` branch. Only code tested and verified in `staging` will be merged into `master` for release.
* Please abide by the Python and JavaScript style and linting rules. kcauto-kai uses the [Flake8](http://flake8.pycqa.org/en/latest/) and an extended version of the [AirBnB JavaScript Style Guide](https://github.com/airbnb/javascript) for Python and JavasScript, respectively. Please use your favorite linter to ensure consistency.
* The JavaScript bundle for the frontend web UI is generated pre-push to master directly on staging. Please do not submit a PR with an updated `bundle.js`. If you've generated an updated `bundle.js`, check the file out back from the `staging` branch to reset it.
