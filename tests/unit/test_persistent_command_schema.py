"""Persistent command-envelope and operation-registry tests."""

from itertools import permutations

import pytest

from ludoweave.world import (
    COMMAND_PROTOCOL,
    TRANSACTION_PROTOCOL,
    CommandActor,
    CommandEnvelope,
    CommandSchemaError,
    CommandTransaction,
    DuplicateOperationError,
    OperationRegistry,
    OperationSpec,
    UnknownOperationError,
    builtin_operation_registry,
)


def _command(
    command_id: str = "cmd-1",
    *,
    transaction_id: str = "tx-1",
    expected_hash: str | None = "sha256:" + "0" * 64,
    arguments: dict[str, object] | None = None,
) -> CommandEnvelope:
    return CommandEnvelope(
        command_id=command_id,
        transaction_id=transaction_id,
        actor=CommandActor(kind="agent", id="codex"),
        operation="entity.spawn",
        arguments={} if arguments is None else arguments,
        expected_world_hash=expected_hash,
    )


def test_logically_equal_argument_orders_have_equal_canonical_bytes() -> None:
    items = [("name", "player"), ("x", 1.5), ("active", True)]
    encodings = {_command(arguments=dict(order)).canonical_bytes() for order in permutations(items)}

    assert len(encodings) == 1


@pytest.mark.parametrize(
    ("left", "right"),
    [
        ({"value": True}, {"value": 1}),
        ({"value": 1}, {"value": 1.0}),
        ({"value": -0.0}, {"value": 0.0}),
    ],
)
def test_command_equality_preserves_exact_canonical_number_kinds(
    left: dict[str, object], right: dict[str, object]
) -> None:
    left_command = _command(arguments=left)
    right_command = _command(arguments=right)

    assert left_command != right_command
    assert left_command.canonical_bytes() != right_command.canonical_bytes()
    assert CommandTransaction((left_command,), "arena") != CommandTransaction(
        (right_command,), "arena"
    )
    with pytest.raises(TypeError):
        hash(left_command)


def test_command_round_trip_detaches_and_freezes_arguments() -> None:
    arguments: dict[str, object] = {"components": {"type": {"x": 1.0}}}
    command = _command(arguments=arguments)
    arguments["components"] = {}

    decoded = CommandEnvelope.from_json(command.canonical_bytes())

    assert decoded == command
    assert decoded.as_dict()["arguments"] == {"components": {"type": {"x": 1.0}}}
    with pytest.raises(TypeError):
        decoded.arguments["new"] = "value"  # type: ignore[index]


def test_transaction_requires_shared_identity_actor_hash_and_unique_commands() -> None:
    transaction = CommandTransaction(
        commands=(_command(), _command("cmd-2")), world_id="arena", dry_run=True
    )
    assert transaction.transaction_id == "tx-1"
    assert transaction.protocol == TRANSACTION_PROTOCOL
    assert CommandTransaction.from_json(transaction.canonical_bytes()) == transaction

    with pytest.raises(CommandSchemaError):
        CommandTransaction(commands=(_command(), _command()), world_id="arena")
    with pytest.raises(CommandSchemaError):
        CommandTransaction(
            commands=(_command(), _command("cmd-2", transaction_id="tx-2")), world_id="arena"
        )
    with pytest.raises(CommandSchemaError):
        CommandTransaction(
            commands=(_command(), _command("cmd-2", expected_hash="sha256:" + "1" * 64)),
            world_id="arena",
        )


def test_decode_rejects_unknown_missing_and_extra_fields() -> None:
    document = _command().as_dict()
    assert document["protocol"] == COMMAND_PROTOCOL

    for key in ("command_id", "actor", "arguments"):
        malformed = dict(document)
        del malformed[key]
        with pytest.raises(CommandSchemaError):
            CommandEnvelope.from_mapping(malformed)

    malformed = dict(document)
    malformed["python_callable"] = "builtins.eval"
    with pytest.raises(CommandSchemaError):
        CommandEnvelope.from_mapping(malformed)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("command_id", ""),
        ("transaction_id", "has spaces"),
        ("operation", "eval_python"),
        ("operation", "Entity.Spawn"),
        ("operation_version", True),
        ("expected_world_hash", "sha256:not-a-hash"),
    ],
)
def test_invalid_command_identities_fail_structurally(field: str, value: object) -> None:
    document = _command().as_dict()
    document[field] = value  # type: ignore[literal-required]
    with pytest.raises(CommandSchemaError):
        CommandEnvelope.from_mapping(document)


def test_operation_versions_must_fit_the_canonical_integer_domain() -> None:
    document = _command().as_dict()
    document["operation_version"] = 2**63
    with pytest.raises(CommandSchemaError):
        CommandEnvelope.from_mapping(document)

    with pytest.raises(CommandSchemaError):
        OperationSpec("entity.spawn", version=2**63)


def test_operation_registry_is_sorted_immutable_and_versioned() -> None:
    v2 = OperationSpec("component.patch", version=2)
    spawn = OperationSpec("entity.spawn")
    v1 = OperationSpec("component.patch")
    registry = OperationRegistry((v2, spawn, v1))

    assert registry.specs == (v1, v2, spawn)
    assert registry.resolve("component.patch", 2) is v2
    with pytest.raises(UnknownOperationError):
        registry.resolve("component.patch", 3)
    with pytest.raises(DuplicateOperationError):
        OperationRegistry((spawn, spawn))

    builtins = builtin_operation_registry()
    assert builtins.resolve("world.tick", 1).transactional
    assert builtins.fingerprint.startswith("sha256:")
    assert builtins.fingerprint == builtin_operation_registry().fingerprint


def test_arguments_cannot_carry_python_types_or_callables() -> None:
    with pytest.raises(Exception) as raised:
        _command(arguments={"callable": eval})
    assert getattr(raised.value, "code", None) == "world.invalid_canonical_json"
