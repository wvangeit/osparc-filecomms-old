import concurrent.futures as futures
import uuid

from osparc_filecomms import handshakers


def run_handshake(self_uuid, input_dir_path, output_dir_path, is_initiator):
    handshake = handshakers.FileHandshaker(
        self_uuid, input_dir_path, output_dir_path, is_initiator
    )
    other_uuid = handshake.shake()

    return other_uuid


def test_handshakes_functional(tmp_path):
    test_input_dir = tmp_path / "test_input_dir"
    test_output_dir = tmp_path / "test_output_dir"
    test_input_dir.mkdir()
    test_output_dir.mkdir()

    initiator_uuid = str(uuid.uuid4())
    receiver_uuid = str(uuid.uuid4())

    executor = futures.ProcessPoolExecutor(max_workers=2)
    initiator_other_uuid = executor.submit(
        run_handshake, initiator_uuid, test_input_dir, test_output_dir, True
    )
    receiver_other_uuid = executor.submit(
        run_handshake, receiver_uuid, test_output_dir, test_input_dir, False
    )

    assert initiator_other_uuid.result() == receiver_uuid
    assert receiver_other_uuid.result() == initiator_uuid
