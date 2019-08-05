"""Test_pntablemetadata module."""

import unittest
from pineboolib.loader.main import init_testing


class TestCreatePNTableMetaData(unittest.TestCase):
    """TestCreatePNTableMetaData Class."""

    def test_basic(self) -> None:
        """Test create a PNTableMetaData."""

        from pineboolib.application.metadata.pntablemetadata import PNTableMetaData

        mtd = PNTableMetaData("prueba_1", "Alias de prueba_1", "qry_prueba_1")

        self.assertEqual(mtd.name(), "prueba_1")
        self.assertEqual(mtd.alias(), "Alias de prueba_1")
        self.assertEqual(mtd.isQuery(), True)

        mtd.setName("prueba_2")
        mtd.setAlias("Alias de prueba_2")
        mtd.setQuery("qry_prueba_2")

        self.assertEqual(mtd.query(), "qry_prueba_2")


class TestCopyPNTableMetaData(unittest.TestCase):
    """TestCopyPNTableMetaData Class."""

    @classmethod
    def setUpClass(cls) -> None:
        """Ensure pineboo is initialized for testing."""
        init_testing()

    def test_basic(self) -> None:
        """Test copy a PNTableMetaData from other."""

        from pineboolib.application.metadata.pntablemetadata import PNTableMetaData
        from pineboolib.application import project

        mtd_1 = project.conn.manager().metadata("flgroups")

        mtd_2 = PNTableMetaData(mtd_1)

        self.assertEqual(mtd_2.name(), "flgroups")
        self.assertEqual(mtd_2.alias(), "Grupos de Usuarios")
        self.assertEqual(mtd_2.fieldNameToAlias("idgroup"), "Nombre")
        self.assertEqual(mtd_2.primaryKey(), "idgroup")
        self.assertEqual(mtd_2.fieldAliasToName("Nombre"), "idgroup")


class TestPNTableMetaData(unittest.TestCase):
    """TestPNTableMetaData Class."""

    @classmethod
    def setUpClass(cls) -> None:
        """Ensure pineboo is initialized for testing."""
        init_testing()

    def test_basic(self) -> None:
        """Test manage a PNTableMetaData."""

        from pineboolib.application import project

        mtd = project.conn.manager().metadata("flgroups")
        mtd_2 = project.conn.manager().metadata("flareas")
        if mtd is None:
            raise Exception
        if mtd_2 is None:
            raise Exception
        self.assertEqual(mtd.fieldType("descripcion"), 3)
        self.assertEqual(mtd.fieldIsPrimaryKey("descripcion"), False)
        self.assertEqual(mtd.fieldIsPrimaryKey("idgroup"), True)
        self.assertEqual(mtd.fieldIsIndex("descripcion"), 1)
        self.assertEqual(mtd.fieldLength("descripcion"), 100)
        self.assertEqual(mtd.fieldPartInteger("descripcion"), 4)
        self.assertEqual(mtd.fieldPartDecimal("descripcion"), 0)
        self.assertEqual(mtd.fieldCalculated("descripcion"), False)
        self.assertEqual(mtd.fieldVisible("descripcion"), True)

        field = mtd.field("descripcion")
        if field is None:
            raise Exception
        self.assertEqual(field.name(), "descripcion")

        field_list = mtd.fieldList()
        self.assertEqual(len(field_list), 2)

        field_list_2 = mtd.fieldListArray(False)
        self.assertEqual(field_list_2, ["idgroup", "descripcion"])

        field_list_3 = mtd.fieldListArray(True)
        self.assertEqual(field_list_3, ["flgroups.idgroup", "flgroups.descripcion"])

        mtd.removeFieldMD("descripcion")
        self.assertEqual(mtd.fieldIsIndex("descripcion"), -1)
        self.assertEqual(mtd.fieldIsUnique("idgroup"), False)

        self.assertEqual(mtd.indexPos("idgroup"), 0)
        self.assertEqual(mtd.fieldNames(), ["idgroup"])
        self.assertEqual(mtd_2.fieldNamesUnlock(), ["bloqueo"])

        self.assertEqual(mtd.concurWarn(), False)
        mtd.setConcurWarn(True)
        self.assertEqual(mtd.concurWarn(), True)

        self.assertEqual(mtd.detectLocks(), False)
        mtd.setDetectLocks(True)
        self.assertEqual(mtd.detectLocks(), True)

        self.assertEqual(mtd.FTSFunction(), "")
        mtd.setFTSFunction("1234_5678")
        self.assertEqual(mtd.FTSFunction(), "1234_5678")

        self.assertEqual(mtd.inCache(), False)
        mtd.setInCache(True)
        self.assertEqual(mtd.inCache(), True)

        field_pos_0 = mtd.indexFieldObject(0)
        self.assertEqual(field_pos_0.name(), "idgroup")


class TestRelationsPNTableMetaData(unittest.TestCase):
    """TestRelationsPNTableMetaData Class."""

    @classmethod
    def setUpClass(cls) -> None:
        """Ensure pineboo is initialized for testing."""
        init_testing()

    def test_basic(self) -> None:
        """Test Relations M1 and 1M."""

        from pineboolib.application import project

        mtd_1 = project.conn.manager().metadata("flusers")
        if mtd_1 is None:
            raise Exception
        self.assertEqual(mtd_1.fieldTableM1("idgroup"), "flgroups")
        self.assertEqual(mtd_1.fieldForeignFieldM1("idgroup"), "idgroup")


class TestCompoundKeyPNTableMetaData(unittest.TestCase):
    """TestCompoundKeyPNTableMetaData Class."""

    @classmethod
    def setUpClass(cls) -> None:
        """Ensure pineboo is initialized for testing."""
        init_testing()

    def test_basic(self) -> None:
        """Test CompoundKey."""

        from pineboolib.application import project

        mtd = project.conn.manager().metadata("flseqs")
        if mtd is None:
            raise Exception
        field_list = mtd.fieldListOfCompoundKey("campo")
        if field_list is None:
            raise Exception
        self.assertEqual(field_list[0].name(), "campo")


if __name__ == "__main__":
    unittest.main()
