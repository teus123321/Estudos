"""Testes do domínio sem depender de uma instalação do MySQL."""

import unittest

from sqlalchemy import create_engine

import banco


class TestesCadastroPets(unittest.TestCase):
    def setUp(self):
        banco.engine = create_engine("sqlite+pysqlite:///:memory:")
        banco.Base.metadata.create_all(banco.engine)
        self.assertTrue(banco.criar_usuario("ana", "senha-ana"))
        self.assertTrue(banco.criar_usuario("bruno", "senha-bruno"))
        self.ana_id = banco.autenticar("ana", "senha-ana")[0]
        self.bruno_id = banco.autenticar("bruno", "senha-bruno")[0]

    def tearDown(self):
        banco.engine.dispose()
        banco.engine = None

    def test_login_valido_e_invalido(self):
        self.assertEqual(banco.autenticar("ana", "senha-ana"), (self.ana_id, "ana"))
        self.assertIsNone(banco.autenticar("ana", "senha-errada"))
        self.assertIsNone(banco.autenticar("desconhecido", "1234"))
        self.assertFalse(banco.criar_usuario("ana", "outra-senha"))

    def test_cadastrar_e_listar_somente_os_proprios_pets(self):
        identificador = banco.cadastrar_pet(
            self.ana_id, "Rex", "5", "Vira-lata", "12,50", "Caramelo", "Tenho atualmente"
        )
        self.assertEqual(banco.listar_pets(self.bruno_id), [])
        registros = banco.listar_pets(self.ana_id)
        self.assertEqual(len(registros), 1)
        self.assertEqual(registros[0][0], identificador)
        self.assertEqual(registros[0][1], "Rex")
        self.assertEqual(str(registros[0][4]), "12.50")

    def test_edicao_e_exclusao_nao_permitem_outro_usuario(self):
        pet_id = banco.cadastrar_pet(self.ana_id, "Luna", 2, "SRD", "6.00", "Preta", "Já tive")
        self.assertFalse(banco.atualizar_pet(
            self.bruno_id, pet_id, "Invasão", 3, "SRD", 10, "Branca", "Já tive"
        ))
        self.assertFalse(banco.excluir_pet(self.bruno_id, pet_id))
        self.assertEqual(banco.listar_pets(self.ana_id)[0][1], "Luna")
        self.assertTrue(banco.atualizar_pet(
            self.ana_id, pet_id, "Luna", 4, "SRD", 7.5, "Preta", "Tenho atualmente"
        ))
        self.assertEqual(banco.listar_pets(self.ana_id)[0][2], 4)
        self.assertTrue(banco.excluir_pet(self.ana_id, pet_id))
        self.assertEqual(banco.listar_pets(self.ana_id), [])

    def test_validacao_dos_campos(self):
        exemplos_invalidos = [
            ("", 1, "SRD", 10, "Preta", "Já tive"),
            ("Lua", -1, "SRD", 10, "Preta", "Já tive"),
            ("Lua", "abc", "SRD", 10, "Preta", "Já tive"),
            ("Lua", 1, "SRD", 0, "Preta", "Já tive"),
            ("Lua", 1, "SRD", "nan", "Preta", "Já tive"),
            ("Lua", 1, "SRD", 10, "", "Já tive"),
            ("Lua", 1, "SRD", 10, "Preta", "Desconhecida"),
        ]
        for campos in exemplos_invalidos:
            with self.subTest(campos=campos), self.assertRaises(ValueError):
                banco.cadastrar_pet(self.ana_id, *campos)


if __name__ == "__main__":
    unittest.main()
