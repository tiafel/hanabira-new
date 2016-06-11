# -*- coding: utf-8 -*-
# vim: ts=4 noet sw=4 sts=4

# начать изучение pytest можно отсюда: http://pytest.org/latest/

import pytest # не используется в данной либе сейчас

def func(x):
	return x + 1

def test_answer():
	assert func(3) == 5

