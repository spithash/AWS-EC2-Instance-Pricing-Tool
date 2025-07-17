import subprocess

def test_ec2pricing_help():
    result = subprocess.run(
        ["ec2pricing", "-h"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "usage" in result.stdout.lower()

def test_ec2pricing_missing_args():
    result = subprocess.run(
        ["ec2pricing", "t2.micro", "--os", "linux"],
        capture_output=True,
        text=True
    )
    # Shouldn't crash, even if no distro is provided
    assert result.returncode == 0 or result.returncode == 1

