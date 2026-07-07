import pytest


def test_light_sessions_fill_the_host(subject):
    plan = subject.agents_per_host(16, 2, 1)
    assert plan.agents == 14
    assert plan.usable_ram_gib == 14
    assert plan.leftover_gib == 0


def test_heavy_sessions_leave_headroom(subject):
    plan = subject.agents_per_host(16, 2, 3)
    # (16 - 2) / 3 = 4.67 -> 4 sessions, 2 GiB left over.
    assert plan.agents == 4
    assert plan.leftover_gib == pytest.approx(2.0)


def test_floor_not_round(subject):
    # 13 / 3 = 4.33 must floor to 4, never round to 4 or up to 5.
    plan = subject.agents_per_host(15, 2, 3)
    assert plan.agents == 4


def test_overhead_swallows_all_ram(subject):
    plan = subject.agents_per_host(2, 2, 1)
    assert plan.agents == 0
    assert plan.usable_ram_gib == 0
    assert plan.leftover_gib == 0


def test_overhead_exceeds_ram_is_not_negative(subject):
    plan = subject.agents_per_host(1, 4, 1)
    assert plan.agents == 0
    assert plan.usable_ram_gib == 0


def test_zero_ceiling_is_an_error(subject):
    with pytest.raises(ValueError):
        subject.agents_per_host(16, 2, 0)
