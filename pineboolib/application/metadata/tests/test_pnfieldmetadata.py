import unittest
from pineboolib.loader.main import init_testing


class TestStringField(unittest.TestCase):
    """Test string field"""

    @classmethod
    def setUpClass(cls) -> None:
        """Ensure pineboo is initialized for testing."""
        init_testing()

    def test_basic(self) -> None:
        """Test collect a field from the pntablemetadata flmodules and check the values"""

        from pineboolib.application import project

        mtd = project.conn.manager().metadata("flmodules")
        field = mtd.field("version")

        self.assertNotEqual(field, None)
        self.assertEqual(field.name(), "version")
        self.assertEqual(field.isPrimaryKey(), False)
        self.assertEqual(field.isCompoundKey(), False)
        self.assertEqual(field.length(), 3)
        self.assertEqual(field.allowNull(), False)
        self.assertEqual(field.visibleGrid(), True)
        self.assertEqual(field.visible(), True)
        self.assertEqual(field.editable(), False)
        self.assertEqual(field.defaultValue(), "0.0")
        self.assertEqual(field.regExpValidator(), "[0-9]\\.[0-9]")


class TestUintField(unittest.TestCase):
    """Test uint field"""

    @classmethod
    def setUpClass(cls) -> None:
        """Ensure pineboo is initialized for testing."""
        init_testing()

    def test_basic(self) -> None:
        """Test collect a field from the pntablemetadata flseq and check the values"""

        from pineboolib.application import project

        mtd = project.conn.manager().metadata("flseqs")
        field = mtd.field("seq")

        self.assertNotEqual(field, None)
        self.assertEqual(field.name(), "seq")
        self.assertEqual(field.alias(), "Secuencia")
        self.assertEqual(field.isPrimaryKey(), False)
        self.assertEqual(field.isCompoundKey(), False)
        self.assertEqual(field.length(), 0)
        self.assertEqual(field.allowNull(), False)
        self.assertEqual(field.visibleGrid(), True)
        self.assertEqual(field.visible(), True)
        self.assertEqual(field.editable(), True)
        self.assertEqual(field.defaultValue(), None)
        self.assertEqual(field.regExpValidator(), None)


class TestStringListField(unittest.TestCase):
    """Test string field"""

    @classmethod
    def setUpClass(cls) -> None:
        """Ensure pineboo is initialized for testing."""
        init_testing()

    def test_basic(self) -> None:
        """Test collect a field from the pntablemetadata flsettings and check the values"""

        from pineboolib.application import project

        mtd = project.conn.manager().metadata("flsettings")
        field = mtd.field("valor")

        self.assertNotEqual(field, None)
        self.assertEqual(field.name(), "valor")
        self.assertEqual(field.alias(), "Valor")
        self.assertEqual(field.isPrimaryKey(), False)
        self.assertEqual(field.isCompoundKey(), False)
        self.assertEqual(field.length(), 0)
        self.assertEqual(field.allowNull(), True)
        self.assertEqual(field.visibleGrid(), False)
        self.assertEqual(field.visible(), True)
        self.assertEqual(field.editable(), True)
        self.assertEqual(field.defaultValue(), None)
        self.assertEqual(field.regExpValidator(), None)


class TestPixmapField(unittest.TestCase):
    """Test string field"""

    @classmethod
    def setUpClass(cls) -> None:
        """Ensure pineboo is initialized for testing."""
        init_testing()

    def test_basic(self) -> None:
        """Test collect a field from the pntablemetadata flmodules and check the values"""

        from pineboolib.application import project

        mtd = project.conn.manager().metadata("flmodules")

        field = mtd.field("icono")
        self.assertNotEqual(field, None)
        self.assertEqual(field.name(), "icono")
        self.assertEqual(field.isPrimaryKey(), False)
        self.assertEqual(field.isCompoundKey(), False)
        self.assertEqual(field.length(), 0)
        self.assertEqual(field.allowNull(), True)
        self.assertEqual(field.type(), "pixmap")
        self.assertEqual(field.visibleGrid(), True)
        self.assertEqual(field.visible(), True)
        self.assertEqual(field.editable(), True)
        self.assertEqual(field.defaultValue(), None)


class TestUnlockField(unittest.TestCase):
    """Test string field"""

    @classmethod
    def setUpClass(cls) -> None:
        """Ensure pineboo is initialized for testing."""
        init_testing()

    def test_basic(self) -> None:
        """Test collect a field from the pntablemetadata flmodules and check the values"""

        from pineboolib.application import project

        mtd = project.conn.manager().metadata("flmodules")

        field = mtd.field("bloqueo")
        self.assertNotEqual(field, None)
        self.assertEqual(field.name(), "bloqueo")
        self.assertEqual(field.isPrimaryKey(), False)
        self.assertEqual(field.isCompoundKey(), False)
        self.assertEqual(field.length(), 0)
        self.assertEqual(field.allowNull(), False)
        self.assertEqual(field.type(), "unlock")
        self.assertEqual(field.visibleGrid(), True)
        self.assertEqual(field.visible(), True)
        self.assertEqual(field.editable(), True)
        self.assertEqual(field.defaultValue(), True)
        self.assertEqual(field.regExpValidator(), None)


class TestBoolField(unittest.TestCase):
    """Test string field"""

    @classmethod
    def setUpClass(cls) -> None:
        """Ensure pineboo is initialized for testing."""
        init_testing()

    def test_basic(self) -> None:
        """Test collect a field from the pntablemetadata flmodules and check the values"""

        from pineboolib.application import project

        mtd = project.conn.manager().metadata("flmetadata")

        field = mtd.field("bloqueo")
        self.assertNotEqual(field, None)
        self.assertEqual(field.name(), "bloqueo")
        self.assertEqual(field.alias(), "Tabla bloqueada")
        self.assertEqual(field.isPrimaryKey(), False)
        self.assertEqual(field.isCompoundKey(), False)
        self.assertEqual(field.length(), 0)
        self.assertEqual(field.allowNull(), True)
        self.assertEqual(field.type(), "bool")
        self.assertEqual(field.visibleGrid(), True)
        self.assertEqual(field.visible(), True)
        self.assertEqual(field.editable(), True)
        self.assertEqual(field.defaultValue(), None)
        self.assertEqual(field.regExpValidator(), None)


class TestDateField(unittest.TestCase):
    """Test date field"""

    @classmethod
    def setUpClass(cls) -> None:
        """Ensure pineboo is initialized for testing."""
        init_testing()

    def test_basic(self) -> None:
        """Test collect a field from the pntablemetadata flupdates and check the values"""

        from pineboolib.application import project

        mtd = project.conn.manager().metadata("flupdates")
        field = mtd.field("fecha")

        self.assertNotEqual(field, None)
        self.assertEqual(field.name(), "fecha")
        self.assertEqual(field.alias(), "Fecha")
        self.assertEqual(field.isPrimaryKey(), False)
        self.assertEqual(field.isCompoundKey(), False)
        self.assertEqual(field.length(), 0)
        self.assertEqual(field.type(), "date")
        self.assertEqual(field.allowNull(), False)
        self.assertEqual(field.visibleGrid(), True)
        self.assertEqual(field.visible(), True)
        self.assertEqual(field.editable(), False)
        self.assertEqual(field.defaultValue(), None)
        self.assertEqual(field.regExpValidator(), None)


class TestTimeField(unittest.TestCase):
    """Test date field"""

    @classmethod
    def setUpClass(cls) -> None:
        """Ensure pineboo is initialized for testing."""
        init_testing()

    def test_basic(self) -> None:
        """Test collect a field from the pntablemetadata flupdates and check the values"""

        from pineboolib.application import project

        mtd = project.conn.manager().metadata("flupdates")
        field = mtd.field("hora")

        self.assertNotEqual(field, None)
        self.assertEqual(field.name(), "hora")
        self.assertEqual(field.alias(), "Hora")
        self.assertEqual(field.isPrimaryKey(), False)
        self.assertEqual(field.isCompoundKey(), False)
        self.assertEqual(field.length(), 0)
        self.assertEqual(field.type(), "time")
        self.assertEqual(field.allowNull(), False)
        self.assertEqual(field.visibleGrid(), True)
        self.assertEqual(field.visible(), True)
        self.assertEqual(field.editable(), False)
        self.assertEqual(field.defaultValue(), None)
        self.assertEqual(field.regExpValidator(), None)


class TestDoubleField(unittest.TestCase):
    """Test date field"""

    @classmethod
    def setUpClass(cls) -> None:
        """Ensure pineboo is initialized for testing."""
        init_testing()

    def test_basic(self) -> None:
        """Test collect a field and check the values"""

        from pineboolib.application.metadata.pnfieldmetadata import PNFieldMetaData

        field = PNFieldMetaData(
            "new_double",
            "Nuevo Double",
            False,
            False,
            "double",
            0,
            False,
            True,
            True,
            5,
            8,
            False,
            False,
            False,
            0.01,
            False,
            None,
            True,
            False,
            False,
        )

        self.assertNotEqual(field, None)
        self.assertEqual(field.name(), "new_double")
        self.assertEqual(field.alias(), "Nuevo Double")
        self.assertEqual(field.isPrimaryKey(), False)
        self.assertEqual(field.isCompoundKey(), False)
        self.assertEqual(field.length(), 0)
        self.assertEqual(field.type(), "double")
        self.assertEqual(field.allowNull(), False)
        self.assertEqual(field.visibleGrid(), True)
        self.assertEqual(field.visible(), True)
        self.assertEqual(field.editable(), True)
        self.assertEqual(field.defaultValue(), 0.01)
        self.assertEqual(field.regExpValidator(), None)
        self.assertEqual(field.partInteger(), 5)
        self.assertEqual(field.partDecimal(), 8)


if __name__ == "__main__":
    unittest.main()
