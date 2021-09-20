def test_build_bogus_platform(cli):
    cli.run("-ntfoo-bar", "build", "2.7.1")
    assert cli.failed
    assert "Compiling on platform 'foo' is not yet supported" in cli.logged


def test_invalid(cli):
    cli.run("-n", "build", "foo")
    assert cli.failed
    assert "Invalid python spec: ?foo" in cli.logged

    cli.run("-n", "build", "3.6")
    assert cli.failed
    assert "Please provide full desired version" in cli.logged

    cli.run("-n", "build", "3.6.7", "-mfoo,bar")
    assert cli.failed
    assert "Unknown modules: foo, bar" in cli.logged

    cli.run("-n", "build", "conda:1.2.3")
    assert cli.failed
    assert "Python family 'conda' is not yet supported" in cli.logged
