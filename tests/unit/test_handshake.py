import json
import uuid
import pathlib as pl

import pytest

import handshakes

test_input_dir = pl.Path("doesntexist_input")
test_output_dir = pl.Path("doesntexist_ouput")


def test_init():
    handshake = handshakes.FileHandshaker(
        "Initiator",
        pl.Path(test_input_dir),
        pl.Path(test_output_dir),
    )

    assert isinstance(handshake, handshakes.FileHandshaker)
    assert handshake.is_initiator is False


def test_init_fail():
    with pytest.raises(TypeError) as exc_info:
        _ = handshakes.FileHandshaker("Initiator", pl.Path(test_output_dir))

        assert (
            exc_info.value
            == "__init__() missing 1 required positional argument: 'output_dir_path'"
        )


def test_handshake_initiator(mocker):
    initiator_uuid = str(uuid.uuid4())
    receiver_uuid = str(uuid.uuid4())

    initiator_handshake = handshakes.FileHandshaker(
        initiator_uuid,
        pl.Path(test_input_dir),
        pl.Path(test_output_dir),
        is_initiator=True,
    )

    assert initiator_handshake.is_initiator is True

    mocker.patch.object(
        initiator_handshake, "wait_for_path_exists", return_value=True
    )

    returned_confirmed_handshake = {
        "uuid": receiver_uuid,
        "confirmed_uuid": initiator_uuid,
        "command": "confirm_registration",
    }
    mocker.patch.object(
        pl.Path,
        "read_text",
        return_value=json.dumps(returned_confirmed_handshake),
    )

    written_texts = []

    def mock_write_text(content):
        nonlocal written_texts
        written_texts.append(content)

    mocker.patch.object(pl.Path, "write_text", side_effect=mock_write_text)

    other_uuid = initiator_handshake.shake()

    assert initiator_handshake.other_uuid == receiver_uuid
    assert other_uuid == receiver_uuid

    assert len(written_texts) == 2

    register_handshake = {
        "uuid": initiator_uuid,
        "command": "register",
    }

    assert json.loads(written_texts[0]) == register_handshake

    confirmed_handshake = {
        "uuid": initiator_uuid,
        "confirmed_uuid": receiver_uuid,
        "command": "confirm_registration",
    }

    assert json.loads(written_texts[1]) == confirmed_handshake


def test_handshake_receiver(mocker):
    initiator_uuid = "Initiator"
    receiver_uuid = "Receiver"

    receiver_handshake = handshakes.FileHandshaker(
        receiver_uuid,
        pl.Path(test_input_dir),
        pl.Path(test_output_dir),
    )

    assert receiver_handshake.is_initiator is False

    mocker.patch.object(
        receiver_handshake, "wait_for_path_exists", return_value=True
    )

    register_handshake = {
        "uuid": initiator_uuid,
        "command": "register",
    }

    returned_confirmed_handshake = {
        "uuid": initiator_uuid,
        "confirmed_uuid": receiver_uuid,
        "command": "confirm_registration",
    }

    read_texts = [
        json.dumps(register_handshake),
        json.dumps(returned_confirmed_handshake),
    ]

    mocker.patch.object(pl.Path, "read_text", side_effect=read_texts)

    written_texts = []

    def mock_write_text(content):
        nonlocal written_texts
        written_texts.append(content)

    mocker.patch.object(
        pl.Path,
        "write_text",
        side_effect=mock_write_text,
    )

    other_uuid = receiver_handshake.shake()

    assert other_uuid == initiator_uuid
    assert receiver_handshake.other_uuid == initiator_uuid

    assert len(written_texts) == 1

    confirmed_handshake = {
        "uuid": receiver_uuid,
        "confirmed_uuid": initiator_uuid,
        "command": "confirm_registration",
    }

    assert json.loads(written_texts[0]) == confirmed_handshake
