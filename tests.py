from parse_csv import ParseCsv

p1 = ParseCsv(filename='data.csv', headers=True)

def test_remove_irrelevant_records():
    input_list_records = [
        ['https://groceries.morrisons.com/browse', 'THE BEST', '178974', 'https://groceries.morrisons.com/browse/178974', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', '', '', '']]

    output_list_records = p1.remove_irrelevant_records(input_list_records)

    assert len(output_list_records) == 1, "Bad record not filtered"


def test_create_final_list():
    filtered_records =[[['THE BEST', '178974', 'https://groceries.morrisons.com/browse/178974'],
                        ['FRESH', '178969', 'https://groceries.morrisons.com/browse/178974/178969'],
                        ['CHEESE', '178975', 'https://groceries.morrisons.com/browse/178974/178969/178975']]]

    actual_output = p1.create_final_list(filtered_records)

    expected_output =[{'label': 'THE BEST', 'id': '178974', 'url': 'https://groceries.morrisons.com/browse/178974',
                       'children': [
                           {'label': 'FRESH', 'id': '178969', 'url': 'https://groceries.morrisons.com/browse/178974/178969',
                            'children': [
                                {'label': 'CHEESE', 'id': '178975', 'url': 'https://groceries.morrisons.com/browse/178974/178969/178975'}
                            ]
                           }
                       ]
                       }
                      ]

    assert actual_output == expected_output, "mapping incorrect"


