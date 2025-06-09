import subprocess
import logging
import os
import signal
from pathlib import Path
from typing import Dict, Any

class DSLInterpreter:
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Configuração do logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_dir / "dsl_execution.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("DSLInterpreter")
        
        # Mapeamento de comandos para funções
        self.command_handlers = {
            "configurar_banco": self._handle_configurar_banco,
            "iniciar_servidor": self._handle_iniciar_servidor,
            "executar_teste": self._handle_executar_teste,
            "deploy_ambiente": self._handle_deploy_ambiente
        }
        
        # Armazena processos em execução
        self.running_processes = {}
    
    def execute(self, commands):
        """
        Executa uma lista de comandos.
        
        Args:
            commands: Lista de comandos a serem executados
            
        Returns:
            list: Lista de resultados da execução
        """
        results = []
        try:
            for command in commands:
                try:
                    handler = self.command_handlers.get(command.name)
                    if not handler:
                        self.logger.error(f"Comando desconhecido: {command.name}")
                        results.append({
                            'command': command.name,
                            'success': False,
                            'error': 'Comando desconhecido'
                        })
                        continue
                    
                    success = handler(**command.args)
                    results.append({
                        'command': command.name,
                        'success': success
                    })
                    
                except Exception as e:
                    self.logger.error(f"Erro ao executar comando {command.name}: {str(e)}")
                    results.append({
                        'command': command.name,
                        'success': False,
                        'error': str(e)
                    })
        finally:
            # Limpa processos em execução
            self._cleanup_processes()
        
        return results
    
    def _cleanup_processes(self):
        """Limpa todos os processos em execução."""
        for name, process in self.running_processes.items():
            try:
                if process.poll() is None:  # Processo ainda está rodando
                    process.terminate()
                    process.wait(timeout=5)
            except Exception as e:
                self.logger.error(f"Erro ao limpar processo {name}: {str(e)}")
                try:
                    os.kill(process.pid, signal.SIGKILL)
                except:
                    pass
    
    def _handle_configurar_banco(self, host: str, database: str) -> bool:
        """Configura o banco de dados."""
        try:
            # Remove as aspas dos argumentos
            host = host.strip('"')
            database = database.strip('"')
            
            self.logger.info(f"Configurando banco de dados: {database} em {host}")
            
            # Verifica se o PostgreSQL está instalado
            if not self._check_command_exists('psql'):
                self.logger.error("PostgreSQL não está instalado")
                return False
            
            # Cria o banco de dados
            cmd = f"sudo -u postgres psql -h {host} -c 'CREATE DATABASE {database}'"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                self.logger.info(f"Banco {database} configurado com sucesso")
                return True
            else:
                self.logger.error(f"Erro ao configurar banco: {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"Erro ao configurar banco: {str(e)}")
            return False
    
    def _handle_iniciar_servidor(self, host: str, porta: int) -> bool:
        """Inicia o servidor."""
        try:
            # Remove as aspas do host
            host = host.strip('"')
            
            self.logger.info(f"Iniciando servidor em {host}:{porta}")
            
            # Verifica se a porta está em uso
            if self._is_port_in_use(porta):
                self.logger.error(f"Porta {porta} já está em uso")
                return False
            
            # Inicia o servidor usando systemd
            service_name = f"dsl-server-{porta}"
            service_content = f"""[Unit]
Description=DSL Server on port {porta}
After=network.target

[Service]
Type=simple
User={os.getenv('USER')}
WorkingDirectory={os.getcwd()}
ExecStart=/usr/bin/python3 -m http.server {porta} --bind {host}
Restart=on-failure

[Install]
WantedBy=multi-user.target
"""
            
            # Cria o arquivo de serviço
            service_path = f"/etc/systemd/system/{service_name}.service"
            with open(service_path, 'w') as f:
                f.write(service_content)
            
            # Recarrega o systemd e inicia o serviço
            subprocess.run(['sudo', 'systemctl', 'daemon-reload'])
            subprocess.run(['sudo', 'systemctl', 'start', service_name])
            
            self.logger.info(f"Servidor iniciado como serviço systemd: {service_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao iniciar servidor: {str(e)}")
            return False
    
    def _handle_executar_teste(self, suite: str) -> bool:
        """Executa os testes."""
        try:
            # Remove as aspas do argumento
            suite = suite.strip('"')
            
            self.logger.info(f"Executando suite de testes: {suite}")
            
            # Verifica se o pytest está instalado
            if not self._check_command_exists('pytest'):
                self.logger.error("pytest não está instalado")
                return False
            
            # Executa os testes
            cmd = f"python3 -m pytest {suite} -v"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                self.logger.info(f"Testes executados com sucesso")
                return True
            else:
                self.logger.error(f"Erro nos testes: {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"Erro ao executar testes: {str(e)}")
            return False
    
    def _handle_deploy_ambiente(self, ambiente: str) -> bool:
        """Realiza o deploy no ambiente especificado."""
        try:
            # Remove as aspas do argumento
            ambiente = ambiente.strip('"')
            
            self.logger.info(f"Realizando deploy no ambiente: {ambiente}")
            
            # Verifica se o Docker está instalado
            if not self._check_command_exists('docker'):
                self.logger.error("Docker não está instalado")
                return False
            
            # Verifica se o Docker Compose está instalado
            if not self._check_command_exists('docker-compose'):
                self.logger.error("Docker Compose não está instalado")
                return False
            
            # Executa o deploy usando Docker Compose
            cmd = f"docker-compose -f docker-compose.{ambiente}.yml up -d"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                self.logger.info(f"Deploy realizado com sucesso em {ambiente}")
                return True
            else:
                self.logger.error(f"Erro no deploy: {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"Erro ao realizar deploy: {str(e)}")
            return False
    
    def _check_command_exists(self, command: str) -> bool:
        """Verifica se um comando existe no sistema."""
        return subprocess.run(['which', command], 
                            capture_output=True).returncode == 0
    
    def _is_port_in_use(self, port: int) -> bool:
        """Verifica se uma porta está em uso."""
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) == 0 