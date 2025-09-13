

def extract_county_name(name: str) -> str:
    return name.split(",")[1].strip()

def extract_municipality_name(name: str) -> str:
    return name.split(",")[0].strip()