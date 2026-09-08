from .contract_envelope import ContractEnvelope


def map_event(raw: bytes) -> ContractEnvelope:
    envelope = ContractEnvelope.from_json(raw)
    if envelope.message_kind != "event":
        raise ValueError("expected event envelope")
    return envelope
