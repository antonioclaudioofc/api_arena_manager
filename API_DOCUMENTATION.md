# API Arena Manager - Documentacao Completa

## 1. Visao geral

- Nome da API: `Arena Manager`
- Framework: `FastAPI`
- Titulo OpenAPI: `Arena Manager`
- Endpoint raiz: `GET /`
- Resposta da raiz:

```json
{
  "message": "Welcome to the Arena Manager API"
}
```

## 2. Autenticacao

A API usa Bearer Token JWT.

- Header esperado:

```http
Authorization: Bearer <token>
```

- O token e emitido em `POST /auth/login`.
- Expiracao atual do token: `20 minutos`.

## 3. Formato padrao de respostas

### 3.1 Sucesso com mensagem

Schema `MessageResponse`:

```json
{
  "message": "string"
}
```

### 3.2 Erro de regra de negocio

`HTTPException` customizada retorna:

```json
{
  "message": "string"
}
```

### 3.3 Erro de validacao de entrada

Para erros de validacao (Pydantic/FastAPI), a API retorna `400`:

```json
{
  "message": "Dados invalidos",
  "fields": {
    "campo": "descricao do erro"
  }
}
```

### 3.4 Erro SQL/enum

Quando ocorre erro de enum no banco, retorna `400`:

```json
{
  "message": "valor invalido para um dos campos",
  "fiels": {
    "role": "Use apenas: admin ou client"
  }
}
```

Observacao: o campo esta escrito como `fiels` no codigo atual.

### 3.5 Erro interno

```json
{
  "message": "Erro interno no servidor"
}
```

## 4. Endpoints

## 4.1 Auth (`/auth`)

### POST `/auth/register`

Cria usuario e publica evento de verificacao de e-mail.

Auth: nao requer

Request body (`RequestUser`):

```json
{
  "name": "Joao Silva",
  "email": "joao@exemplo.com",
  "password": "123456"
}
```

Regras:
- `password` minimo 6 caracteres
- `email` unico
- usuario e criado com role `player`
- `is_email_verified` inicia como `false`

Response:
- `201 Created`

```json
{
  "message": "Usuario criado com sucesso"
}
```

Possiveis erros:
- `409` `{"message": "E-mail ja cadastrado"}`
- `400` erro de validacao de body

---

### POST `/auth/login`

Autentica usuario e retorna JWT.

Auth: nao requer

Request: `application/x-www-form-urlencoded`

Campos:
- `username`: recebe o e-mail
- `password`: senha

Response:
- `200 OK`

```json
{
  "access_token": "<jwt>",
  "token_type": "bearer"
}
```

Possiveis erros:
- `401` `{"message": "Usuario inexistente"}`
- `401` `{"message": "Usuario ou senha invalida"}`
- `401` `{"message": "E-mail nao verificado"}`

---

### GET `/auth/verify-email?token=<token>`

Verifica e-mail por token e responde HTML.

Auth: nao requer

Response:
- `200 OK` (`text/html`) pagina de sucesso

Possiveis erros:
- `401` (`text/html`) pagina de falha com mensagem de token invalido

---

### POST `/auth/forgot-password`

Solicita recuperacao de senha.

Auth: nao requer

Request body (`ForgotPasswordRequest`):

```json
{
  "email": "usuario@dominio.com"
}
```

Comportamento:
- Se o e-mail existir:
- gera `reset_password_token`
- define expiracao em `1 hora`
- publica evento `password_reset`
- Se nao existir: retorna mesma resposta para nao vazar existencia

Response:
- `200 OK`

```json
{
  "message": "Enviado as instrucoes de recuperacao para o e-mail."
}
```

---

### POST `/auth/reset-password`

Reseta senha via JSON usando token.

Auth: nao requer

Request body (`ResetPasswordRequest`):

```json
{
  "token": "token-de-reset",
  "new_password": "novaSenha123"
}
```

Regras:
- `new_password` minimo 6 caracteres
- token precisa existir e nao estar expirado

Response:
- `200 OK`

```json
{
  "message": "Senha redefinida com sucesso"
}
```

Possiveis erros:
- `401` `{"message": "Token invalido"}`
- `401` `{"message": "Token expirado"}`
- `400` erro de validacao do body

---

### GET `/auth/reset-password?token=<token>`

Abre pagina HTML com formulario de nova senha.

Auth: nao requer

Response:
- `200 OK` (`text/html`) formulario

Possiveis erros:
- `401` (`text/html`) pagina de link invalido/expirado

---

### POST `/auth/reset-password-form`

Submete formulario HTML para redefinir senha.

Auth: nao requer

Request: `application/x-www-form-urlencoded`

Campos:
- `token`: string
- `new_password`: string (minimo 6)

Response:
- `200 OK` (`text/html`) pagina de sucesso

Possiveis erros:
- `400` (`text/html`) senha invalida
- `401` (`text/html`) token invalido/expirado

## 4.2 User (`/user`)

### GET `/user/me`

Retorna usuario autenticado.

Auth: requer Bearer

Response (`ResponseUser`):
- `200 OK`

```json
{
  "id": "uuid",
  "email": "user@dominio.com",
  "name": "Nome",
  "role": "player"
}
```

Possiveis erros:
- `401` token invalido/ausente
- `401` usuario do token nao encontrado

---

### PUT `/user/me`

Atualiza perfil.

Auth: requer Bearer

Request body (`UpdateUser`):

```json
{
  "name": "Novo Nome",
  "email": "novo@dominio.com"
}
```

Todos os campos sao opcionais.

Response:
- `200 OK`

```json
{
  "message": "Perfil atualizado com sucesso"
}
```

Possiveis erros:
- `409` e-mail ja cadastrado
- `409` username ja cadastrado (regra existente no servico)
- `400` validacao
- `401` token invalido/ausente

---

### PUT `/user/change-password`

Troca senha do usuario logado.

Auth: requer Bearer

Request body (`UserVerification`):

```json
{
  "password": "senhaAtual",
  "new_password": "novaSenha123"
}
```

Regras:
- `new_password` minimo 6
- senha atual deve estar correta
- nova senha deve ser diferente da atual

Response:
- `200 OK`

```json
{
  "message": "Senha atualizado com sucesso"
}
```

Possiveis erros:
- `403` senha atual incorreta
- `403` nova senha igual a atual
- `400` validacao
- `401` token invalido/ausente

---

### DELETE `/user/account`

Remove conta do usuario autenticado.

Auth: requer Bearer

Response:
- `200 OK`

```json
{
  "message": "Conta deletada com sucesso"
}
```

Possiveis erros:
- `401` token invalido/ausente

## 4.3 Arenas (`/arenas`)

Todos endpoints requerem Bearer.

### GET `/arenas/`

Lista arenas do usuario.

Response (`list[ResponseArena]`):
- `200 OK`

Possiveis erros:
- `403` `{"message": "Usuario nao possui arenas"}`
- `401` token invalido/ausente

---

### POST `/arenas/`

Cria arena.

Request body (`RequestArena`):

```json
{
  "name": "Arena Centro",
  "description": "Opcional",
  "phone": "11999999999",
  "email": "arena@dominio.com",
  "city": "Sao Paulo",
  "address": "Rua X, 123",
  "state": "SP",
  "zip_code": "01000-000",
  "opening_time": "08:00:00",
  "closing_time": "22:00:00"
}
```

Obrigatorios:
- `name`, `phone`, `city`, `address`, `state`, `zip_code`

Response:
- `201 Created`

```json
{
  "message": "Arena criada com sucesso"
}
```

Possiveis erros:
- `400` validacao
- `401` token invalido/ausente

---

### PUT `/arenas/{arena_id}`

Atualiza arena.

Request body (`UpdateArena`): todos opcionais.

Response:
- `200 OK`

```json
{
  "message": "Arena atualizada com sucesso"
}
```

Possiveis erros:
- `404` arena nao encontrada
- `403` sem permissao
- `400` validacao
- `401` token invalido/ausente

---

### DELETE `/arenas/{arena_id}`

Remove arena.

Response:
- `200 OK`

```json
{
  "message": "Arena deletada com sucesso"
}
```

Possiveis erros:
- `404` arena nao encontrada
- `403` sem permissao
- `401` token invalido/ausente

## 4.4 Courts (`/courts`)

Todos endpoints requerem Bearer.

### POST `/courts/`

Cria quadra.

Request body (`RequestCourt`):

```json
{
  "arena_id": "uuid",
  "name": "Quadra 1",
  "sport_type": "futsal",
  "surface_type": "sintetico",
  "price_per_hour": 120.50
}
```

Obrigatorios:
- `arena_id`, `name`, `sport_type`, `price_per_hour`

Response:
- `201 Created`

```json
{
  "message": "Quadra criada com sucesso"
}
```

Possiveis erros:
- `404` arena nao encontrada
- `403` sem permissao
- `400` validacao
- `401` token invalido/ausente

---

### GET `/courts/{arena_id}`

Lista quadras da arena do dono autenticado.

Response (`list[ResponseCourt]`):
- `200 OK`

Possiveis erros:
- `403` sem permissao
- `401` token invalido/ausente

---

### PUT `/courts/{court_id}`

Atualiza quadra.

Request body (`UpdateCourt`): campos opcionais.

Response:
- `200 OK`

```json
{
  "message": "Quadra atualizada com sucesso"
}
```

Possiveis erros:
- `404` quadra nao encontrada
- `404` arena nao encontrada
- `403` sem permissao para editar
- `400` validacao
- `401` token invalido/ausente

---

### DELETE `/courts/{court_id}`

Remove quadra.

Response:
- `200 OK`

```json
{
  "message": "Quadra deletada com sucesso"
}
```

Possiveis erros:
- `404` quadra nao encontrada
- `404` arena nao encontrada
- `403` sem permissao para remover
- `401` token invalido/ausente

## 4.5 Schedules (`/schedules`)

Todos endpoints requerem Bearer.

### POST `/schedules/`

Cria um horario.

Request body (`RequestSchedule`):

```json
{
  "court_id": "uuid",
  "date": "2026-03-10",
  "start_time": "09:00",
  "end_time": "10:00"
}
```

Response:
- `201 Created`

```json
{
  "message": "Horario criado com sucesso"
}
```

Possiveis erros:
- `404` quadra nao encontrada
- `403` sem permissao
- `400` data no passado
- `400` horario inicial >= final
- `400` validacao
- `401` token invalido/ausente

---

### POST `/schedules/batch`

Cria horarios em lote.

Request body (`RequestScheduleBatch`):

```json
{
  "court_id": "uuid",
  "start_date": "2026-03-10",
  "end_date": "2026-03-20",
  "start_time": "08:00",
  "end_time": "12:00",
  "interval_minutes": 60,
  "weekdays": [0, 1, 2, 3, 4]
}
```

Notas:
- `weekdays` usa padrao Python: `0=segunda` ... `6=domingo`
- se `weekdays` vazio, usa todos os dias

Response:
- `201 Created`

```json
{
  "message": "Horarios criados com sucesso"
}
```

Possiveis erros:
- `404` quadra nao encontrada
- `403` sem permissao
- `400` intervalo invalido
- `400` data inicial no passado
- `400` data final menor que inicial
- `400` horario inicial >= final
- `409` conflito de horario existente
- `400` validacao
- `401` token invalido/ausente

---

### PUT `/schedules/{schedule_id}`

Atualiza horario.

Request body (`UpdateSchedule`): todos opcionais.

Response:
- `200 OK`

```json
{
  "message": "Horario atualizado com sucesso"
}
```

Possiveis erros:
- `404` horario nao encontrado
- `403` sem permissao
- `400` validacao
- `401` token invalido/ausente

---

### DELETE `/schedules/{schedule_id}`

Remove horario.

Response:
- `200 OK`

```json
{
  "message": "Horario deletado com sucesso"
}
```

Possiveis erros:
- `404` horario nao encontrado
- `403` sem permissao
- `401` token invalido/ausente

## 4.6 Reservations (`/reservations`)

### POST `/reservations/`

Cria reserva.

Auth: requer Bearer

Request body (`RequestReservation`):

```json
{
  "schedule_id": "uuid"
}
```

Regras:
- apenas usuario `player` pode reservar
- horario deve existir
- horario nao pode ser passado
- horario nao pode estar confirmado por outra reserva

Response:
- `201 Created`

```json
{
  "message": "Reserva criada com sucesso"
}
```

Possiveis erros:
- `403` apenas clientes podem reservar
- `404` horario nao encontrado
- `400` horario passado
- `400` horario ja reservado
- `400` validacao
- `401` token invalido/ausente

---

### GET `/reservations/`

Lista todas as reservas.

Auth: nao requer (no codigo atual)

Response:
- `200 OK`
- formato: lista de objetos `Reservation` (sem response_model explicito)

---

### GET `/reservations/me`

Lista reservas do usuario autenticado.

Auth: requer Bearer

Response (`list[ResponseReservation]`):
- `200 OK`

---

### GET `/reservations/owner`

Lista reservas das arenas do owner autenticado.

Auth: requer Bearer

Response (`list[ResponseOwnerReservation]`):
- `200 OK`

Possiveis erros:
- `403` apenas donos podem visualizar
- `401` token invalido/ausente

---

### DELETE `/reservations/{reservation_id}`

Cancela reserva.

Auth: requer Bearer

Response:
- `204 No Content`

Possiveis erros:
- `404` reserva nao encontrada
- `403` sem permissao
- `400` reserva ja cancelada
- `401` token invalido/ausente

## 4.7 Catalog (`/catalog`)

Endpoints publicos de consulta.

### GET `/catalog/arenas`

Lista todas as arenas.

Response (`list[ResponseArena]`):
- `200 OK`

---

### GET `/catalog/arenas/{arena_id}`

Retorna arena por id.

Response (`ResponseArena`):
- `200 OK`

Possiveis erros:
- `404` arena nao encontrada

---

### GET `/catalog/arenas/{arena_id}/courts`

Lista quadras da arena.

Response (`list[ResponseCourt]`):
- `200 OK`

Possiveis erros:
- `404` arena nao encontrada

---

### GET `/catalog/courts/{court_id}/schedules`

Lista horarios com disponibilidade.

Response (`list[dict]`):

```json
[
  {
    "id": "uuid",
    "date": "2026-03-10",
    "start_time": "09:00",
    "end_time": "10:00",
    "court_id": "uuid",
    "is_available": true
  }
]
```

Possiveis erros:
- `404` quadra nao encontrada

## 5. Schemas (definicoes)

## 5.1 Auth/User

### `Token`

```json
{
  "access_token": "string",
  "token_type": "string"
}
```

### `RequestUser`

```json
{
  "name": "string",
  "email": "email",
  "password": "string (min 6)"
}
```

### `UpdateUser`

```json
{
  "name": "string | null",
  "email": "email | null"
}
```

### `ResponseUser`

```json
{
  "id": "uuid",
  "email": "email",
  "name": "string",
  "role": "admin | owner | player"
}
```

### `UserVerification`

```json
{
  "password": "string",
  "new_password": "string (min 6)"
}
```

### `ForgotPasswordRequest`

```json
{
  "email": "email"
}
```

### `ResetPasswordRequest`

```json
{
  "token": "string",
  "new_password": "string (min 6)"
}
```

## 5.2 Arena

### `RequestArena`

```json
{
  "name": "string",
  "description": "string | null",
  "phone": "string",
  "email": "string | null",
  "city": "string",
  "address": "string",
  "state": "string",
  "zip_code": "string",
  "opening_time": "HH:MM:SS | null",
  "closing_time": "HH:MM:SS | null"
}
```

### `UpdateArena`

Mesmo campos de `RequestArena`, todos opcionais.

### `ResponseArena`

```json
{
  "id": "uuid",
  "owner_id": "uuid",
  "name": "string",
  "slug": "string | null",
  "description": "string | null",
  "phone": "string",
  "email": "string | null",
  "city": "string",
  "address": "string",
  "state": "string",
  "zip_code": "string",
  "opening_time": "HH:MM:SS | null",
  "closing_time": "HH:MM:SS | null"
}
```

## 5.3 Court

### `RequestCourt`

```json
{
  "arena_id": "uuid",
  "name": "string",
  "sport_type": "string",
  "surface_type": "string | null",
  "price_per_hour": 120.50
}
```

### `UpdateCourt`

Mesmo campos de `RequestCourt`, opcionais (exceto `arena_id` que nao esta no schema de update).

### `ResponseCourt`

```json
{
  "id": "uuid",
  "slug": "string | null",
  "name": "string",
  "arena_id": "uuid",
  "sport_type": "string",
  "surface_type": "string",
  "price_per_hour": 120.50
}
```

## 5.4 Schedule

### `RequestSchedule`

```json
{
  "court_id": "uuid",
  "date": "YYYY-MM-DD",
  "start_time": "HH:MM",
  "end_time": "HH:MM"
}
```

### `RequestScheduleBatch`

```json
{
  "court_id": "uuid",
  "start_date": "YYYY-MM-DD",
  "end_date": "YYYY-MM-DD",
  "start_time": "HH:MM",
  "end_time": "HH:MM",
  "interval_minutes": 60,
  "weekdays": [0, 1, 2, 3, 4]
}
```

### `UpdateSchedule`

```json
{
  "date": "YYYY-MM-DD | null",
  "start_time": "HH:MM | null",
  "end_time": "HH:MM | null"
}
```

### `ResponseSchedule`

```json
{
  "id": "uuid",
  "court_id": "uuid",
  "date": "YYYY-MM-DD",
  "start_time": "HH:MM",
  "end_time": "HH:MM",
  "court": {
    "id": "uuid",
    "slug": "string | null",
    "name": "string",
    "arena_id": "uuid",
    "sport_type": "string",
    "surface_type": "string",
    "price_per_hour": 120.50
  }
}
```

## 5.5 Reservation

### `RequestReservation`

```json
{
  "schedule_id": "uuid"
}
```

### `UpdateReservation`

```json
{
  "status": "pending | confirmed | cancelled | expired | completed | no_show"
}
```

### `ResponseReservation`

```json
{
  "id": "uuid",
  "schedule_id": "uuid",
  "user_id": "uuid",
  "status": "confirmed",
  "schedule": {
    "id": "uuid",
    "court_id": "uuid",
    "date": "YYYY-MM-DD",
    "start_time": "HH:MM",
    "end_time": "HH:MM",
    "court": {
      "id": "uuid",
      "slug": "string | null",
      "name": "string",
      "arena_id": "uuid",
      "sport_type": "string",
      "surface_type": "string",
      "price_per_hour": 120.50
    }
  }
}
```

### `ResponseOwnerReservation`

```json
{
  "id": "uuid",
  "status": "confirmed | cancelled | ...",
  "created_at": "datetime | null",
  "cancelled_at": "datetime | null",
  "schedule": {
    "id": "uuid",
    "date": "YYYY-MM-DD",
    "start_time": "HH:MM",
    "end_time": "HH:MM"
  },
  "court": {
    "id": "uuid",
    "name": "string"
  },
  "arena": {
    "id": "uuid",
    "name": "string"
  },
  "client": {
    "id": "uuid",
    "name": "string",
    "email": "string"
  }
}
```

## 6. Enums

### `UserRole`
- `admin`
- `owner`
- `player`

### `ReservationStatus`
- `pending`
- `confirmed`
- `cancelled`
- `expired`
- `completed`
- `no_show`

### `ReservationPaymentStatus`
- `pending`
- `paid`
- `failed`
- `refunded`

### `PaymentMethod`
- `cash`
- `pix`
- `credit_card`
- `debit_card`

### `PaymentStatus`
- `pending`
- `paid`
- `refunded`
- `failed`
- `cancelled`

### `MatchStatus`
- `scheduled`
- `confirmed`
- `in_progress`
- `finished`
- `cancelled`

### `MatchVisibility`
- `public`
- `private`
- `friends`

### `SkillLevel`
- `beginner`
- `intermediate`
- `advanced`
- `professional`

## 7. Notificações (Notify Me API)

Notificações são enviadas via HTTP POST para a Notify Me API.

**Variáveis de ambiente:**
- `NOTIFY_API_URL` — URL base da API (ex: `https://notify-me.vercel.app`)
- `NOTIFY_API_KEY` — Chave de autenticação (header `X-API-Key`)

### 7.1 `verification`
Disparado em `POST /auth/register`.
→ `POST /api/arena-manager/verification`

Payload:

```json
{
  "email": "user@dominio.com",
  "token": "email-verification-token"
}
```

### 7.2 `password_reset`
Disparado em `POST /auth/forgot-password` (quando e-mail existe).
→ `POST /api/arena-manager/password-reset`

Payload:

```json
{
  "email": "usuario@dominio.com",
  "token": "token-de-reset"
}
```

### 7.3 `owner_promotion`
Disparado ao criar arena para usuario `player`.
→ `POST /api/arena-manager/owner-promotion`

### 7.4 `new_court`
Disparado ao criar quadra.
→ `POST /api/arena-manager/new-court`

### 7.5 `reservation_created`
Disparado ao criar reserva (recipient owner/client).
→ `POST /api/arena-manager/reservation-created`

### 7.6 `reservation_cancelled`
Disparado ao cancelar reserva (recipient owner/client).
→ `POST /api/arena-manager/reservation-cancelled`

## 8. Matriz rapida de status HTTP

- `200` sucesso
- `201` criado
- `204` sem conteudo (cancelamento de reserva)
- `400` dados invalidos / regra de negocio
- `401` nao autorizado (token/credenciais)
- `403` proibido (sem permissao)
- `404` recurso nao encontrado
- `409` conflito (duplicidade/conflito de horario)
- `500` erro interno

## 9. Observacoes importantes do estado atual do codigo

- `GET /auth/verify-email`, `GET /auth/reset-password` e `POST /auth/reset-password-form` retornam HTML, nao JSON.
- `GET /reservations/` esta sem autenticacao no codigo atual.
- Existe resposta de erro SQL com campo `fiels` (typo) no payload.
- Os textos de erro/sucesso estao documentados conforme strings atuais do codigo.
