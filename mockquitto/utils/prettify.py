from json import JSONEncoder, JSONDecoder


def json_prettifier(jsn_string):
    encoder = JSONEncoder(sort_keys=True, indent=4)
    decoder = JSONDecoder()
    encoded = '\n\t' + '\t'.join(encoder.encode(decoder.decode(jsn_string)).splitlines(True))
    return encoded
