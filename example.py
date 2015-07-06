from parser import loads


if __name__ == '__main__':
    # a simple test
    # example below is from http://json.org/example
    example = '''{
            "title": "example glossary",
            "GlossDiv": {
                "title": "S",
                "GlossList": {
                    "GlossEntry": {
                        "ID": "SGML",
                        "SortAs": "SGML",
                        "GlossTerm": "Standard Generalized Markup Language",
                        "Acronym": "SGML",
                        "Abbrev": "ISO 8879:1986",
                        "GlossDef": {
                            "para": "A meta-markup language, used to create markup languages such as DocBook.",
                            "GlossSeeAlso": ["GML", "XML"]
                            },
                        "GlossSee": "markup"
                        }
                    }
                }
            }
    '''
    import json
    assert cmp(loads(example), json.loads(example)) == 0
