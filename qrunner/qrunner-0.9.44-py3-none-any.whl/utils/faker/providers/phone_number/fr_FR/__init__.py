from .. import Provider as PhoneNumberProvider


class Provider(PhoneNumberProvider):
    formats = (
        "+33 (0){{area_code_with_separator}} ## ## ##",
        "+33 {{area_code_with_separator}} ## ## ##",
        "0{{area_code_without_separator}}######",
        "0{{area_code_with_separator}} ## ## ##",
    )

    # https://fr.wikipedia.org/wiki/Liste_des_indicatifs_t%C3%A9l%C3%A9phoniques_en_France#Liste_des_indicatifs_d%C3%A9partementaux_fran%C3%A7ais_class%C3%A9s_par_indicatif
    area_codes = (
        # landlines
        "130",
        "134",
        "139",
        "140",
        "141",
        "142",
        "143",
        "144",
        "145",
        "146",
        "147",
        "148",
        "149",
        "153",
        "155",
        "156",
        "158",
        "160",
        "164",
        "169",
        "170",
        "172",
        "173",
        "174",
        "175",
        "176",
        "177",
        "178",
        "179",
        "180",
        "181",
        "182",
        "183",
        "188",
        "214",
        "218",
        "219",
        "221",
        "222",
        "223",
        "228",
        "229",
        "230",
        "231",
        "232",
        "233",
        "234",
        "235",
        "236",
        "237",
        "238",
        "240",
        "241",
        "243",
        "244",
        "245",
        "246",
        "247",
        "248",
        "249",
        "250",
        "251",
        "252",
        "253",
        "254",
        "255",
        "256",
        "257",
        "258",
        "261",
        "262",
        "269",
        "272",
        "276",
        "277",
        "278",
        "279",
        "285",
        "290",
        "296",
        "297",
        "298",
        "299",
        "310",
        "320",
        "321",
        "322",
        "323",
        "324",
        "325",
        "326",
        "327",
        "328",
        "329",
        "339",
        "344",
        "345",
        "351",
        "352",
        "353",
        "354",
        "355",
        "356",
        "357",
        "358",
        "359",
        "360",
        "361",
        "362",
        "363",
        "364",
        "365",
        "366",
        "367",
        "368",
        "369",
        "370",
        "371",
        "372",
        "373",
        "375",
        "376",
        "379",
        "380",
        "381",
        "382",
        "383",
        "384",
        "385",
        "386",
        "387",
        "388",
        "389",
        "390",
        "411",
        "413",
        "415",
        "420",
        "422",
        "423",
        "426",
        "427",
        "430",
        "432",
        "434",
        "437",
        "438",
        "442",
        "443",
        "444",
        "449",
        "450",
        "456",
        "457",
        "458",
        "463",
        "465",
        "466",
        "467",
        "468",
        "469",
        "470",
        "471",
        "472",
        "473",
        "474",
        "475",
        "476",
        "477",
        "478",
        "479",
        "480",
        "481",
        "482",
        "483",
        "484",
        "485",
        "486",
        "487",
        "488",
        "489",
        "490",
        "491",
        "492",
        "493",
        "494",
        "495",
        "497",
        "498",
        "499",
        "58 ",
        "516",
        "517",
        "518",
        "519",
        "524",
        "531",
        "532",
        "533",
        "534",
        "535",
        "536",
        "540",
        "545",
        "546",
        "547",
        "549",
        "553",
        "554",
        "555",
        "556",
        "557",
        "558",
        "559",
        "561",
        "562",
        "563",
        "564",
        "565",
        "567",
        "579",
        "581",
        "582",
        "586",
        "587",
        "590",
        "594",
        "596",
        # mobile numbers
        "6##",
        "7##",
        "80#",
    )

    def area_code_without_separator(self) -> str:
        return self.numerify(self.random_element(self.area_codes))

    def area_code_with_separator(self) -> str:
        area_code: str = self.random_element(self.area_codes)
        return self.numerify(f"{area_code[0]} {area_code[1:]}")

    def phone_number(self) -> str:
        pattern: str = self.random_element(self.formats)
        return self.numerify(self.generator.parse(pattern))
