import pytest
from main import StateMachine, Transition


def test_state_machine_initialization():
    sm = StateMachine()
    assert sm.states == set()
    assert sm.current_state is None
    assert sm.transitions == {}


def test_add_state():
    sm = StateMachine()
    sm.add_state("idle")
    assert "idle" in sm.states
    sm.add_state("running")
    assert sm.states == {"idle", "running"}


def test_add_transition_invalid_source():
    sm = StateMachine()
    sm.add_state("idle")
    with pytest.raises(ValueError, match="Unknown source state"):
        sm.add_transition("unknown", "idle", "start")


def test_add_transition_invalid_target():
    sm = StateMachine()
    sm.add_state("idle")
    with pytest.raises(ValueError, match="Unknown target state"):
        sm.add_transition("idle", "unknown", "start")


def test_add_duplicate_transition():
    sm = StateMachine()
    sm.add_state("idle")
    sm.add_state("running")
    sm.add_transition("idle", "running", "start")
    with pytest.raises(ValueError, match="already exists"):
        sm.add_transition("idle", "running", "start")


def test_set_initial_state_valid():
    sm = StateMachine()
    sm.add_state("idle")
    sm.set_initial_state("idle")
    assert sm.current_state == "idle"


def test_set_initial_state_invalid():
    sm = StateMachine()
    with pytest.raises(ValueError, match="not defined"):
        sm.set_initial_state("idle")


def test_trigger_no_initial_state():
    sm = StateMachine()
    with pytest.raises(ValueError, match="No current state"):
        sm.trigger("start")


def test_trigger_valid():
    sm = StateMachine()
    sm.add_state("idle")
    sm.add_state("running")
    sm.add_transition("idle", "running", "start")
    sm.set_initial_state("idle")
    new_state = sm.trigger("start")
    assert new_state == "running"
    assert sm.current_state == "running"


def test_trigger_invalid_event():
    sm = StateMachine()
    sm.add_state("idle")
    sm.add_state("running")
    sm.add_transition("idle", "running", "start")
    sm.set_initial_state("idle")
    with pytest.raises(ValueError, match="No transition from"):
        sm.trigger("stop")


def test_get_possible_events_no_state():
    sm = StateMachine()
    assert sm.get_possible_events() == []


def test_get_possible_events_with_state():
    sm = StateMachine()
    sm.add_state("idle")
    sm.add_state("running")
    sm.add_state("stopped")
    sm.add_transition("idle", "running", "start")
    sm.add_transition("idle", "stopped", "stop")
    sm.set_initial_state("idle")
    events = sm.get_possible_events()
    assert "start" in events
    assert "stop" in events
    assert len(events) == 2


def test_edge_case_empty_machine():
    sm = StateMachine()
    # no states, no initial state
    assert sm.get_possible_events() == []
    with pytest.raises(ValueError, match="No current state"):
        sm.trigger("any")


def test_complex_valid_transitions():
    sm = StateMachine()
    sm.add_state("a")
    sm.add_state("b")
    sm.add_state("c")
    sm.add_transition("a", "b", "a->b")
    sm.add_transition("b", "c", "b->c")
    sm.add_transition("c", "a", "c->a")
    sm.set_initial_state("a")
    assert sm.current_state == "a"
    sm.trigger("a->b")
    assert sm.current_state == "b"
    sm.trigger("b->c")
    assert sm.current_state == "c"
    sm.trigger("c->a")
    assert sm.current_state == "a"


def test_transition_dataclass():
    t = Transition(from_state="a", to_state="b", event="go")
    assert t.from_state == "a"
    assert t.to_state == "b"
    assert t.event == "go"