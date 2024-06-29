echo ">>> ** Assuming you have cloned pytorch in tests/tmp/pytorch. ** <<<"

echo "Process with numpy style..."
python docstripy/main.py tests/tmp/pytorch -o tests/tmp/pytorch2 -s numpy --len 79
python tests/inte_tests/save_docstrings.py tests/tmp/pytorch2 tests/tmp/numpy.txt

echo "Process with Google style..."
python docstripy/main.py tests/tmp/pytorch -o tests/tmp/pytorch2 -s google --len 79
python tests/inte_tests/save_docstrings.py tests/tmp/pytorch2 tests/tmp/google.txt

echo "Process with ReST style..."
python docstripy/main.py tests/tmp/pytorch -o tests/tmp/pytorch2 -s rest --len 79
python tests/inte_tests/save_docstrings.py tests/tmp/pytorch2 tests/tmp/rest.txt

echo "Done."
echo "See results in tests/tmp/<style-name>.txt"
