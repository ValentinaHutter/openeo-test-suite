from stac_validator import stac_validator

def validate_stac_dict(collection_dict: dict):
    stac = stac_validator.StacValidate()
    is_valid_stac = stac.validate_dict(collection_dict)
    if not is_valid_stac:
        raise ValueError(stac.message)