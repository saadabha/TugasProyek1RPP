import rdflib
from rdflib.namespace import RDF, OWL, RDFS
import sys

# Nama file ontologi
ONTOLOGY_FILE = "../Ontologi/dota2_ontology.owl"

# Nama file Prolog ABox yang akan dihasilkan
OUTPUT_FILE = "abox_dota2.pl"

# Namespace dari ontologi
NS_BASE = "http://www.semanticweb.org/dota2-ontology#"
NS = rdflib.Namespace(NS_BASE)

def get_local_name(term):
    """
    Mengambil bagian 'lokal' dari URI atau nilai literal.
    Contoh:
    - URIRef("...#anti_mage") -> "anti_mage"
    - Literal("Magical") -> "magical" (lowercase)
    """
    if isinstance(term, rdflib.URIRef):
        term_str = str(term)
        if '#' in term_str:
            return term_str.split('#')[-1].lower().replace('npc_dota_hero_','')
        return term_str.split('/')[-1].lower().replace('npc_dota_hero_', '')
    elif isinstance(term, rdflib.Literal):
        # Ganti spasi dgn underscore dan buat lowercase
        return str(term).lower().replace(" ", "_") 
    else:
        return str(term).lower()

def format_prolog_fact(predicate, subject, obj):
    """Memformat triple sebagai fakta Prolog: predicate(subject, object)."""
    return f"{predicate}({get_local_name(subject)}, {get_local_name(obj)}).\n"


def convert_ontology():
    """Membaca file OWL dan mengonversinya menjadi ABox Prolog."""
    
    g = rdflib.Graph()
    try:
        g.parse(ONTOLOGY_FILE, format="xml")
        print(f"Berhasil memuat {ONTOLOGY_FILE}")
    except Exception as e:
        print(f"GAGAL memuat file ontologi: {e}", file=sys.stderr)
        return

    g.bind("", NS)

    # Kumpulan untuk menyimpan fakta Prolog
    hero_facts = set()
    attribute_facts = set()
    role_facts = set()
    hero_ability_facts = set()
    ability_facts = set() 
    ability_type_facts = set()
    damage_type_facts = set()

    # 1. Temukan Atribut Utama (:hasPrimaryAttribute)
    print("Mencari Hero dan Atribut...")
    for s, p, o in g.triples((None, NS.hasPrimaryAttribute, None)):
        hero_facts.add(f"hero({get_local_name(s)}).\n")
        attribute_facts.add(format_prolog_fact("primary_attribute", s, o))

    # 2. Temukan Role (:hasRole)
    print("Mencari Role...")
    for s, p, o in g.triples((None, NS.hasRole, None)):
        role_facts.add(format_prolog_fact("has_role", s, o))

    # 3. Temukan Ability Hero (:hasAbility)
    print("Mencari Ability...")
    for s, p, o in g.triples((None, NS.hasAbility, None)):
        hero_ability_facts.add(format_prolog_fact("has_ability", s, o))
        ability_facts.add(o) # Tambahkan 'o' (objek/ability) ke set

    # 4. Temukan Tipe Ability & Damage
    print(f"Mencari detail untuk {len(ability_facts)} ability...")

    for ability_uri in ability_facts:
        # Ambil SEMUA properti untuk ability ini
        for p, o in g.predicate_objects(subject=ability_uri):
            # Ganti NS.abilityType -> NS.hasBehavior
            if p == NS.hasBehavior:
                ability_type_facts.add(format_prolog_fact("ability_type", ability_uri, o))
            
            # Ganti NS.damageType -> NS.hasDamageType
            elif p == NS.hasDamageType:
                damage_type_facts.add(format_prolog_fact("damage_type", ability_uri, o))


    print("\nHASIL DIAGNOSTIK")
    print(f"Ditemukan   {len(hero_facts)} hero (dari 'hasPrimaryAttribute').")
    print(f"Ditemukan   {len(attribute_facts)} fakta 'primary_attribute'.")
    print(f"Ditemukan   {len(role_facts)} fakta 'has_role'.")
    print(f"Ditemukan   {len(hero_ability_facts)} fakta 'has_ability'.")
    print(f"Ditemukan   {len(ability_type_facts)} fakta 'ability_type' (dari 'hasBehavior').")
    print(f"Ditemukan   {len(damage_type_facts)} fakta 'damage_type' (dari 'hasDamageType').")

    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write("% === Fakta Hero ===\n")
            f.writelines(sorted(hero_facts))
            f.write("\n")

            f.write("% Properti: Atribut Utama (hasPrimaryAttribute)\n")
            f.writelines(sorted(attribute_facts))
            f.write("\n")
            
            f.write("% Properti: Role (hasRole)\n")
            f.writelines(sorted(role_facts))
            f.write("\n")

            f.write("% Properti: Kepemilikan Ability (hasAbility)\n")
            f.writelines(sorted(hero_ability_facts))
            f.write("\n")

            f.write("% === Fakta Ability ===\n\n")
            f.write("% Properti: Tipe Ability (abilityType)\n")
            f.writelines(sorted(ability_type_facts))
            f.write("\n")

            f.write("% Properti: Tipe Damage (damageType)\n")
            f.writelines(sorted(damage_type_facts))
            f.write("\n")

        print(f"Konversi selesai! Berhasil.\n")
        print(f"ABox Prolog telah disimpan ke: {OUTPUT_FILE}")

    except Exception as e:
        print(f"Gagal menulis ke file output: {e}", file=sys.stderr)

# --- Jalankan Konverter ---
if __name__ == "__main__":
    convert_ontology()