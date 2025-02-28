from pathlib import Path
from anutils import data_path


TEST_FILE = "the-ultimate-test.txt"
TEST_STRING = "You passed!!!"


def test_data_path_is_correct():
    """
    Verify data_path points to the right directory
    """
    assert isinstance(data_path, Path), f"{data_path} is not a Path!"
    assert data_path.is_dir(), f"Data path {data_path} is not a directory!"
    test_file = data_path / TEST_FILE
    assert test_file.exists(), f"Could not find test file in path: '{data_path}'! Perhaps this is the wrong location."
    with test_file.open() as f:
        text = f.read()
        assert text == TEST_STRING, f"Read text {text!r} does not match expected text!"