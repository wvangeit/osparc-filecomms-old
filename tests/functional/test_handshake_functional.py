import pathlib as pl
import concurrent.futures as futures
import uuid

import handshakes


this_dir = pl.Path(__file__).parent
test_input_dir = this_dir / "test_input_dir"
test_output_dir = this_dir / "test_output_dir"


def run_handshake(self_uuid, is_initiator):
    input_dir_path = test_input_dir if is_initiator else test_output_dir
    output_dir_path = test_output_dir if is_initiator else test_input_dir
    handshake = handshakes.FileHandshake(
        self_uuid, input_dir_path, output_dir_path, is_initiator
    )
    other_uuid = handshake.shake()

    return other_uuid


def test_handshakes_functional():
    initiator_uuid = uuid.uuid4()
    receiver_uuid = uuid.uuid4()

    executor = futures.ProcessPoolExecutor(max_workers=2)
    initiator_other_uuid = executor.submit(run_handshake, True, initiator_uuid)
    receiver_other_uuid = executor.submit(run_handshake, False, receiver_uuid)

    assert initiator_other_uuid.result() == receiver_uuid
    assert receiver_other_uuid.result() == initiator_uuid
