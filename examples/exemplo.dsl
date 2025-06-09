configurarBanco "localhost" "banco_teste"
iniciarServidor "localhost" porta=8080
executarTeste "testes_unitarios"
deployEmAmbiente "producao" 