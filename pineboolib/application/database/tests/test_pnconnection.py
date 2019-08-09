"""Test_pnconnection module."""

import unittest
from pineboolib.loader.main import init_testing
from pineboolib import application
from pineboolib.application.database import pnsqlcursor


class TestPNConnection(unittest.TestCase):
    """TestPNConnection Class."""

    @classmethod
    def setUpClass(cls) -> None:
        """Ensure pineboo is initialized for testing."""
        init_testing()

    def test_basic1(self) -> None:
        """Basic test 1."""

        conn_ = application.project.conn

        self.assertEqual(conn_.connectionName(), "default")
        conn_aux_ = conn_.useConn("dbAux")
        conn_.useConn("conn_test")
        self.assertNotEqual(conn_, conn_aux_)
        dict_databases = conn_.dictDatabases()
        self.assertTrue(dict_databases)

        self.assertTrue(conn_.isOpen())
        self.assertTrue(conn_.useConn("dbAux").isOpen())
        self.assertFalse(conn_.useConn("conn_test").isOpen())

        self.assertEqual([*dict_databases], ["dbAux", "conn_test"])
        self.assertTrue(conn_.removeConn("conn_test"))
        self.assertEqual([*dict_databases], ["dbAux"])

    def test_basic2(self) -> None:
        """Basic test 2."""

        conn_ = application.project.conn

        default_tables_list = [
            "flareas",
            "flmodules",
            "flfiles",
            "flgroups",
            "fllarge",
            "flserial",
            "flusers",
            "flvar",
            "flmetadata",
            "fltest",
        ]

        self.assertEqual(conn_.tables("Tables"), default_tables_list)
        default_tables_list.append("sqlite_master")
        self.assertEqual(conn_.tables(), default_tables_list)
        self.assertEqual(conn_.tables("SystemTables"), ["sqlite_master"])
        self.assertEqual(conn_.tables("Views"), [])

        db = conn_.database()
        db_db_aux = conn_.database("dbAux")
        self.assertEqual(conn_.db(), conn_)
        self.assertNotEqual(db, db_db_aux)
        self.assertEqual(conn_.DBName(), str(conn_))

    def test_basic3(self) -> None:
        """Basic test 3."""

        from pineboolib.fllegacy import systype

        conn_ = application.project.conn
        sys_type = systype.SysType()

        self.assertTrue(conn_.driver())
        self.assertTrue(conn_.cursor())
        sys_type.addDatabase("conn_test_2")
        self.assertTrue(conn_.useConn("conn_test_2").isOpen())
        sys_type.removeDatabase("conn_test_2")
        self.assertEqual(conn_.driverName(), "FLsqlite")
        self.assertEqual(conn_.driver().alias_, conn_.driverAlias())
        self.assertEqual(conn_.driverNameToDriverAlias(conn_.driverName()), "SQLite3 (SQLITE3)")

    def test_basic4(self) -> None:
        """Basic test 4."""

        conn_ = application.project.conn

        self.assertTrue(conn_.interactiveGUI_)
        conn_.setInteractiveGUI(False)
        self.assertFalse(conn_.interactiveGUI())
        self.assertEqual(conn_, conn_.db())
        self.assertEqual(conn_.dbAux(), conn_.useConn("dbAux"))

        self.assertEqual(conn_.formatValue("string", "hola", True), "'HOLA'")
        self.assertEqual(conn_.formatValueLike("string", "hola", True), "LIKE 'HOLA%%'")
        self.assertTrue(conn_.canSavePoint())
        self.assertTrue(conn_.canTransaction())
        self.assertEqual(conn_.transactionLevel(), 0)
        self.assertTrue(conn_.canDetectLocks())
        self.assertTrue(conn_.manager())
        self.assertTrue(conn_.managerModules())
        self.assertTrue(conn_.canOverPartition())

        mtd_seqs = conn_.manager().metadata("flseqs")

        if mtd_seqs is None:
            raise Exception("mtd_seqs is empty!.")

        self.assertTrue(conn_.existsTable("fltest"))
        self.assertTrue(conn_.existsTable("flseqs"))
        self.assertFalse(conn_.mismatchedTable("flseqs", mtd_seqs))
        self.assertEqual(conn_.normalizeValue("holá, 'avión'"), "holá, ''avión''")

    def test_basic5(self) -> None:
        """Basic test 5."""

        conn_ = application.project.conn

        cursor = pnsqlcursor.PNSqlCursor("flareas")
        conn_.doTransaction(cursor)
        cursor.setModeAccess(cursor.Insert)
        cursor.setValueBuffer("idarea", "test")
        cursor.setValueBuffer("bloqueo", "false")
        cursor.setValueBuffer("descripcion", "test area")
        cursor.commitBuffer()
        conn_.doRollback(cursor)
        conn_.doTransaction(cursor)
        cursor.setModeAccess(cursor.Insert)
        cursor.setValueBuffer("idarea", "test")
        cursor.setValueBuffer("bloqueo", "false")
        cursor.setValueBuffer("descripcion", "test area")
        cursor.commitBuffer()
        conn_.doCommit(cursor, False)


if __name__ == "__main__":
    unittest.main()
