import subprocess

def test_ec2pricing_fetch_pricing():
    result = subprocess.run(
        ["ec2pricing", "t3.micro", "--os", "windows", "--distro", "microsoft"],
        capture_output=True,
        text=True,
        timeout=30,  # in case it takes some time
    )

    # Assert command succeeded
    assert result.returncode == 0

    # Check that the output contains expected starting messages
    expected_messages = [
        "📡 Fetching enabled AWS regions",
        "🌎 Found 17 regions",
        "💰 Fetching pricing data",
        "📄 Total pricing pages fetched: 1",
    ]

    output = result.stdout
    for message in expected_messages:
        assert message in output, f"Expected '{message}' in output"
