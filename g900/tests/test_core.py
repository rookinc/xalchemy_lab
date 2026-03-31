from witness_machine.core import (
    action_cell,
    mu,
    output_signature,
    subjective_cycle,
    objective_cycle,
    tau,
)

def test_tau_wrap_subjective():
    assert tau((4, 0)) == (0, 0)

def test_tau_wrap_objective():
    assert tau((4, 1)) == (0, 1)

def test_mu_flip_subjective():
    assert mu((2, 0)) == (2, 1)

def test_mu_flip_objective():
    assert mu((2, 1)) == (2, 0)

def test_commute():
    st = (3, 0)
    assert tau(mu(st)) == mu(tau(st))

def test_subjective_cycle_0():
    assert subjective_cycle(0) == ["o0", "o1", "o2", "s2", "t0", "s0"]

def test_objective_cycle_0():
    assert objective_cycle(0) == ["o0", "o1", "o2", "s3", "t3", "s0"]

def test_action_cell_0():
    assert action_cell(0) == ["o2", "s2", "t0", "s0", "t3", "s3"]

def test_output_subjective():
    assert output_signature((1, 0)) == ("return", 4, 26)

def test_output_objective():
    assert output_signature((1, 1)) == ("forward", 5, 18)
