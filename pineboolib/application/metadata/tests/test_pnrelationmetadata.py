import unittest
from pineboolib.loader.main import init_testing


class TestPNRelationMetaData(unittest.TestCase):
    """TestPNRelationMetaData Class."""

    @classmethod
    def setUpClass(cls) -> None:
        """Ensure pineboo is initialized for testing."""
        init_testing()

    def test_basic(self) -> None:
        """PNRelationMetaData."""

        from pineboolib.application import project

        mtd = project.conn.manager().metadata("flgroups")
        if mtd is None:
            raise Exception
        rel_1 = mtd.relation("idgroup", "idgroup", "flusers")
        rel_2 = mtd.relation("idgroup", "idgroup", "flacs")
        if rel_1 is None:
            raise Exception
        if rel_2 is None:
            raise Exception

        self.assertEqual(rel_1.field(), "idgroup")
        self.assertEqual(rel_2.foreignField(), "idgroup")
        self.assertEqual(rel_2.foreignTable(), "flacs")
        self.assertEqual(rel_2.deleteCascade(), False)
        self.assertEqual(rel_1.cardinality(), "1M")


class TestCreatePNRelationMetaData(unittest.TestCase):
    """TestCreatePNRelationMetaData Class."""

    def test_basic(self) -> None:
        """PNRelationMetaData."""

        from pineboolib.application import project
        from pineboolib.application.metadata.pnrelationmetadata import PNRelationMetaData

        mtd = project.conn.manager().metadata("flgroups")
        if mtd is None:
            raise Exception
        rel_1 = mtd.relation("idgroup", "idgroup", "flusers")
        rel_2 = PNRelationMetaData(rel_1)
        rel_3 = PNRelationMetaData("flgroups", "idgroup", "M1", True, True, False)

        self.assertEqual(rel_2.foreignField(), "idgroup")
        self.assertEqual(rel_2.foreignTable(), "flusers")

        rel_3.setField("new_field")

        self.assertEqual(rel_3.field(), "new_field")
        self.assertEqual(rel_3.foreignField(), "idgroup")
        self.assertEqual(rel_3.cardinality(), "M1")
        self.assertEqual(rel_3.deleteCascade(), True)
        self.assertEqual(rel_3.updateCascade(), True)
        self.assertEqual(rel_3.checkIn(), False)


if __name__ == "__main__":
    unittest.main()
