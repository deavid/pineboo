import unittest
from pineboolib.loader.main import init_testing


class TestPNCompoundKeyFromTableMetaData(unittest.TestCase):
    """Test string field."""

    @classmethod
    def setUpClass(cls) -> None:
        """Ensure pineboo is initialized for testing."""
        init_testing()

    def test_basic(self) -> None:
        """Test check that the data is correct in a compound key."""
        from pineboolib.application import project

        mtd = project.conn.manager().metadata("flseqs")
        if mtd is None:
            raise Exception
        field_1 = mtd.field("campo")
        if field_1 is None:
            raise Exception

        self.assertEqual(field_1.name(), "campo")
        self.assertEqual(field_1.isCompoundKey(), True)

        ck_list = mtd.fieldListOfCompoundKey("campo")
        if ck_list is None:
            raise Exception
        self.assertEqual(len(ck_list), 1)
        self.assertEqual(ck_list[0].name(), "campo")


class TestGeneratePNCompoundKey(unittest.TestCase):
    """Test string field."""

    @classmethod
    def setUpClass(cls) -> None:
        """Ensure pineboo is initialized for testing."""
        init_testing()

    def test_basic(self) -> None:
        """Test create a composite key and check its values."""
        from pineboolib.application import project
        from pineboolib.application.metadata.pncompoundkeymetadata import PNCompoundKeyMetaData

        mtd = project.conn.manager().metadata("flfiles")
        if mtd is None:
            raise Exception

        field_1 = mtd.field("sha")
        field_2 = mtd.field("contenido")
        if field_1 is None:
            raise Exception
        if field_2 is None:
            raise Exception
        ck_mtd_1 = PNCompoundKeyMetaData()
        ck_mtd_1.addFieldMD(field_1)
        ck_mtd_1.addFieldMD(field_2)
        field_list_1 = ck_mtd_1.fieldList()

        ck_mtd_2 = PNCompoundKeyMetaData(ck_mtd_1)  # Copy

        field_list_2 = ck_mtd_2.fieldList()

        self.assertEqual(len(field_list_1), 2)
        self.assertEqual(len(field_list_2), 2)
        self.assertEqual(ck_mtd_2.hasField("sha"), True)
        self.assertEqual(ck_mtd_2.hasField("other"), False)


if __name__ == "__main__":
    unittest.main()
