# Log helper tools (`run_with_log.py` and `watch_log.py`)

## What problem these tools solve

Long-running commands are easier to debug when you can:

1. see output live in your current terminal,
2. keep a full log on disk,
3. watch that same log in another terminal/editor pane.

These tools provide that workflow in a cross-platform way using only Python 3 standard library.

## Why these are external wrappers (not product logging changes)

These scripts run **outside** your application process. That means you can add live mirrored logging for any command without changing product code, logging frameworks, or runtime behavior inside the app itself.

## CLI reference

### `tools/run_with_log.py`

Runs an arbitrary command, merges `stderr` into `stdout`, streams output live to console, and writes the same merged output to a log file.

```bash
python tools/run_with_log.py [--log PATH] COMMAND [ARG ...]
```

- `--log PATH`: log file path (default: `run.log`)
- `COMMAND [ARG ...]`: command to execute

Examples:

```bash
python tools/run_with_log.py --log run.log python -u main.py
python tools/run_with_log.py --log logs/latest.log uv run python -u main.py
```

If no command is provided, it prints a helpful error and exits non-zero.

### `tools/watch_log.py`

Watches a log file and prints newly appended content in real time.

```bash
python tools/watch_log.py LOG_PATH
```

Examples:

```bash
python tools/watch_log.py run.log
python tools/watch_log.py logs/latest.log
```

Behavior notes:

- If the file does not exist yet, it waits until the file appears.
- Uses polling with a short sleep interval for cross-platform simplicity.
- Decodes text as UTF-8 with replacement for invalid bytes.

## Typical workflow (two terminals)

### Terminal A (run command + write log)

```bash
python tools/run_with_log.py --log logs/latest.log python -u main.py
```

### Terminal B (watch log in real time)

```bash
python tools/watch_log.py logs/latest.log
```

## Unix/macOS/Linux usage

Use the same commands as above in your shell.

```bash
python tools/run_with_log.py --log logs/latest.log python -u main.py
python tools/watch_log.py logs/latest.log
```

## Windows PowerShell and VSCode terminal usage

Use exactly the same command forms in PowerShell or the VSCode integrated terminal.

```powershell
python tools/run_with_log.py --log logs/latest.log python -u main.py
python tools/watch_log.py logs/latest.log
```

## Buffering note

Some programs buffer their output internally, which can delay what you see in real time.
For Python commands, prefer `python -u` to reduce buffering.

## Minimal VSCode integrated terminal example

Open two integrated terminals:

- **Terminal 1** runs the app with mirrored logging.
- **Terminal 2** follows the log file.

```bash
# Terminal 1
python tools/run_with_log.py --log logs/latest.log python -u main.py

# Terminal 2
python tools/watch_log.py logs/latest.log
```

## Design rationale

- **Cross-platform first:** no reliance on shell tools like `tee`/`tail`.
- **Standard library only:** easy setup and auditability.
- **Minimal surface area:** two small scripts with stable, explicit CLI.
- **No product code changes:** works as a wrapper around any existing command.
- **Merged stream semantics:** `stderr` is redirected into `stdout` so console and log content match.
