# Configurar banco de dados
configurarBanco "localhost" "banco_teste" "sua_senha_aqui_test"

# Iniciar servidor
iniciarServidor "localhost" porta=8080

# Executar testes
executarTeste "testes_unitarios"

# Deploy em ambiente de produção
deployEmAmbiente "producao" 