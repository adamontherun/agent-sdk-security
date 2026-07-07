def test_all_three_is_lethal(subject):
    report = subject.assess_trifecta(True, True, True)
    assert report["lethal"] is True
    assert report["present"] == [
        "private_data",
        "untrusted_content",
        "external_comms",
    ]
    assert report["breakable_by_cutting"] == [
        "private_data",
        "untrusted_content",
        "external_comms",
    ]


def test_two_legs_is_not_lethal(subject):
    report = subject.assess_trifecta(True, True, False)
    assert report["lethal"] is False
    assert report["present"] == ["private_data", "untrusted_content"]
    assert report["breakable_by_cutting"] == []


def test_no_legs(subject):
    report = subject.assess_trifecta(False, False, False)
    assert report["lethal"] is False
    assert report["present"] == []
    assert report["breakable_by_cutting"] == []


def test_present_preserves_leg_order(subject):
    # external_comms and private_data set, untrusted_content not:
    # present must follow LEG_NAMES order, not argument-truthiness order.
    report = subject.assess_trifecta(True, False, True)
    assert report["present"] == ["private_data", "external_comms"]
    assert report["lethal"] is False
