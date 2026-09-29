"""Static reference data: the African Union's 55 member states, by ISO 3166-1
alpha-3 code. Used to filter global datasets down to the continent without
depending on a fuzzy name match (country names vary across sources)."""

AFRICAN_COUNTRIES: dict[str, str] = {
    "DZA": "Algeria", "AGO": "Angola", "BEN": "Benin", "BWA": "Botswana",
    "BFA": "Burkina Faso", "BDI": "Burundi", "CPV": "Cape Verde",
    "CMR": "Cameroon", "CAF": "Central African Republic", "TCD": "Chad",
    "COM": "Comoros", "COG": "Congo", "COD": "Democratic Republic of Congo",
    "DJI": "Djibouti", "EGY": "Egypt", "GNQ": "Equatorial Guinea",
    "ERI": "Eritrea", "SWZ": "Eswatini", "ETH": "Ethiopia", "GAB": "Gabon",
    "GMB": "Gambia", "GHA": "Ghana", "GIN": "Guinea", "GNB": "Guinea-Bissau",
    "CIV": "Cote d'Ivoire", "KEN": "Kenya", "LSO": "Lesotho", "LBR": "Liberia",
    "LBY": "Libya", "MDG": "Madagascar", "MWI": "Malawi", "MLI": "Mali",
    "MRT": "Mauritania", "MUS": "Mauritius", "MAR": "Morocco",
    "MOZ": "Mozambique", "NAM": "Namibia", "NER": "Niger", "NGA": "Nigeria",
    "RWA": "Rwanda", "STP": "Sao Tome and Principe", "SEN": "Senegal",
    "SYC": "Seychelles", "SLE": "Sierra Leone", "SOM": "Somalia",
    "ZAF": "South Africa", "SSD": "South Sudan", "SDN": "Sudan",
    "TZA": "Tanzania", "TGO": "Togo", "TUN": "Tunisia", "UGA": "Uganda",
    "ZMB": "Zambia", "ZWE": "Zimbabwe", "ESH": "Western Sahara",
}
