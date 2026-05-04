"""Tiny State Machine Framework with Transition Validation

Provides a minimal StateMachine class that validates all transitions:
- ensures that added states and transitions are consistent,
- prevents triggering invalid events from the current state,
- exposes possible events.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Set


@dataclass
class Transition:
    from_state: str
    to_state: str
    event: str


class StateMachine:
    def __init__(self) -> None:
        self.states: Set[str] = set()
        self.transitions: Dict[tuple, str] = {}
        self.current_state: Optional[str] = None

    def add_state(self, state: str) -> None:
        """Register a new state."""
        self.states.add(state)

    def add_transition(self, from_state: str, to_state: str, event: str) -> None:
        """
        Define a valid transition from one state to another on a given event.
        Raises ValueError if either state is unknown or the transition is
        already defined.
        """
        if from_state not in self.states:
            raise ValueError(f"Unknown source state: {from_state}")
        if to_state not in self.states:
            raise ValueError(f"Unknown target state: {to_state}")
        key = (from_state, event)
        if key in self.transitions:
            raise ValueError(
                f"Transition from {from_state} via {event} already exists"
            )
        self.transitions[key] = to_state

    def set_initial_state(self, state: str) -> None:
        """Set the initial state of the machine."""
        if state not in self.states:
            raise ValueError(f"Initial state '{state}' is not defined")
        self.current_state = state

    def trigger(self, event: str) -> str:
        """
        Execute a transition based on the current state and event.
        Returns the new state.  Raises ValueError if the event is invalid
        for the current state or if no initial state has been set.
        """
        if self.current_state is None:
            raise ValueError(
                "No current state – call set_initial_state() first"
            )
        key = (self.current_state, event)
        if key not in self.transitions:
            raise ValueError(
                f"No transition from '{self.current_state}' on event '{event}'"
            )
        self.current_state = self.transitions[key]
        return self.current_state

    def get_possible_events(self) -> List[str]:
        """Return list of events valid in the current state."""
        if self.current_state is None:
            return []
        return [
            event
            for (state, event) in self.transitions
            if state == self.current_state
        ]


def main() -> None:
    # Create a simple state machine
    sm = StateMachine()

    # Add states
    sm.add_state("idle")
    sm.add_state("running")
    sm.add_state("stopped")

    # Add valid transitions
    sm.add_transition("idle", "running", "start")
    sm.add_transition("running", "stopped", "stop")
    sm.add_transition("stopped", "idle", "reset")

    # Set initial state
    sm.set_initial_state("idle")
    print(f"Initial state: {sm.current_state}")

    # Trigger a valid event
    new_state = sm.trigger("start")
    print(f"After 'start': {new_state}")

    # Show possible events
    print(f"Possible events now: {sm.get_possible_events()}")

    # Continue with valid transitions
    new_state = sm.trigger("stop")
    print(f"After 'stop': {new_state}")

    new_state = sm.trigger("reset")
    print(f"After 'reset': {new_state}")

    # Demonstrate error handling for invalid event
    try:
        sm.trigger("start")  # from idle after reset, `start` is valid
        sm.trigger("stop")   # from running, `stop` is valid
        sm.trigger("reset")  # from stopped, `reset` is valid
        # Now from idle we try to trigger a non-existent event
        sm.trigger("pause")
    except ValueError as e:
        print(f"Transition error: {e}")

    # Demonstrate error handling for undefined state on transition addition
    try:
        sm.add_transition("idle", "paused", "pause")
    except ValueError as e:
        print(f"Validation error: {e}")


if __name__ == "__main__":
    main()