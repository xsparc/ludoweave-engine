"""Single-owner engine lifecycle and deterministic fixed-tick walking skeleton."""

from dataclasses import dataclass
from enum import Enum
from threading import get_ident
from types import TracebackType

from ludoweave.app.config import EngineConfig
from ludoweave.core.clock import Clock, MonotonicClock
from ludoweave.core.errors import ConfigurationError, LifecycleError
from ludoweave.render.api import RenderBackend, RenderDescriptor


class LifecycleState(Enum):
    """Observable engine lifecycle states."""

    CREATED = "created"
    INITIALIZING = "initializing"
    READY = "ready"
    RUNNING = "running"
    STOPPED = "stopped"
    FAILED = "failed"
    CLOSED = "closed"


@dataclass(frozen=True, slots=True)
class RunSummary:
    """Immutable result of one configured fixed-tick run."""

    ticks: int
    frames: int
    start_ns: int
    end_ns: int
    fixed_hz: int
    renderer: str

    @property
    def elapsed_ns(self) -> int:
        return self.end_ns - self.start_ns


class Engine:
    """M0 application lifecycle owner.

    The engine takes ownership of the injected render backend. All lifecycle
    methods must run on the constructing thread; the object is not concurrently
    safe. Closing is explicit and idempotent.
    """

    __slots__ = ("_backend", "_clock", "_config", "_descriptor", "_owner_thread", "_state")

    def __init__(
        self,
        config: EngineConfig,
        backend: RenderBackend,
        *,
        clock: Clock | None = None,
        descriptor: RenderDescriptor | None = None,
    ) -> None:
        self._config = config
        self._backend = backend
        self._clock = MonotonicClock() if clock is None else clock
        self._descriptor = RenderDescriptor() if descriptor is None else descriptor
        self._owner_thread = get_ident()
        self._state = LifecycleState.CREATED

    @property
    def state(self) -> LifecycleState:
        return self._state

    @property
    def config(self) -> EngineConfig:
        return self._config

    def initialize(self) -> None:
        """Initialize the owned backend or close it after a failed attempt."""

        self._assert_owner_thread()
        self._require_state("initialize", LifecycleState.CREATED)
        self._state = LifecycleState.INITIALIZING
        try:
            self._backend.initialize(self._descriptor)
        except Exception as error:
            self._state = LifecycleState.FAILED
            cleanup_error_type = self._cleanup_failed_initialization()
            details: dict[str, str] = {"cause_type": type(error).__name__}
            if cleanup_error_type is not None:
                details["cleanup_error_type"] = cleanup_error_type
            raise LifecycleError(
                "render backend initialization failed",
                code="engine.initialization_failed",
                subsystem="application",
                phase="initialize",
                details=details,
            ) from error
        self._state = LifecycleState.READY

    def run(self, ticks: int) -> RunSummary:
        """Execute exactly ``ticks`` fixed steps and perform orderly shutdown."""

        self._assert_owner_thread()
        self._require_state("run", LifecycleState.READY)
        self._validate_tick_count(ticks)

        start_ns = self._clock.now_ns()
        completed = 0
        failure: Exception | None = None
        self._state = LifecycleState.RUNNING
        try:
            for tick in range(ticks):
                deadline_ns = start_ns + ((tick + 1) * 1_000_000_000) // self._config.fixed_hz
                self._clock.wait_until_ns(deadline_ns)
                self._backend.render(tick=tick)
                completed += 1
        except Exception as error:
            failure = error
        finally:
            if self._state is LifecycleState.RUNNING:
                self.shutdown()

        if failure is not None:
            raise LifecycleError(
                "fixed-tick run failed",
                code="engine.run_failed",
                subsystem="application",
                phase="run",
                details={"cause_type": type(failure).__name__, "ticks_completed": completed},
            ) from failure

        return RunSummary(
            ticks=completed,
            frames=completed,
            start_ns=start_ns,
            end_ns=self._clock.now_ns(),
            fixed_hz=self._config.fixed_hz,
            renderer=self._backend.name,
        )

    def shutdown(self) -> None:
        """Stop a ready or running engine without releasing its backend."""

        self._assert_owner_thread()
        self._require_state("shutdown", LifecycleState.READY, LifecycleState.RUNNING)
        self._state = LifecycleState.STOPPED

    def close(self) -> None:
        """Release the owned backend once and leave the engine closed."""

        self._assert_owner_thread()
        if self._state is LifecycleState.CLOSED:
            return
        if self._state in (LifecycleState.READY, LifecycleState.RUNNING):
            self._state = LifecycleState.STOPPED
        try:
            self._backend.close()
        except Exception as error:
            raise LifecycleError(
                "render backend close failed",
                code="engine.close_failed",
                subsystem="application",
                phase="close",
                details={"cause_type": type(error).__name__},
            ) from error
        finally:
            self._state = LifecycleState.CLOSED

    def __enter__(self) -> "Engine":
        self.initialize()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool:
        self.close()
        return False

    def _assert_owner_thread(self) -> None:
        current_thread = get_ident()
        if current_thread != self._owner_thread:
            raise LifecycleError(
                "engine lifecycle methods must run on the creating thread",
                code="engine.wrong_thread",
                subsystem="application",
                phase="threading",
                details={"operation_thread": current_thread, "owner_thread": self._owner_thread},
            )

    def _require_state(self, operation: str, *allowed: LifecycleState) -> None:
        if self._state not in allowed:
            raise LifecycleError(
                f"cannot {operation} engine from {self._state.value} state",
                code="engine.invalid_transition",
                subsystem="application",
                phase=operation,
                details={
                    "operation": operation,
                    "state": self._state.value,
                    "allowed": ",".join(state.value for state in allowed),
                },
            )

    @staticmethod
    def _validate_tick_count(ticks: object) -> None:
        if isinstance(ticks, bool) or not isinstance(ticks, int) or ticks < 0:
            raise ConfigurationError(
                "ticks must be a non-negative integer",
                code="config.invalid_tick_count",
                subsystem="application",
                phase="run",
                details={"ticks": repr(ticks)},
            )

    def _cleanup_failed_initialization(self) -> str | None:
        cleanup_error_type: str | None = None
        try:
            self._backend.close()
        except Exception as cleanup_error:
            cleanup_error_type = type(cleanup_error).__name__
        finally:
            self._state = LifecycleState.CLOSED
        return cleanup_error_type
