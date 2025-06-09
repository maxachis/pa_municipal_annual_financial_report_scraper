from report_creator.models.average import AverageRow


class AverageWithPopRow(AverageRow):
    pop_estimate: int
    pop_margin: int
    urban_rural: str
    class_: str
