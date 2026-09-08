from .contract_envelope import ContractEnvelope


def map_command(raw: bytes) -> ContractEnvelope:
    envelope = ContractEnvelope.from_json(raw)
    if envelope.message_kind != "command":
        raise ValueError("expected command envelope")
    return envelope
