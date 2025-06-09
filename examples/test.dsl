# Configurar banco de dados
configurar_banco "postgresql" "localhost" "5432" "meu_banco" "usuario" "senha"

# Iniciar servidor
iniciar_servidor "node" "app.js" "3000"

# Executar testes
executar_teste "pytest" "tests/"

# Deploy em ambiente de produção
deploy_ambiente "prod" "main" "https://github.com/usuario/projeto.git" 