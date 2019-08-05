import unittest
from pineboolib.loader.main import init_testing


class TestStringField(unittest.TestCase):
    """Test string field."""

    @classmethod
    def setUpClass(cls) -> None:
        """Ensure pineboo is initialized for testing."""
        init_testing()

    def test_basic(self) -> None:
        """Test collect a field from the pntablemetadata flmodules and check the values"""

        from pineboolib.application import project

        mtd = project.conn.manager().metadata("flmodules")
        if mtd is None:
            raise Exception
        field = mtd.field("version")
        if field is None:
            raise Exception

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

        assign_value_1 = field.formatAssignValue("version", "a.1", False)
        assign_value_2 = field.formatAssignValue("version", "b.1", True)
        self.assertEqual(assign_value_1, "version = 'a.1'")
        self.assertEqual(assign_value_2, "upper(version) = 'B.1'")


class TestCopyField(unittest.TestCase):
    """Test Copy a field."""

    @classmethod
    def setUpClass(cls) -> None:
        """Ensure pineboo is initialized for testing."""
        init_testing()

    def test_basic(self) -> None:
        """Test copy a field data from another."""

        from pineboolib.application import project
        from pineboolib.application.metadata.pnfieldmetadata import PNFieldMetaData

        mtd = project.conn.manager().metadata("flmodules")
        if mtd is None:
            raise Exception
        field_1 = mtd.field("version")

        field_2 = PNFieldMetaData(field_1)

        self.assertNotEqual(field_2, None)
        self.assertEqual(field_2.name(), "version")
        self.assertEqual(field_2.isPrimaryKey(), False)
        self.assertEqual(field_2.isCompoundKey(), False)
        self.assertEqual(field_2.length(), 3)
        self.assertEqual(field_2.allowNull(), False)
        self.assertEqual(field_2.visibleGrid(), True)
        self.assertEqual(field_2.visible(), True)
        self.assertEqual(field_2.editable(), False)
        self.assertEqual(field_2.defaultValue(), "0.0")
        self.assertEqual(field_2.regExpValidator(), "[0-9]\\.[0-9]")


class TestUintField(unittest.TestCase):
    """Test uint field."""

    @classmethod
    def setUpClass(cls) -> None:
        """Ensure pineboo is initialized for testing."""
        init_testing()

    def test_basic(self) -> None:
        """Test collect a field from the pntablemetadata flseq and check the values"""

        from pineboolib.application import project

        mtd = project.conn.manager().metadata("flseqs")
        if mtd is None:
            raise Exception
        field = mtd.field("seq")
        if field is None:
            raise Exception

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

        assign_value = field.formatAssignValue("seq", 666, False)

        self.assertEqual(assign_value, "seq = 666")

        table_metadata = field.metadata()
        if table_metadata is None:
            raise Exception
        self.assertEqual(table_metadata.name(), "flseqs")


class TestStringListField(unittest.TestCase):
    """Test stringlist field."""

    @classmethod
    def setUpClass(cls) -> None:
        """Ensure pineboo is initialized for testing."""
        init_testing()

    def test_basic(self) -> None:
        """Test collect a field from the pntablemetadata flsettings and check the values"""

        from pineboolib.application import project

        mtd = project.conn.manager().metadata("flsettings")
        if mtd is None:
            raise Exception
        field = mtd.field("valor")
        if field is None:
            raise Exception

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
        self.assertEqual(field.flDecodeType("stringlist"), "string")


class TestPixmapField(unittest.TestCase):
    """Test pixmap field."""

    @classmethod
    def setUpClass(cls) -> None:
        """Ensure pineboo is initialized for testing."""
        init_testing()

    def test_basic(self) -> None:
        """Test collect a field from the pntablemetadata flmodules and check the values"""

        from pineboolib.application import project

        mtd = project.conn.manager().metadata("flmodules")
        if mtd is None:
            raise Exception

        field = mtd.field("icono")
        if field is None:
            raise Exception

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
        self.assertEqual(field.flDecodeType("pixmap"), "string")


class TestUnlockField(unittest.TestCase):
    """Test unlock field."""

    @classmethod
    def setUpClass(cls) -> None:
        """Ensure pineboo is initialized for testing."""
        init_testing()

    def test_basic(self) -> None:
        """Test collect a field from the pntablemetadata flmodules and check the values"""

        from pineboolib.application import project

        mtd = project.conn.manager().metadata("flmodules")
        if mtd is None:
            raise Exception

        field = mtd.field("bloqueo")
        if field is None:
            raise Exception
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
        self.assertEqual(field.flDecodeType("unlock"), "bool")


class TestBoolField(unittest.TestCase):
    """Test bool field."""

    @classmethod
    def setUpClass(cls) -> None:
        """Ensure pineboo is initialized for testing."""
        init_testing()

    def test_basic(self) -> None:
        """Test collect a field from the pntablemetadata flmetadata and check the values"""

        from pineboolib.application import project

        mtd = project.conn.manager().metadata("flmetadata")
        if mtd is None:
            raise Exception

        field = mtd.field("bloqueo")
        if field is None:
            raise Exception
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
        self.assertEqual(field.flDecodeType("bool"), "bool")


class TestDateField(unittest.TestCase):
    """Test date field."""

    @classmethod
    def setUpClass(cls) -> None:
        """Ensure pineboo is initialized for testing."""
        init_testing()

    def test_basic(self) -> None:
        """Test collect a field from the pntablemetadata flupdates and check the values"""

        from pineboolib.application import project

        mtd = project.conn.manager().metadata("flupdates")
        if mtd is None:
            raise Exception
        field = mtd.field("fecha")
        if field is None:
            raise Exception

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
        self.assertEqual(field.flDecodeType("date"), "date")


class TestTimeField(unittest.TestCase):
    """Test time field."""

    @classmethod
    def setUpClass(cls) -> None:
        """Ensure pineboo is initialized for testing."""
        init_testing()

    def test_basic(self) -> None:
        """Test collect a field from the pntablemetadata flupdates and check the values"""

        from pineboolib.application import project

        mtd = project.conn.manager().metadata("flupdates")
        if mtd is None:
            raise Exception
        field = mtd.field("hora")
        if field is None:
            raise Exception

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
        self.assertEqual(field.flDecodeType("time"), "time")


class TestDoubleField(unittest.TestCase):
    """Test double field."""

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
        self.assertEqual(field.flDecodeType("double"), "double")


class TestOptionsListField(unittest.TestCase):
    """Test string field with optionsList."""

    @classmethod
    def setUpClass(cls) -> None:
        """Ensure pineboo is initialized for testing."""
        init_testing()

    def test_basic(self) -> None:
        """Test collect a field and check the values"""

        from pineboolib.application.metadata.pnfieldmetadata import PNFieldMetaData

        field = PNFieldMetaData(
            "new_string",
            "Nuevo String",
            False,
            False,
            "string",
            20,
            False,
            True,
            True,
            0,
            0,
            False,
            False,
            False,
            "primero",
            False,
            None,
            True,
            False,
            False,
        )

        self.assertNotEqual(field, None)

        field.setOptionsList("primero,segundo,tercero,cuarto,quinto,sexto,12345678901234567890")

        self.assertEqual(field.name(), "new_string")
        self.assertEqual(field.alias(), "Nuevo String")
        self.assertEqual(field.isPrimaryKey(), False)
        self.assertEqual(field.isCompoundKey(), False)
        self.assertEqual(field.length(), 20)
        self.assertEqual(field.type(), "string")
        self.assertEqual(field.allowNull(), False)
        self.assertEqual(field.visibleGrid(), True)
        self.assertEqual(field.visible(), True)
        self.assertEqual(field.editable(), True)
        self.assertEqual(field.defaultValue(), "primero")
        self.assertEqual(field.regExpValidator(), None)
        self.assertEqual(field.partInteger(), 0)
        self.assertEqual(field.partDecimal(), 0)
        self.assertEqual(field.flDecodeType("string"), "string")
        self.assertEqual(
            field.optionsList(),
            ["primero", "segundo", "tercero", "cuarto", "quinto", "sexto", "12345678901234567890"],
        )
        self.assertEqual(field.getIndexOptionsList("segundo"), 1)


if __name__ == "__main__":
    unittest.main()
