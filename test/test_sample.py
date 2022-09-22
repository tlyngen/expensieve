import pytest

def test_method1():
	x=5
	y=6
	assert x+1 == y,"test failed because x=" + str(x) + " y=" + str(y)