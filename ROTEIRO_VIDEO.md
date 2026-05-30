# Roteiro do Vídeo — Trabalho Docker (Sistemas Distribuídos)

## Duração estimada: 8 a 12 minutos

---

## MAPA DA ARQUITETURA (para mostrar no vídeo)

```
┌─────────────────────────────────────────────────────────────┐
│                     MÁQUINA LOCAL (HOST)                    │
│                                                             │
│  Navegador ──:8080──► [web] Flask To-Do                     │
│  Navegador ──:8081──► [adminer] Painel DB                   │
│  Navegador ──:9000──► [portainer] Gestão Docker             │
│                                                             │
│  ╔═══════════════════════════════════════════╗              │
│  ║         REDE INTERNA DOCKER               ║              │
│  ║                                           ║              │
│  ║  [web] ──────────────► [db] PostgreSQL    ║              │
│  ║  Flask :5000           interno :5432      ║              │
│  ║                              │            ║              │
│  ║                        [volume]           ║              │
│  ║                        db_data            ║              │
│  ║                    (dados persistentes)   ║              │
│  ╚═══════════════════════════════════════════╝              │
│                                                             │
│  IMPORTANTE: o banco de dados NÃO tem porta exposta         │
│  para o host — só os outros contêineres o acessam.          │
└─────────────────────────────────────────────────────────────┘
```

---

## ROTEIRO PASSO A PASSO

### PARTE 1 — Introdução (1 min)
> Fale enquanto mostra o terminal aberto na pasta do projeto

"Neste trabalho de Sistemas Distribuídos, configuramos um ambiente
com 4 contêineres Docker orquestrados pelo Docker Compose.
A aplicação é uma Lista de Tarefas feita em Python com Flask,
que armazena os dados num banco PostgreSQL."

- Mostrar a pasta `docker-todo/` no explorador de arquivos
- Listar os arquivos presentes

---

### PARTE 2 — Explicação do docker-compose.yml (3 min)
> Abrir o arquivo `docker-compose.yml` no editor

Explique cada serviço:

**Serviço `web`:**
"O contêiner web é construído a partir do Dockerfile na pasta /app.
A porta 8080 da máquina local é redirecionada para a porta 5000
do contêiner, que é onde o Flask escuta.
Ele depende do serviço db e só sobe quando o banco está saudável."

**Serviço `db`:**
"O PostgreSQL usa a imagem oficial postgres:16-alpine.
Perceba que ele NÃO tem uma seção `ports:` — isso significa que
nenhuma porta é aberta para máquinas externas.
O volume `db_data` garante que os dados persistam mesmo que o
contêiner seja derrubado e recriado."

**Serviço `adminer`:**
"O Adminer é uma interface web para gerenciar o banco de dados.
Fica disponível na porta 8081 do host."

**Serviço `portainer`:**
"O Portainer é uma interface gráfica para gerenciar todos os
contêineres Docker. Monta o socket do Docker para ter acesso
aos contêineres em execução. Fica na porta 9000."

**Networks e Volumes:**
"Todos os serviços estão na mesma rede bridge interna chamada
`internal`. Os volumes `db_data` e `portainer_data` são
volumes nomeados do Docker — os dados ficam no disco do host
e não se perdem ao parar os contêineres."

---

### PARTE 3 — Subindo o ambiente (1 min)
> No terminal, dentro da pasta `docker-todo/`

```bash
docker compose up --build
```

- Mostrar o download das imagens e o build do Flask
- Aguardar a mensagem de que todos os serviços estão prontos

---

### PARTE 4 — Demonstração da aplicação web (2 min)
> Abrir o navegador em http://localhost:8080

- Adicionar 3 ou 4 tarefas (ex: "Estudar Docker", "Fazer o trabalho", "Gravar vídeo")
- Marcar uma tarefa como concluída (botão "Concluir")
- Excluir uma tarefa
- Mostrar que o contador atualiza

---

### PARTE 5 — Demonstração do Adminer (2 min)
> Abrir o navegador em http://localhost:8081

Preencher o login:
- Sistema: PostgreSQL
- Servidor: **db**
- Usuário: todouser
- Senha: todopass
- Base de dados: tododb

- Clicar em "Selecionar" na tabela `tasks`
- Mostrar que os dados inseridos pela aplicação aparecem aqui
- Comentar: "Aqui conseguimos ver e editar os dados direto no banco"

---

### PARTE 6 — Demonstração do Portainer (1 min)
> Abrir o navegador em http://localhost:9000

- Criar conta inicial (se for a primeira vez)
- Ir em "local" → Containers
- Mostrar os 4 contêineres em execução: todo_web, todo_db, todo_adminer, todo_portainer
- Mostrar logs de algum contêiner (ex: todo_web)

---

### PARTE 7 — Demonstração de Persistência (1 min)
> No terminal

```bash
docker compose down
docker compose up
```

- Após reiniciar, abrir novamente http://localhost:8080
- Mostrar que as tarefas adicionadas anteriormente ainda estão lá
- "Isso demonstra a persistência de dados através do volume Docker"

---

### PARTE 8 — Encerramento (30 seg)
"O ambiente está completamente funcional com 4 contêineres
comunicando-se através de uma rede interna Docker.
O banco de dados é acessível apenas internamente,
e os dados são persistidos em volumes mesmo após reiniciar."

---

## DICAS PARA A GRAVAÇÃO
- Use OBS Studio ou a gravação de tela do Windows (Win + G)
- Aumente o zoom do terminal (Ctrl + Scroll) para ficar legível no vídeo
- Deixe o docker-compose.yml aberto no VS Code com a fonte maior
- Grave em resolução 1080p se possível
