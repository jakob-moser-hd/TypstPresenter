from _pytest.raises import raises

from typstpresenter.model.text.Text import Text
from typstpresenter.model.List import List
from typstpresenter.model.Element import Element

def test_text_creation():
    t = Text(["Hello, ", "World!"])
    assert str(t) == "Hello, World!"
    assert isinstance(t, Element)


def test_error_is_thrown_when_parameter_is_str() -> None:
    with raises(TypeError):
        Text("Hello")


def test_list_creation():
    t1 = Text(["Item 1"])
    t2 = Text(["Item 2"])
    lst = List([t1, t2])
    
    assert len(lst) == 2
    assert lst[0] == t1
    assert lst[1] == t2
    
    lst2 = lst.append(Text(["Item 3"]))
    assert len(lst2) == 3
    assert len(lst) == 2 # original should be unmodified
