# Docker To-Do List — Sistemas Distribuídos

Ambiente Docker Compose com 4 contêineres: aplicação web Flask, PostgreSQL, Adminer e Portainer.

## Requisitos
- Docker Desktop instalado e em execução

## Como executar

```bash
docker compose up --build
```

### URLs disponíveis
| Serviço | URL |
|---|---|
| Aplicação Web (To-Do) | http://localhost:8080 |
| Adminer (gerenciar DB) | http://localhost:8081 |
| Portainer (gerenciar contêineres) | http://localhost:9000 |

### Login no Adminer
- **Sistema:** PostgreSQL
- **Servidor:** db
- **Usuário:** todouser
- **Senha:** todopass
- **Base de dados:** tododb

## Estrutura do projeto

```
docker-todo/
├── docker-compose.yml
└── app/
    ├── Dockerfile
    ├── requirements.txt
    ├── app.py
    └── templates/
        └── index.html
```

## Arquitetura

```
Máquina Local
│
├── :8080 ──► [web] Flask To-Do App
│                    │
│                    └── rede interna ──► [db] PostgreSQL :5432
│                                              │
│                                           volume db_data (persistência)
│
├── :8081 ──► [adminer] Interface DB
│
└── :9000 ──► [portainer] Gestão gráfica dos contêineres
```

> O banco de dados **não expõe porta para o host** — acessível apenas pelos contêineres da rede interna.
