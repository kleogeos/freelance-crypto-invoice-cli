import json
import subprocess
import sys
import tempfile
import os

PY = sys.executable
SCRIPT = "invoice.py"


def run(*args):
    return subprocess.run([PY, SCRIPT, *args], capture_output=True, text=True)


def write_json(data):
    f = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
    json.dump(data, f)
    f.close()
    return f.name


def base(**overrides):
    d = {
        "invoice_number": "INV-0001", "from": "A", "to": "B",
        "network": "TRC20", "address": "Taddr123",
        "items": [{"description": "x", "qty": 1, "rate": 100}],
    }
    d.update(overrides)
    return d


def test_example_json_from_repo():
    r = run("example.json")
    assert r.returncode == 0, r.stderr
    assert "Acme Freelancer" in r.stdout
    assert "TRC20" in r.stdout


def test_total_math():
    path = write_json(base(items=[{"description": "x", "qty": 2, "rate": 50}]))
    r = run(path)
    os.unlink(path)
    assert r.returncode == 0, r.stderr
    assert "Total: $100.00" in r.stdout


def test_qr_code_embedded_with_address():
    path = write_json(base(address="TAbCdEf999"))
    r = run(path)
    os.unlink(path)
    assert "api.qrserver.com" in r.stdout
    assert "TAbCdEf999" in r.stdout


def test_unknown_network_rejected():
    path = write_json(base(network="SOLANA"))
    r = run(path)
    os.unlink(path)
    assert r.returncode != 0
    assert "network must be one of" in r.stderr


def test_missing_address_rejected_cleanly():
    d = base()
    del d["address"]
    path = write_json(d)
    r = run(path)
    os.unlink(path)
    assert r.returncode != 0
    assert "error:" in r.stderr
    assert "Traceback" not in r.stderr


def test_description_is_html_escaped():
    path = write_json(base(items=[{"description": "<script>alert(1)</script>", "qty": 1, "rate": 10}]))
    r = run(path)
    os.unlink(path)
    assert "<script>" not in r.stdout
    assert "&lt;script&gt;" in r.stdout


def test_output_file_written():
    path = write_json(base(invoice_number="INV-0007"))
    out_path = path + ".html"
    r = run(path, "-o", out_path)
    assert r.returncode == 0, r.stderr
    assert os.path.exists(out_path)
    content = open(out_path).read()
    assert "INV-0007" in content
    os.unlink(path)
    os.unlink(out_path)


def test_bad_json_input_rejected_cleanly():
    f = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
    f.write("{not valid json")
    f.close()
    r = run(f.name)
    os.unlink(f.name)
    assert r.returncode != 0
    assert "error:" in r.stderr
    assert "Traceback" not in r.stderr


def test_missing_file_rejected_cleanly():
    r = run("/tmp/does-not-exist-12345.json")
    assert r.returncode != 0
    assert "error:" in r.stderr
    assert "Traceback" not in r.stderr


if __name__ == "__main__":
    failures = 0
    tests = [v for k, v in list(globals().items()) if k.startswith("test_")]
    for t in tests:
        try:
            t()
            print(f"PASS: {t.__name__}")
        except AssertionError as e:
            failures += 1
            print(f"FAIL: {t.__name__}: {e}")
    if failures:
        print(f"{failures} failure(s)")
        sys.exit(1)
    print(f"All {len(tests)} tests passed")
