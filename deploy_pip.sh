python setup.py sdist bdist_wheel
pip install --force-reinstall .\dist\autohelper-0.0.2-py3-none-any.whl
twine upload dist/*