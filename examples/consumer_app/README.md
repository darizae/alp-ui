# Installed-wheel consumer

This example uses only the public wheel API. It creates the one `QApplication`,
installs the Theme, composes four Components in a native Qt layout, supplies its own
`QAbstractTableModel`, and handles native signals.

Build the distributions, create a fresh virtual environment outside this repository,
and install the wheel:

```bash
.venv/bin/python -m build
python3.13 -m venv /tmp/alp-ui-consumer
/tmp/alp-ui-consumer/bin/python -m pip install dist/alp_ui-0.1.0a0-py3-none-any.whl
```

Then run the example. `-I` prevents user site packages and environment path settings
from changing the import result:

```bash
/tmp/alp-ui-consumer/bin/python -I examples/consumer_app/main.py
/tmp/alp-ui-consumer/bin/python -I examples/consumer_app/main.py --custom-theme
```

Use `--smoke` with either command for an automated open-and-clean-shutdown check. On
Windows, use the environment's `Scripts\python.exe` path instead of `bin/python` and
place the virtual environment outside the repository in any suitable temporary
directory.
