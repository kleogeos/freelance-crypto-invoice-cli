import subprocess
import sys

SCRIPT = "swap-helper.py"


def run(*args):
    return subprocess.run([sys.executable, SCRIPT, *args], capture_output=True, text=True)


def test_basic_message():
    r = run("150", "erc20", "trc20")
    assert r.returncode == 0
    assert "150" in r.stdout
    assert "ERC20" in r.stdout
    assert "TRC20" in r.stdout
    assert "simpleswap.io/?ref=" in r.stdout


def test_unknown_network():
    r = run("50", "xyz20", "trc20")
    assert r.returncode == 1
    assert "error:" in r.stderr
    assert "Traceback" not in r.stderr


def test_same_network():
    r = run("50", "trc20", "trc20")
    assert r.returncode == 1
    assert "error:" in r.stderr


def test_bad_amount():
    r = run("not-a-number", "trc20", "erc20")
    assert r.returncode != 0
    assert "Traceback" not in r.stderr


if __name__ == "__main__":
    test_basic_message()
    test_unknown_network()
    test_same_network()
    test_bad_amount()
    print("4/4 passed")
