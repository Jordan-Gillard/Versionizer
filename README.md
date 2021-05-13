# Versionizer
## About
Versionizer is a tool for automatically generating unit tests for functions that change between two commits. This
project was created under the guidance of Dr. Na Meng as part of Virginia Tech's CS 6704 Advanced Topics in 
Software Engineering Research. 

## Use
To use Versionizer, download it using your package manager. For example:
```shell
pip install versionizer
```
or if you're using Poetry (always recommended)
```shell
poetry add versionizer
```
Once you have Versionizer installed, import it into your project and create an instance of the `Versionizer` class.
Versionizer needs only two arguments to get started - the hash of a previous commit, and the directory to test. To run
Versionizer, just call the `run()` function.
```python
from versionizer.versionizer import Versionizer

v = Versionizer(
    project_path="some/path",
    first_commit="some_commit_hash"
)
v.run()
```
And thats it! Versionizer will find all the refactored functions between the previous commit and the current commit
pointed at by your Git repositories `HEAD`. For further customization, check out the `Versionizer` class 
[here](versionizer/versionizer.py).

## Future Features
* Between Commit function diffing will be moved to another project and also be on PyPI.
* CI/CD to assert no breaking changes get into master.
* More test cases + bug fixes
