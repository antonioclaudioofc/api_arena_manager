# API Arena Manager - Documentação

## Índice
- [Autenticação](#autenticação)
- [Usuário](#usuário)
- [Arenas](#arenas)
- [Quadras](#quadras)
- [Horários](#horários)
- [Reservas](#reservas)
- [Catálogo (Público)](#catálogo-público)
- [Códigos de Status HTTP](#códigos-de-status-http)
- [Tipos e Enums](#tipos-e-enums)

---

## Autenticação

### POST `/auth/register`
Registra um novo usuário no sistema.

**Request Body:**
```json
{
  "name": "string",
  "username": "string",
  "email": "user@example.com",
  "password": "string" // mínimo 6 caracteres
}
```

**Response:** `201 Created`
```json
{
  "message": "Usuário criado com sucesso"
}
```

**Erros:**
- `409 Conflict` - E-mail já cadastrado
- `409 Conflict` - Username já cadastrado
- `422 Unprocessable Entity` - Validação falhou (username com espaços, password muito curto, etc)

**Notas:**
- Username não pode conter espaços
- Usuário é criado com role `client` por padrão
- Campos são normalizados automaticamente (trim)

---

### POST `/auth/login`
Autentica um usuário e retorna token de acesso.

**Request Body:** (Form Data)
```
username: string
password: string
```

**Response:** `200 OK`
```json
{
  "access_token": "string",
  "token_type": "bearer"
}
```

**Erros:**
- `401 Unauthorized` - Usuário inexistente
- `401 Unauthorized` - Usuário ou senha inválida

**Notas:**
- Token expira em 20 minutos
- Use o token no header: `Authorization: Bearer {token}`

---

## Usuário

### GET `/user/me`
Retorna o perfil do usuário autenticado.

**Autenticação:** Requerida

**Response:** `200 OK`
```json
{
  "email": "user@example.com",
  "username": "string",
  "name": "string",
  "role": "client" | "owner" | "admin"
}
```

**Erros:**
- `401 Unauthorized` - Token inválido ou ausente

---

### PUT `/user/me`
Atualiza o perfil do usuário autenticado.

**Autenticação:** Requerida

**Request Body:**
```json
{
  "name": "string", // opcional
  "username": "string", // opcional
  "email": "user@example.com" // opcional
}
```

**Response:** `200 OK`
```json
{
  "message": "Perfil atualizado com sucesso"
}
```

**Erros:**
- `401 Unauthorized` - Token inválido
- `409 Conflict` - E-mail já cadastrado
- `409 Conflict` - Username já cadastrado
- `422 Unprocessable Entity` - Username com espaços

**Notas:**
- Todos os campos são opcionais
- Apenas os campos enviados serão atualizados

---

### PUT `/user/change-password`
Altera a senha do usuário autenticado.

**Autenticação:** Requerida

**Request Body:**
```json
{
  "password": "string",
  "new_password": "string" // mínimo 6 caracteres
}
```

**Response:** `200 OK`
```json
{
  "message": "Senha atualizado com sucesso"
}
```

**Erros:**
- `401 Unauthorized` - Token inválido
- `403 Forbidden` - Senha atual incorreta
- `403 Forbidden` - A nova senha deve ser diferente da atual
- `422 Unprocessable Entity` - Nova senha muito curta

---

### DELETE `/user/account`
Deleta a conta do usuário autenticado.

**Autenticação:** Requerida

**Response:** `200 OK`
```json
{
  "message": "Conta deletada com sucesso"
}
```

**Erros:**
- `401 Unauthorized` - Token inválido

---

## Arenas

### GET `/arenas/`
Lista todas as arenas do usuário autenticado.

**Autenticação:** Requerida (Owner)

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "owner_id": 1,
    "name": "Arena Central",
    "city": "São Paulo",
    "address": "Rua Exemplo, 123"
  }
]
```

**Erros:**
- `401 Unauthorized` - Token inválido
- `403 Forbidden` - Usuário não possui arenas

**Notas:**
- Retorna apenas arenas do owner autenticado

---

### POST `/arenas/`
Cria uma nova arena.

**Autenticação:** Requerida

**Request Body:**
```json
{
  "name": "string",
  "city": "string",
  "address": "string"
}
```

**Response:** `201 Created`
```json
{
  "message": "Arena criada com sucesso"
}
```

**Erros:**
- `401 Unauthorized` - Token inválido
- `422 Unprocessable Entity` - Campos obrigatórios ausentes

**Notas:**
- Usuário é automaticamente promovido a `owner` ao criar primeira arena
- Campos são normalizados automaticamente

---

### PUT `/arenas/{arena_id}`
Atualiza uma arena existente.

**Autenticação:** Requerida (Owner da arena)

**Request Body:**
```json
{
  "name": "string", // opcional
  "city": "string", // opcional
  "address": "string" // opcional
}
```

**Response:** `200 OK`
```json
{
  "message": "Arena atualizada com sucesso"
}
```

**Erros:**
- `401 Unauthorized` - Token inválido
- `403 Forbidden` - Sem permissão (não é o dono)
- `404 Not Found` - Arena não encontrada

**Notas:**
- Todos os campos são opcionais
- Apenas o dono pode atualizar

---

### DELETE `/arenas/{arena_id}`
Deleta uma arena.

**Autenticação:** Requerida (Owner da arena)

**Response:** `200 OK`
```json
{
  "message": "Arena deletada com sucesso"
}
```

**Erros:**
- `401 Unauthorized` - Token inválido
- `403 Forbidden` - Sem permissão (não é o dono)
- `404 Not Found` - Arena não encontrada

**Notas:**
- Apenas o dono pode deletar
- Deleta em cascata todas as quadras, horários e reservas relacionadas

---

## Quadras

### GET `/courts/{arena_id}`
Lista todas as quadras de uma arena específica.

**Autenticação:** Requerida (Owner da arena)

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "name": "Quadra 1",
    "arena_id": 1,
    "sports_type": "Futebol",
    "price_per_hour": 100.0
  }
]
```

**Erros:**
- `401 Unauthorized` - Token inválido
- `403 Forbidden` - Sem permissão (não é o dono da arena)

---

### POST `/courts/`
Cria uma nova quadra.

**Autenticação:** Requerida (Owner da arena)

**Request Body:**
```json
{
  "arena_id": 1,
  "name": "string",
  "sports_type": "string",
  "price_per_hour": 100.50
}
```

**Response:** `201 Created`
```json
{
  "message": "Quadra criada com sucesso"
}
```

**Erros:**
- `401 Unauthorized` - Token inválido
- `403 Forbidden` - Sem permissão (não é dono da arena)
- `404 Not Found` - Arena não encontrada
- `422 Unprocessable Entity` - Campos obrigatórios ausentes

**Notas:**
- Apenas o dono da arena pode criar quadras
- Campos são normalizados automaticamente

---

### PUT `/courts/{court_id}`
Atualiza uma quadra existente.

**Autenticação:** Requerida (Owner da arena)

**Request Body:**
```json
{
  "name": "string", // opcional
  "sports_type": "string", // opcional
  "price_per_hour": 100.50 // opcional
}
```

**Response:** `200 OK`
```json
{
  "message": "Quadra atualizada com sucesso"
}
```

**Erros:**
- `401 Unauthorized` - Token inválido
- `403 Forbidden` - Sem permissão para editar esta quadra
- `404 Not Found` - Quadra não encontrada
- `404 Not Found` - Arena não encontrada

**Notas:**
- Todos os campos são opcionais
- Apenas o dono da arena pode atualizar

---

### DELETE `/courts/{court_id}`
Deleta uma quadra.

**Autenticação:** Requerida (Owner da arena)

**Response:** `200 OK`
```json
{
  "message": "Quadra deletada com sucesso"
}
```

**Erros:**
- `401 Unauthorized` - Token inválido
- `403 Forbidden` - Sem permissão para remover esta quadra
- `404 Not Found` - Quadra não encontrada
- `404 Not Found` - Arena não encontrada

**Notas:**
- Apenas o dono da arena pode deletar
- Deleta em cascata todos os horários e reservas relacionadas

---

## Horários

### POST `/schedules/`
Cria um novo horário disponível.

**Autenticação:** Requerida (Owner da arena)

**Request Body:**
```json
{
  "court_id": 1,
  "date": "2026-01-27",
  "start_time": "10:00",
  "end_time": "11:00"
}
```

**Response:** `201 Created`
```json
{
  "message": "Horário criado com sucesso"
}
```

**Erros:**
- `400 Bad Request` - Não é possível criar horários para datas no passado
- `400 Bad Request` - Horário inicial deve ser menor que o horário final
- `401 Unauthorized` - Token inválido
- `403 Forbidden` - Sem permissão (não é dono da arena)
- `404 Not Found` - Quadra não encontrada
- `422 Unprocessable Entity` - Campos obrigatórios ausentes

**Notas:**
- Apenas o dono da arena pode criar horários
- Formato de data: `YYYY-MM-DD`
- Formato de hora: `HH:MM`
- Não é possível criar horários em datas passadas
- Hora inicial (start_time) deve ser menor que a hora final (end_time)

---

### POST `/schedules/batch`
Cria múltiplos horários de uma vez.

**Autenticação:** Requerida (Owner da arena)

**Request Body:**
```json
{
  "court_id": 1,
  "start_date": "2026-01-27",
  "end_date": "2026-01-31",
  "start_time": "08:00",
  "end_time": "20:00",
  "interval_minutes": 60,
  "weekdays": [0, 1, 2, 3, 4]
}
```

**Response:** `201 Created`
```json
{
  "message": "Horários criados com sucesso"
}
```

**Erros:**
- `400 Bad Request` - Intervalo inválido (menor ou igual a 0)
- `400 Bad Request` - Horário inicial deve ser menor que o final
- `401 Unauthorized` - Token inválido
- `403 Forbidden` - Sem permissão
- `404 Not Found` - Quadra não encontrada
- `409 Conflict` - Horário já existente

**Notas:**
- Cria horários automaticamente no intervalo de datas especificado e nos dias da semana definidos
- Weekdays: 0=Segunda, 1=Terça, ..., 6=Domingo
- Se `weekdays` estiver vazio, horários serão criados para todos os dias da semana
- Os meses são automaticamente determinados pelo intervalo de datas (start_date até end_date)
- Data inicial não pode ser no passado
- Data final deve ser maior ou igual à data inicial
- Horário inicial (start_time) deve ser menor que o horário final (end_time)

---

### PUT `/schedules/{schedule_id}`
Atualiza um horário existente.

**Autenticação:** Requerida (Owner da arena)

**Request Body:**
```json
{
  "date": "2026-01-28", // opcional
  "start_time": "10:00", // opcional
  "end_time": "11:00" // opcional
}
```

**Response:** `200 OK`
```json
{
  "message": "Horário atualizado com sucesso"
}
```

**Erros:**
- `401 Unauthorized` - Token inválido
- `403 Forbidden` - Sem permissão
- `404 Not Found` - Horário não encontrado

**Notas:**
- Todos os campos são opcionais
- Apenas o dono da arena pode atualizar

---

### DELETE `/schedules/{schedule_id}`
Deleta um horário.

**Autenticação:** Requerida (Owner da arena)

**Response:** `200 OK`
```json
{
  "message": "Horário deletado com sucesso"
}
```

**Erros:**
- `401 Unauthorized` - Token inválido
- `403 Forbidden` - Sem permissão
- `404 Not Found` - Horário não encontrado

**Notas:**
- Apenas o dono da arena pode deletar
- Deleta em cascata reservas relacionadas

---

## Reservas

### POST `/reservations/`
Cria uma nova reserva.

**Autenticação:** Requerida (Client)

**Request Body:**
```json
{
  "schedule_id": 1
}
```

**Response:** `201 Created`
```json
{
  "message": "Reserva criada com sucesso"
}
```

**Erros:**
- `400 Bad Request` - Não é possível reservar horários passados
- `400 Bad Request` - Horário já está reservado
- `401 Unauthorized` - Token inválido
- `403 Forbidden` - Apenas clientes podem fazer reservas
- `404 Not Found` - Horário não encontrado
- `422 Unprocessable Entity` - schedule_id ausente

**Notas:**
- Apenas usuários com role `client` podem criar reservas
- Não é possível reservar horários no passado (data < hoje)
- Apenas um cliente pode reservar cada horário

---

### GET `/reservations/`
Lista todas as reservas do sistema.

**Autenticação:** Não requerida

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "schedule_id": 1,
    "client_id": 1,
    "status": "active",
    "created_at": "2026-01-26T10:00:00Z"
  }
]
```

**Notas:**
- Endpoint público
- Retorna todas as reservas do sistema

---

### GET `/reservations/me`
Lista todas as reservas do usuário autenticado.

**Autenticação:** Requerida

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "schedule_id": 1,
    "client_id": 1,
    "status": "active",
    "created_at": "2026-01-26T10:00:00Z"
  }
]
```

**Erros:**
- `401 Unauthorized` - Token inválido

**Notas:**
- Retorna apenas reservas do usuário autenticado

---

### DELETE `/reservations/{reservation_id}`
Cancela uma reserva (muda status para cancelled).

**Autenticação:** Requerida (Client dono da reserva)

**Response:** `204 No Content`

**Erros:**
- `400 Bad Request` - Reserva já cancelada
- `401 Unauthorized` - Token inválido
- `403 Forbidden` - Sem permissão (não é o dono da reserva)
- `404 Not Found` - Reserva não encontrada

**Notas:**
- Apenas o cliente que fez a reserva pode cancelar
- Cancelamento muda o status para `cancelled` e registra `cancelled_at`
- Retorna HTTP 204 sem corpo

---

## Catálogo (Público)

Endpoints acessíveis sem autenticação para consultar arenas, quadras e horários disponíveis.

### GET `/catalog/arenas`
Lista todas as arenas disponíveis no sistema.

**Autenticação:** Não requerida

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "owner_id": 1,
    "name": "Arena Central",
    "city": "São Paulo",
    "address": "Rua Exemplo, 123"
  }
]
```

**Notas:**
- Endpoint público - sem autenticação necessária
- Retorna todas as arenas cadastradas no sistema

---

### GET `/catalog/arenas/{arena_id}`
Retorna detalhes de uma arena específica.

**Autenticação:** Não requerida

**Response:** `200 OK`
```json
{
  "id": 1,
  "owner_id": 1,
  "name": "Arena Central",
  "city": "São Paulo",
  "address": "Rua Exemplo, 123"
}
```

**Erros:**
- `404 Not Found` - Arena não encontrada

**Notas:**
- Endpoint público - sem autenticação necessária

---

### GET `/catalog/arenas/{arena_id}/courts`
Lista todas as quadras de uma arena específica.

**Autenticação:** Não requerida

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "name": "Quadra 1",
    "arena_id": 1,
    "sports_type": "Futebol",
    "price_per_hour": 100.0
  }
]
```

**Erros:**
- `404 Not Found` - Arena não encontrada

**Notas:**
- Endpoint público - sem autenticação necessária
- Retorna todas as quadras de uma arena

---

### GET `/catalog/courts/{court_id}/schedules`
Lista todos os horários disponíveis de uma quadra com informação de disponibilidade.

**Autenticação:** Não requerida

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "date": "2026-01-27",
    "start_time": "10:00",
    "end_time": "11:00",
    "court_id": 1,
    "available": true,
    "court": {
      "id": 1,
      "name": "Quadra 1",
      "arena_id": 1,
      "sports_type": "Futebol",
      "price_per_hour": 100.0
    }
  },
  {
    "id": 2,
    "date": "2026-01-27",
    "start_time": "11:00",
    "end_time": "12:00",
    "court_id": 1,
    "available": false,
    "court": {
      "id": 1,
      "name": "Quadra 1",
      "arena_id": 1,
      "sports_type": "Futebol",
      "price_per_hour": 100.0
    }
  }
]
```

**Erros:**
- `404 Not Found` - Quadra não encontrada

**Notas:**
- Endpoint público - sem autenticação necessária
- `available` é `true` quando o horário está livre
- `available` é `false` quando há uma reserva ativa para aquele horário
- Útil para exibir disponibilidade de agendamento para clientes

---

## Códigos de Status HTTP

### Sucesso
- `200 OK` - Requisição bem-sucedida
- `201 Created` - Recurso criado com sucesso
- `204 No Content` - Sucesso sem corpo de resposta (DELETE)

### Erros do Cliente
- `400 Bad Request` - Requisição inválida
- `401 Unauthorized` - Autenticação necessária ou inválida
- `403 Forbidden` - Sem permissão para acessar o recurso
- `404 Not Found` - Recurso não encontrado
- `409 Conflict` - Conflito (email/username duplicado, horário já existente)
- `422 Unprocessable Entity` - Validação de dados falhou

### Formato de Erro
```json
{
  "detail": "Mensagem de erro descritiva"
}
```

---

## Tipos e Enums

### UserRole
```typescript
type UserRole = "admin" | "owner" | "client"
```

- `admin` - Administrador do sistema
- `owner` - Proprietário de arenas
- `client` - Cliente que faz reservas

**Notas:**
- Usuários começam como `client`
- São promovidos automaticamente a `owner` ao criar primeira arena

### ReservationStatus
```typescript
type ReservationStatus = "active" | "cancelled" | "finished" | "cancel_requested"
```

- `active` - Reserva ativa
- `cancelled` - Reserva cancelada
- `finished` - Reserva finalizada
- `cancel_requested` - Cancelamento solicitado (não utilizado atualmente)

---

## Notas Gerais

### Autenticação
- Endpoints protegidos requerem header: `Authorization: Bearer {token}`
- Token expira em 20 minutos
- Token retornado no `/auth/login`

### Normalização de Dados
Os seguintes campos são automaticamente normalizados (trim):
- `name`, `username`, `email` (user)
- `name`, `city`, `address` (arena)
- `name`, `sports_type` (court)

### Validações Especiais
- Username não pode conter espaços
- Password deve ter no mínimo 6 caracteres
- Email deve ser válido
- Datas no formato ISO: `YYYY-MM-DD`
- Horários no formato: `HH:MM`

### Permissões
- **Client**: Pode criar reservas, atualizar perfil
- **Owner**: Pode gerenciar suas arenas, quadras e horários
- **Admin**: (não documentado, desconsiderado por enquanto)

### Cascata de Deleção
- Deletar arena → deleta quadras → deleta horários → deleta reservas
- Deletar quadra → deleta horários → deleta reservas
- Deletar horário → deleta reservas
