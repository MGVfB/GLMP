# GLMP: Build manifesto metadata from filenames
# Final parser: the Excel sheet "Parteien" is the master reference for
# legacy party abbreviations. The manifesto text is NEVER used to guess a party.
#
# Put this script in the root of the local GLMP repository.
# Run from the repository root:
#   python build_manifestos_metadata.py
#
# Inputs:
#   metadata/source/Abkürzungen Städte & Parteien.xlsx
#   metadata/source/city_lookup.csv
#   metadata/source/local_cities.csv
#   manifestos/*.txt
#
# Outputs:
#   metadata/manifestos.csv
#   metadata/unmatched_manifestos.csv

from pathlib import Path
import hashlib
import re
import unicodedata
import pandas as pd

ROOT = Path(__file__).resolve().parent
MANIFESTO_DIR = ROOT / "manifestos"
SOURCE_DIR = ROOT / "metadata" / "source"
OUTPUT_DIR = ROOT / "metadata"

CITY_XLSX = SOURCE_DIR / "Abkürzungen Städte & Parteien.xlsx"
CITY_LOOKUP = SOURCE_DIR / "city_lookup.csv"
LOCAL_CITIES = SOURCE_DIR / "local_cities.csv"
OUTPUT = OUTPUT_DIR / "manifestos.csv"
UNMATCHED = OUTPUT_DIR / "unmatched_manifestos.csv"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def norm(s):
    s = str(s).strip().lower().replace("ß", "ss")
    s = s.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue")
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[^a-z0-9]+", "_", s)
    return s.strip("_")


def norm_simple(s):
    s = str(s).strip().lower().replace("ß", "ss")
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[^a-z0-9]+", "_", s)
    return s.strip("_")


def stable_id(filename):
    digest = hashlib.sha1(filename.encode("utf-8")).hexdigest()[:10].upper()
    return f"GLMP-{digest}"


def year_from_2digit(yy):
    yy = int(yy)
    return 2000 + yy if yy <= 24 else 1900 + yy


def clean_cell(value):
    if pd.isna(value):
        return ""
    return str(value).strip()


def load_sources():
    cities_x = pd.read_excel(CITY_XLSX, sheet_name="Städte")
    parties_x = pd.read_excel(CITY_XLSX, sheet_name="Parteien")

    cities_x = cities_x[["Stadt", "Abkürzung", "Bundesland"]].dropna(
        subset=["Stadt", "Abkürzung"]
    ).copy()

    parties_x = parties_x[["Partei", "Abkürzung", "Vorgänger", "Kommentar", "Legende"]].copy()
    parties_x["Partei"] = parties_x["Partei"].map(clean_cell)
    parties_x["Abkürzung"] = parties_x["Abkürzung"].map(clean_cell).str.lower()
    parties_x = parties_x[parties_x["Partei"] != ""].copy()

    local = pd.read_csv(LOCAL_CITIES, sep=";")
    local = local.dropna(subset=["city"]).copy()

    lookup = pd.read_csv(CITY_LOOKUP, sep=";")
    lookup = lookup.dropna(subset=["abbrev", "city_full"]).copy()

    city_info = {}
    for _, r in local.iterrows():
        city = clean_cell(r["city"])
        city_info[city] = {
            "state": clean_cell(r["state_name"]) or None,
            "inhabitants_2024": r["inhabitants_2024"] if "inhabitants_2024" in r else None,
        }

    for _, r in cities_x.iterrows():
        city = clean_cell(r["Stadt"])
        city_info.setdefault(city, {})
        city_info[city]["state"] = clean_cell(r["Bundesland"]) or city_info[city].get("state")

    for _, r in lookup.iterrows():
        city = clean_cell(r["city_full"])
        city_info.setdefault(city, {})

    city_alias = {}
    for city in city_info:
        city_alias[norm(city)] = city
        city_alias[norm_simple(city)] = city

    city_abbrev = {}
    for _, r in cities_x.iterrows():
        city_abbrev[clean_cell(r["Abkürzung"]).lower()] = clean_cell(r["Stadt"])
    for _, r in lookup.iterrows():
        ab = clean_cell(r["abbrev"]).lower()
        city = clean_cell(r["city_full"])
        city_abbrev.setdefault(ab, city)

    # Party abbreviations from the Excel sheet are the authoritative source.
    party_abbrev = {}
    party_name = {}
    party_abbr_by_name = {}
    for _, r in parties_x.iterrows():
        party = clean_cell(r["Partei"])
        abbr = clean_cell(r["Abkürzung"]).lower()
        if not party:
            continue
        party_name.setdefault(norm(party), party)
        party_name.setdefault(norm_simple(party), party)
        if abbr:
            party_abbrev.setdefault(abbr, []).append(party)
            party_abbr_by_name.setdefault(norm(party), abbr)
            party_abbr_by_name.setdefault(norm_simple(party), abbr)

    # De-duplicate candidates while preserving Excel order.
    for abbr, candidates in party_abbrev.items():
        party_abbrev[abbr] = list(dict.fromkeys(candidates))

    return city_info, city_alias, city_abbrev, party_abbrev, party_name, party_abbr_by_name


def city_mentions_in_party(party, all_cities):
    """Return municipalities explicitly indicated by a party label.

    Besides the full city name, allow distinctive city-name components. This
    handles labels such as "Bunte Linke Heidelberg" for the municipality
    "Heidelberg" and adjectival forms such as "Aachener-Bürger-Liste" for
    "Aachen". Only components of at least five letters are considered, to
    avoid accidental matches on short/common words.
    """
    p = norm_simple(party).replace("_", " ")
    hits = []
    for city in all_cities:
        c = norm_simple(city).replace("_", " ")
        if not c:
            continue
        if c in p:
            hits.append(city)
            continue
        city_tokens = [t for t in c.split() if len(t) >= 5]
        party_tokens = set(re.findall(r"[a-z0-9]+", p))
        if any(t in party_tokens for t in city_tokens):
            hits.append(city)
            continue
        # Prefix match covers adjectival forms such as Aachen -> Aachener.
        if any(any(pt.startswith(t) or t.startswith(pt) for pt in party_tokens if len(pt) >= 5)
               for t in city_tokens):
            hits.append(city)
    return list(dict.fromkeys(hits))



# Explicit legacy exceptions that are not covered by the Excel party master.
# These are documented corpus-specific mappings; the manifesto text is not
# searched automatically by the parser.
LEGACY_PARTY_OVERRIDES = {
    "ha09hak": "Hagen Aktiv",
    "st14sos": "SÖS (Stuttgart Ökologisch Sozial)",
    "bh19bge": "Bündnis Grundeinkommen",
    "bh19dih": "Die Humanisten",
    "bh19veg": "V-Partei³",
    "ch19prc": "Pro Chemnitz",
    "ef19mws": "Mehrwertstadt Erfurt",
    "hd19dhd": "Die Heidelberger",
    "hd19hib": "Heidelberg in Bewegung",
    "ma19mal": "Freie Wähler – Mannheimer Liste (ML)",
    "po19ich": "Ich",
    "rt19guu": "Die Grünen und Unabhängigen",
    "st19sos": "SÖS (Stuttgart Ökologisch Sozial)",
    "au20aib": "Augsburg in Bürgerhand",
    "au20aux": "Generation Aux",
    "au20wsa": "Wir sind Augsburg",
    "bo20npd": "NPD",
    "do20baj": "Basisdemokratie jetzt in Dortmund",
    "do20bvt": "Bündnis für Vielfalt und Toleranz",
    "do20dos": "Digital Ökologisch Sozial",
    "du20aud": "Aufbruch Duisburg",
    "du20bdd": "BIG-DERGAH Wahlbündnis Duisburg",
    "ge20aug": "AUF Gelsenkirchen",
    "gt20bfg": "BfGT – Bürger für Gütersloh",
    "ha20hak": "Hagen Aktiv",
    "he20wwh": "Wählergemeinschaft Wanne-Herne",
    "in20udi": "Unabhängige Demokraten Ingolstadts",
    "ko20kli": "Klima Freunde Köln",
    "kr20wuz": "Wählergemeinschaft Unsere Zukunft",
    "le20lpp": "Leverkusener Liste",
    "mo20fbm": "Freie Bürgerliste Moers",
    "mh20bam": "Bürgerlicher Aufbruch Mülheim an der Ruhr",
    "mu20mul": "Münchner Liste",
    "mu20mut": "mut",
    "mu20rlm": "Rosa Liste München",
    "ms20mib": "Münster ist bunt und international",
    "ne20dzp": "Deutsche Zentrumspartei",
    "ne20tsh": "Tierschutzpartei",
    "nu20lil": "Die aNDERE",
    "ob20vio": "Die Violetten",
    "re20phd": "Die Holisten",
    "rg20brk": "Brücke – Ideen verbinden Menschen e.V.",
    "sg20abi": "Alternative Bürgerinitiative (ABI)",
}

# Cases whose exact party name is not sufficiently supported by the currently
# available reference material remain unknown rather than being guessed.

def resolve_party(raw_abbr, city, party_abbrev, all_cities):
    """Resolve a legacy abbreviation using only the Excel party master.

    Resolution order:
      1. unique abbreviation -> exact Excel party
      2. among duplicates, exact municipality named in party label
      3. among duplicates, exclude candidates explicitly tied to another city;
         if one generic candidate remains, use it
      4. otherwise leave ambiguous; never guess from manifesto text
    """
    raw_abbr = clean_cell(raw_abbr).lower()

    # Special local naming convention: files using the abbreviation "pro"
    # denote the local list "Pro + municipality" (e.g. au20pro -> Pro Augsburg).
    # This is a corpus-wide naming rule and therefore takes precedence over
    # the duplicate generic "pro" entries in the Excel party sheet.
    if raw_abbr == "pro" and city:
        return f"Pro {city}", raw_abbr, "ok"

    candidates = party_abbrev.get(raw_abbr, [])

    if len(candidates) == 1:
        return candidates[0], raw_abbr, "ok"

    if len(candidates) == 0:
        return None, raw_abbr, "unknown_party"

    city_norm = norm_simple(city).replace("_", " ") if city else ""

    # First: a candidate explicitly names the municipality.
    exact_city = []
    for p in candidates:
        mentions = city_mentions_in_party(p, all_cities)
        if city and any(norm_simple(c).replace("_", " ") == city_norm for c in mentions):
            exact_city.append(p)
    if len(exact_city) == 1:
        return exact_city[0], raw_abbr, "ok"

    # Second: remove candidates that explicitly name a different municipality.
    generic_or_same = []
    for p in candidates:
        mentions = city_mentions_in_party(p, all_cities)
        if not mentions:
            generic_or_same.append(p)
        elif city and any(norm_simple(c).replace("_", " ") == city_norm for c in mentions):
            generic_or_same.append(p)

    if len(generic_or_same) == 1:
        return generic_or_same[0], raw_abbr, "ok"

    return " | ".join(candidates), raw_abbr, "ambiguous_party"


def resolve_city(raw_city, city_alias):
    if not raw_city:
        return None
    return city_alias.get(norm(raw_city)) or city_alias.get(norm_simple(raw_city))



def resolve_legacy_override(stem, city, party_abbrev):
    key = stem.lower()
    party = LEGACY_PARTY_OVERRIDES.get(key)
    if party:
        # Keep the historical filename abbreviation as the machine-readable
        # abbreviation; the party label is the controlled canonical label.
        pabbr = key[4:] if re.fullmatch(r"[a-z]{2}\d{2}[a-z0-9]+", key) else key
        if re.fullmatch(r"[a-z]{2}gp[a-z0-9]+", key):
            pabbr = key[4:]
        return party, pabbr, "ok"
    return None


def parse_legacy(stem, city_info, city_abbrev, party_abbrev, all_cities):
    s = stem.lower()

    # Explicit corpus-specific legacy mappings.
    override = resolve_legacy_override(s, None, party_abbrev)
    if override:
        party, resolved_abbr, status = override
        # Resolve municipality/year from the filename while using the controlled party label.
        m_std = re.fullmatch(r"([a-z]{2})(\d{2})([a-z0-9]+)", s)
        if m_std and m_std.group(1) in city_abbrev:
            cabbr, yy, _ = m_std.groups()
            city = city_abbrev[cabbr]
            return {
                "municipality": city,
                "state": city_info.get(city, {}).get("state"),
                "party": party,
                "party_abbreviation": resolved_abbr,
                "election_year": year_from_2digit(yy),
                "election_type": "local election",
                "document_type": "Wahlprogramm",
                "mapping_method": "legacy_manual_override",
                "mapping_status": status,
                "city_abbreviation": cabbr,
            }

    # Grundsatzprogramm: city + gp + party abbreviation, e.g. acgpfwg.
    # No election year is encoded in this filename convention.
    m = re.fullmatch(r"([a-z]{2})gp([a-z0-9]+)", s)
    if m and m.group(1) in city_abbrev:
        cabbr, pabbr = m.groups()
        city = city_abbrev[cabbr]
        party, resolved_abbr, status = resolve_party(pabbr, city, party_abbrev, all_cities)
        return {
            "municipality": city,
            "state": city_info.get(city, {}).get("state"),
            "party": party,
            "party_abbreviation": resolved_abbr,
            "election_year": None,
            "election_type": "local election",
            "document_type": "Grundsatzprogramm",
            "mapping_method": "legacy_gp_filename",
            "mapping_status": status,
            "city_abbreviation": cabbr,
        }

    # Standard legacy: city + two-digit year + party abbreviation.
    m = re.fullmatch(r"([a-z]{2})(\d{2})([a-z0-9]+)", s)
    if m and m.group(1) in city_abbrev:
        cabbr, yy, pabbr = m.groups()
        city = city_abbrev[cabbr]
        party, resolved_abbr, status = resolve_party(pabbr, city, party_abbrev, all_cities)
        return {
            "municipality": city,
            "state": city_info.get(city, {}).get("state"),
            "party": party,
            "party_abbreviation": resolved_abbr,
            "election_year": year_from_2digit(yy),
            "election_type": "local election",
            "document_type": "Wahlprogramm",
            "mapping_method": "legacy_filename",
            "mapping_status": status,
            "city_abbreviation": cabbr,
        }

    return None


def parse_filename(filename, city_info, city_alias, city_abbrev, party_abbrev, party_name, party_abbr_by_name):
    # Some files have an accidental space before .txt.
    cleaned_filename = re.sub(r"\s+\.txt$", ".txt", filename, flags=re.IGNORECASE)
    stem = Path(cleaned_filename).stem
    all_cities = list(city_info.keys())

    legacy = parse_legacy(stem, city_info, city_abbrev, party_abbrev, all_cities)
    if legacy:
        return legacy

    # Modern format: City_Party_YYYY.txt.
    m = re.fullmatch(r"(.+?)_(.+)_(\d{4})", stem)
    if m:
        city_raw, party_raw, year = m.groups()
        city = resolve_city(city_raw, city_alias)

        # Modern descriptive filenames are authoritative for the party label.
        # If the label is present in the Excel master, canonicalize it and add
        # its abbreviation; otherwise retain the filename label unchanged.
        p = party_name.get(norm(party_raw)) or party_name.get(norm_simple(party_raw))
        if p:
            party = p
            resolved_abbr = party_abbr_by_name.get(norm(party)) or party_abbr_by_name.get(norm_simple(party))
        else:
            party = party_raw.strip()
            resolved_abbr = None

        status = "ok" if city else "unknown_city"
        return {
            "municipality": city,
            "state": city_info.get(city, {}).get("state") if city else None,
            "party": party,
            "party_abbreviation": resolved_abbr,
            "election_year": int(year),
            "election_type": "local election",
            "document_type": "Wahlprogramm",
            "mapping_method": "modern_filename",
            "mapping_status": status,
            "city_abbreviation": None,
        }

    return {
        "municipality": None,
        "state": None,
        "party": None,
        "party_abbreviation": None,
        "election_year": None,
        "election_type": None,
        "document_type": None,
        "mapping_method": None,
        "mapping_status": "unparsed_filename",
        "city_abbreviation": None,
    }


def main():
    required = [MANIFESTO_DIR, CITY_XLSX, CITY_LOOKUP, LOCAL_CITIES]
    for p in required:
        if not p.exists():
            raise SystemExit(f"Required path not found: {p}")

    (city_info, city_alias, city_abbrev, party_abbrev,
     party_name, party_abbr_by_name) = load_sources()

    filenames = sorted(p.name for p in MANIFESTO_DIR.glob("*.txt") if p.is_file())
    rows = []

    for filename in filenames:
        parsed = parse_filename(
            filename, city_info, city_alias, city_abbrev, party_abbrev,
            party_name, party_abbr_by_name
        )
        rows.append({
            "manifesto_id": stable_id(filename),
            "filename": filename,
            "path": f"manifestos/{filename}",
            **parsed,
        })

    new_df = pd.DataFrame(rows)

    # Preserve stable IDs only. Never carry old automated party assignments
    # into a newly parsed dataset.
    if OUTPUT.exists():
        try:
            old = pd.read_csv(OUTPUT)
            if "filename" in old.columns and "manifesto_id" in old.columns:
                old_ids = old[["filename", "manifesto_id"]].drop_duplicates("filename")
                new_df = new_df.drop(columns=["manifesto_id"]).merge(
                    old_ids, on="filename", how="left"
                )
                new_df["manifesto_id"] = new_df["manifesto_id"].fillna(
                    new_df["filename"].map(stable_id)
                )
        except Exception as exc:
            print(f"Warning: could not preserve existing IDs: {exc}")

    cols = [
        "manifesto_id", "filename", "path", "municipality", "state",
        "party", "party_abbreviation", "election_year", "election_type",
        "document_type", "mapping_method", "mapping_status", "city_abbreviation"
    ]
    new_df = new_df[cols].sort_values(
        ["election_year", "municipality", "party", "filename"],
        na_position="last"
    )

    new_df.to_csv(OUTPUT, index=False, encoding="utf-8-sig")
    unmatched = new_df[new_df["mapping_status"] != "ok"].copy()
    unmatched.to_csv(UNMATCHED, index=False, encoding="utf-8-sig")

    print(f"Manifestos found: {len(new_df):,}")
    print(f"Mapped OK: {(new_df.mapping_status == 'ok').sum():,}")
    print(f"Needs review: {(new_df.mapping_status != 'ok').sum():,}")
    print("Status breakdown:")
    print(new_df["mapping_status"].value_counts(dropna=False).to_string())
    print(f"Output: {OUTPUT}")
    print(f"Review file: {UNMATCHED}")


if __name__ == "__main__":
    main()
