============================= test session starts ==============================
platform linux -- Python 3.13.12, pytest-9.0.2, pluggy-1.6.0 -- /home/jules/.cache/uv/builds-v0/.tmpSILTaz/bin/python
cachedir: .pytest_cache
rootdir: /app/backend
configfile: pyproject.toml
plugins: anyio-4.12.1
collecting ... collected 4 items

core_ingestion/tests/test_ingestion_dag.py::test_topological_bottom_up_ordering PASSED [ 25%]
core_ingestion/tests/test_ingestion_dag.py::test_cycle_detection PASSED  [ 50%]
core_ingestion/tests/test_ingestion_dag.py::test_working_memory_refresher_injection PASSED [ 75%]
core_ingestion/tests/test_ingestion_dag.py::test_multi_source_extraction PASSED [100%]

=============================== warnings summary ===============================
../../home/jules/.cache/uv/archive-v0/O2VKV_O0YWGC6LcxbYp5a/lib/python3.13/site-packages/_pytest/config/__init__.py:1428
  /home/jules/.cache/uv/archive-v0/O2VKV_O0YWGC6LcxbYp5a/lib/python3.13/site-packages/_pytest/config/__init__.py:1428: PytestConfigWarning: Unknown config option: asyncio_mode

    self._warn_or_fail_if_strict(f"Unknown config option: {key}\n")

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
========================= 4 passed, 1 warning in 0.14s =========================
