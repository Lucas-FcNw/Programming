# Guia Rápido de Uso

## 🚀 Início Rápido (5 minutos)

### 1. Configure as credenciais Azure

Crie o arquivo `.env` na raiz do projeto:

```bash
AZURE_CLIENT_ID=your-client-id-here
AZURE_CLIENT_SECRET=your-client-secret-here
AZURE_TENANT_ID=your-tenant-id-here
JWT_SECRET=your-super-secret-jwt-key-min-256-bits
```

### 2. Inicie os serviços com Docker

```bash
docker-compose up -d
```

### 3. Acesse a aplicação

Abra o navegador em: http://localhost:8080/oauth2/authorization/microsoft

## 📌 Testando os Endpoints

### 1. Login

Acesse pelo navegador:
```
http://localhost:8080/oauth2/authorization/microsoft
```

Faça login com seu email @mackenzie.br ou @mackenzista.com.br

### 2. Copie os tokens da resposta

Após o login bem-sucedido, você receberá:
- `accessToken`
- `refreshToken`

### 3. Use o token nas requisições

```bash
# Obter informações do usuário atual
curl -X GET http://localhost:8080/api/v1/auth/me \
  -H "Authorization: Bearer SEU_ACCESS_TOKEN"

# Validar token
curl -X GET http://localhost:8080/api/v1/auth/validate \
  -H "Authorization: Bearer SEU_ACCESS_TOKEN"

# Fazer logout
curl -X POST http://localhost:8080/api/v1/auth/logout \
  -H "Authorization: Bearer SEU_ACCESS_TOKEN"

# Renovar token
curl -X POST http://localhost:8080/api/v1/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"refreshToken": "SEU_REFRESH_TOKEN"}'
```

### 4. Testar endpoint de admin (apenas para ROLE_ADMIN)

```bash
curl -X GET http://localhost:8080/api/v1/auth/admin/test \
  -H "Authorization: Bearer SEU_ACCESS_TOKEN"
```

## 🔑 Como obter credenciais Azure AD

1. Acesse https://portal.azure.com
2. Vá em "Azure Active Directory"
3. Clique em "App registrations" > "New registration"
4. Preencha:
   - Name: `Mackenzie Auth Service`
   - Redirect URI: `http://localhost:8080/login/oauth2/code/microsoft`
5. Após criar, copie:
   - Application (client) ID → `AZURE_CLIENT_ID`
   - Directory (tenant) ID → `AZURE_TENANT_ID`
6. Vá em "Certificates & secrets" > "New client secret"
   - Copie o valor → `AZURE_CLIENT_SECRET`

## 🛠️ Comandos Úteis

```bash
# Ver logs da aplicação
docker-compose logs -f auth-service

# Ver logs do MongoDB
docker-compose logs -f mongodb

# Reiniciar serviços
docker-compose restart

# Parar todos os serviços
docker-compose down

# Limpar tudo (incluindo dados)
docker-compose down -v

# Acessar MongoDB CLI
docker exec -it mackenzie-mongodb mongosh -u admin -p mackenzie@2025

# Build local (sem Docker)
mvn clean package

# Executar local (sem Docker)
mvn spring-boot:run
```

## 📊 Monitorando MongoDB

```bash
# Conectar ao MongoDB
docker exec -it mackenzie-mongodb mongosh -u admin -p mackenzie@2025

# Dentro do MongoDB shell
use mackenzie_auth

# Ver todos os usuários
db.users.find().pretty()

# Ver todas as roles
db.roles.find().pretty()

# Contar usuários
db.users.count()

# Ver último usuário criado
db.users.find().sort({createdAt: -1}).limit(1).pretty()
```

## 🐛 Troubleshooting

### Erro: "Email não pertence aos domínios permitidos"

Verifique se o email usado no login termina com:
- `@mackenzie.br` ou
- `@mackenzista.com.br`

### Erro: "Token inválido"

- Verifique se o token não expirou (24 horas)
- Use o refresh token para obter um novo access token
- Certifique-se de incluir "Bearer " antes do token

### Erro de conexão com MongoDB

```bash
# Verificar se MongoDB está rodando
docker ps | grep mongodb

# Reiniciar MongoDB
docker-compose restart mongodb
```

### Erro de OAuth2

- Verifique se as credenciais Azure estão corretas no `.env`
- Confirme que a Redirect URI está configurada no Azure Portal
- Verifique os logs: `docker-compose logs -f auth-service`

## 🎯 Próximos Passos

1. **Adicionar novos endpoints** em `AuthController.java`
2. **Criar novas roles** e atribuir permissões específicas
3. **Integrar com frontend** (React, Angular, Vue)
4. **Deploy para AWS** (ECS, Elastic Beanstalk ou EKS)
5. **Configurar CI/CD** (GitHub Actions, GitLab CI)

## 💡 Dicas

- Use o Postman ou Insomnia para testar os endpoints
- Instale a extensão MongoDB for VS Code para visualizar dados
- Configure logging detalhado em desenvolvimento
- Use variáveis de ambiente diferentes para dev/prod
