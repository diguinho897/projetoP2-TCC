configurarBanco "localhost" "banco_teste" "sua_senha_aqui"
iniciarServidor "localhost" porta=8080
executarTeste "testes_unitarios"
deployEmAmbiente "producao" 