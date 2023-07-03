# **README - Cliente e Servidor Tracker**

Este é um programa cliente-servidor que permite compartilhar e obter arquivos entre os clientes conectados usando um servidor Tracker.

## **Requisitos**

Certifique-se de ter o seguinte software instalado em seu sistema:

- Python (versão 3.x)

## **Configuração**

1. Faça o download dos arquivos **`tracker_server.py`** e **`client.py`** para o seu sistema.
2. Abra os arquivos **`tracker_server.py`** e **`client.py`** em um editor de texto.
3. No arquivo **`tracker_server.py`**, verifique e modifique o endereço IP e a porta na linha **`self.server_socket.bind(('192.168.0.141', 5000))`** para corresponder ao endereço IP e porta desejados para o servidor Tracker.
4. No arquivo **`client.py`**, verifique e modifique o endereço IP e a porta na linha **`self.tracker_address = ('192.168.0.141', 5000)`** para corresponder ao endereço IP e porta do servidor Tracker configurado anteriormente.
5. O cliente e o servidor Tracker devem estar na mesma rede ou ter conectividade para se comunicarem corretamente.

## **Compilação e Execução**

Siga as etapas abaixo para compilar e executar o programa:

1. Abra um terminal ou prompt de comando.
2. Navegue até o diretório onde os arquivos **`tracker_server.py`** e **`client.py`** estão localizados.
3. Para iniciar o servidor Tracker, execute o seguinte comando no terminal:
    
    ```
    python tracker_server.py
    ```
    
    O servidor Tracker iniciará e estará pronto para aceitar conexões de clientes.
    
4. Em outro terminal, execute o seguinte comando para iniciar um cliente:
    
    ```
    python client.py
    ```
    
    O cliente se conectará ao servidor Tracker e começará a compartilhar e obter arquivos com outros clientes conectados.
    

## **Considerações Finais**

Certifique-se de que o servidor Tracker esteja em execução antes de iniciar o cliente. Verifique as configurações de endereço IP e porta para garantir que o cliente se conecte ao servidor corretamente.

O programa permite que você compartilhe arquivos no diretório "files" localizado no mesmo diretório do arquivo **`client.py`**. Certifique-se de colocar os arquivos que deseja compartilhar nesse diretório.
