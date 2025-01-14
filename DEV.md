# Developing

- [Running devenv scripts](#running-devenv-scripts)
- [Configuring VS Code/Cursor Python Interpreter](#configuring-vscodecursor-python-interpreter)

## Running devenv scripts

This project uses `devenv` activated via `direnv` to automatically set up the dev environment,
and invite you into a shell with the corrent binaries, scripts, and environment variables.

Once you successfully activated the environment running `direnv allow`, you can run the following scripts:

### Running the API

To run the API:
```bash
$ start
```

To run the API in Docker:
```bash
$ docker-build
$ docker-run
```

Cursor/VS Code should open up a dialog asking you to launch a browser for accessing the API endpoint.

### Running Tests
To run tests:
```bash
$ pytest
```

## Configuring VS Code/Cursor Python Interpreter

> We now have a `.vscode/settings.json` file that sets the default interpreter path to the devenv-managed virtual environment.
> The following steps are no longer necessary.

To configure VS Code or Cursor to use the Python interpreter from your devenv-managed virtual environment:

1. Find your virtual environment path:
   ```bash
   $ echo $VIRTUAL_ENV
   /Users/username/path/to/project/.devenv/state/venv
   ```

2. Open VS Code/Cursor Command Palette (Cmd/Ctrl + Shift + P)
   - Type: "Python: Select Interpreter"
   - Click "Enter interpreter path..."
   - Click "Find..."

3. Enter the full path to the Python interpreter:
   ```
   /Users/username/path/to/project/.devenv/state/venv/bin/python3
   ```
   Note: Always append `bin/python3` to your `$VIRTUAL_ENV` path

4. VS Code/Cursor will now use the devenv-managed Python interpreter for:
   - IntelliSense
   - Linting
   - Debugging
   - Running Python files

### Verification

To verify the correct interpreter is being used:
- Create a new Python file
- Check the Python interpreter shown in the bottom status bar
- It should match the path from your devenv environment

