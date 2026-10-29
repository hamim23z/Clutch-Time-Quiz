from matchnorm import base_name, normalize


def test_normalize_matches_the_websites_rules():
    cases = {
        "Nenê": "nene", "Amar'e Stoudemire": "amare stoudemire", "Shai Gilgeous-Alexander": "shai gilgeous alexander",
        "J. J. Barea": "jj barea", "J.J. Barea": "jj barea", "JJ Barea": "jj barea", "Jimmy   Butler": "jimmy butler",
        "D-Wade": "d wade", "AK-47": "ak 47", "Dončić": "doncic",
    }
    for text, want in cases.items():
        assert normalize(text) == want, text


def test_suffixes_are_dropped_only_when_asked():
    assert normalize("Jimmy Butler III") == "jimmy butler iii"
    assert normalize("Jimmy Butler III", True) == "jimmy butler"
    assert normalize("Gary Payton II", True) == "gary payton"
    assert normalize("V", True) == "v"  # a lone token is never dropped


def test_base_name_drops_the_disambiguator():
    assert base_name("Mike James (2002-2014)") == "Mike James"
    assert base_name("Tony Mitchell (2014, id 2489010)") == "Tony Mitchell"
    assert base_name("Allen Iverson") == "Allen Iverson"
