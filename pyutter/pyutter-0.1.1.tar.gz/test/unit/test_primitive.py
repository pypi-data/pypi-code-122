from pyutter.core.primitive import Text, ButtonWidget, Function


def test_widget():
    x = Text()
    assert x() == ('', [{}])


def test_text():
    x = Text()
    computed_properties = x.__properties__()
    assert computed_properties['tag'] == "plain"
    assert computed_properties['traits']["render"] == 1
    assert "text" in computed_properties['traits'].keys()
    print(x.__properties__())
    print(x.__properties__().keys())


def test_button_widget_with_action():
    x = ButtonWidget([])
    computed_properties = x.__properties__()
    assert computed_properties['traits']["render"] == 1
    assert "actionId" not in computed_properties['traits'].keys()
    assert "actionVars" not in computed_properties['traits'].keys()
    assert "actionEvent" not in computed_properties['traits'].keys()


def test_action_button_widget():
    mock_callable = lambda: 4
    f = Function(mock_callable)
    x = ButtonWidget([], action=f)
    computed_properties = x.__properties__()

    assert x() == ('', [{}])
    assert computed_properties['traits']["render"] == 1
    assert "actionId" in computed_properties['traits'].keys()
    assert computed_properties['traits']["actionId"] == f.id
    assert "actionVars" in computed_properties['traits'].keys()
    assert "actionEvent" in computed_properties['traits'].keys()
