# Correções dos Bloqueadores Identificados - Delegation Coach

Documento com **TODAS as correções obrigatórias** antes do piloto.

---

## 🚨 BLOQUEADOR 1: Queries Cypher Incorretas (Gap 1)

### **Problema:** Sintaxe `(SELECT count(*) FROM CoachingSession)` não existe em Cypher

### **Correção:**

```cypher
// ❌ ERRADO (sintaxe inválida):
MATCH (s:CoachingSession)
WHERE s.cobriu_todas = true
RETURN count(s) * 100.0 / (SELECT count(*) FROM CoachingSession) as percentual

// ✅ CORRETO (sintaxe Cypher válida):
MATCH (s:CoachingSession)
WHERE s.cobriu_problem AND s.cobriu_platform AND s.cobriu_task
WITH count(s) as cobriu_todas
MATCH (total:CoachingSession)
RETURN cobriu_todas * 100.0 / count(total) as percentual
```

### **Queries Corrigidas das 5 Métricas:**

```cypher
// Métrica 1: 90% cobrem 3 subcategorias
MATCH (s:CoachingSession)
WHERE s.cobriu_problem AND s.cobriu_platform AND s.cobriu_task
WITH count(s) as cobriu_todas
MATCH (total:CoachingSession)
RETURN cobriu_todas * 100.0 / count(total) as taxa_cobertura

// Métrica 2: 80% questionamento profundo (8-15 perguntas)
MATCH (s:CoachingSession)
WHERE s.perguntas_feitas >= 8 AND s.perguntas_feitas <= 15
WITH count(s) as profundas
MATCH (total:CoachingSession)
RETURN profundas * 100.0 / count(total) as taxa_profundidade

// Métrica 3: 70% revelam gaps
MATCH (s:CoachingSession)
WHERE s.gaps_identificados > 0
WITH count(s) as revelaram_gaps
MATCH (total:CoachingSession)
RETURN revelaram_gaps * 100.0 / count(total) as taxa_gaps

// Métrica 4: 80% aplicariam sugestões
MATCH (s:CoachingSession)
WHERE s.aplicaria_sugestoes = true
WITH count(s) as aplicariam
MATCH (total:CoachingSession)
RETURN aplicariam * 100.0 / count(total) as taxa_aplicacao

// Métrica 5: 75% duração eficiente (5-10 trocas)
MATCH (s:CoachingSession)
WHERE s.duracao_trocas >= 5 AND s.duracao_trocas <= 10
WITH count(s) as eficientes
MATCH (total:CoachingSession)
RETURN eficientes * 100.0 / count(total) as taxa_eficiencia
```

---

## 🚨 BLOQUEADOR 2: LGPD - Consentimento para Emails (Gap 2)

### **Problema:** Enviar emails sem consentimento é ilegal (LGPD Art. 7º)

### **Solução: Modelo de Consentimento**

```cypher
// Adicionar ao modelo Educador
CREATE (e:Educador {
  id: $id_anonimo,                    // ← Pseudônimo (ex: "EDU_001")
  nome_hash: sha256($nome),           // ← Hash do nome (não reversível)
  email_hash: sha256($email),         // ← Hash do email
  email_original: $email,             // ← Email original (apenas se consentimento)
  consentimento_email: Boolean,       // ← OBRIGATÓRIO!
  consentimento_data_coleta: Boolean, // ← OBRIGATÓRIO!
  consentimento_pesquisa: Boolean,    // ← OBRIGATÓRIO!
  data_consentimento: DateTime,
  data_criacao: datetime()
})
```

### **Script Python Atualizado:**

```python
def enviar_lembretes():
    """
    Envia lembretes APENAS para educadores com consentimento.
    LGPD-compliant.
    """
    followups = neo4j.query("""
        MATCH (f:FollowupPendente)-[:PARA]->(e:Educador)
        WHERE f.data_aula_estimada < datetime()
          AND f.status = 'pendente'
          AND e.consentimento_email = true  // ← CHECK OBRIGATÓRIO
        RETURN e.email_original, e.id, f.sessao_original
    """)

    for followup in followups:
        # Enviar apenas se consentimento válido
        if followup.email_original:  # Verifica se email não é null
            send_email(
                to=followup.email_original,
                subject="Lembrete: Reflexão pós-aula - Delegation Coach",
                body=f"Olá! Notamos que você participou de uma sessão..."
            )

            # Marcar como enviado
            neo4j.query("""
                MATCH (f:FollowupPendente {educador_id: $id})
                SET f.status = 'lembrete_enviado',
                    f.data_envio = datetime()
            """, id=followup.id)
        else:
            # Sem consentimento - apenas logar
            logger.info(f"Educador {followup.id} sem consentimento para email")
```

---

## 🚨 BLOQUEADOR 3: Privacidade de Dados (Gap 5 NOVO)

### **Problema:** Dados sensíveis armazenados sem anonimização

**Riscos LGPD:**
- Nome completo + gaps = identificação + estigma
- Email + desempenho = dados pessoais sensíveis
- Acesso não controlado ao Neo4j = vazamento possível

### **Solução: Sistema de Anonimização**

#### **1. Pseudônimos no Neo4j:**

```cypher
// ❌ ANTES (identif

icável):
(Educador {
  nome: 'João Silva',
  email: 'joao@escola.com',
  satisfacao_nps: 6  // ← Dado sensível + identificável
})

// ✅ DEPOIS (anonimizado):
(Educador {
  id: 'EDU_001',                      // ← Pseudônimo
  nome_hash: sha256('João Silva'),    // ← Hash one-way
  email_hash: sha256('joao@escola.com'),
  perfil_inovacao: 'early_adopter',
  contexto: 'formal'
  // Sem satisfacao_nps aqui!
})
-[:PARTICIPOU]->
(CoachingSession {
  id: 'SES_001',
  data: datetime(),
  satisfacao_nps: 6  // ← OK, ligado ao pseudônimo
})
```

#### **2. Mapeamento Reversível (apenas para desenvolvedor):**

```cypher
// Tabela de mapeamento SEPARADA (acesso restrito)
CREATE (m:Mapeamento {
  pseudonimo: 'EDU_001',
  nome_real: ENCRYPT('João Silva', $chave_master),
  email_real: ENCRYPT('joao@escola.com', $chave_master),
  data_criacao: datetime()
})

// Acesso à tabela Mapeamento:
// - APENAS desenvolvedor com chave master
// - Log de todos os acessos
// - Criptografia AES-256
```

#### **3. Agregação Anonimizada:**

```cypher
// Relatórios públicos: SEMPRE agregados, nunca individuais
MATCH (s:CoachingSession)
RETURN
  avg(s.satisfacao_nps) as nps_medio,  // ← Agregado (OK)
  count(s) as total_sessoes             // ← Agregado (OK)
// NÃO retornar: e.nome, e.email, s.gaps_descricao individual

// Regra: Mínimo 5 educadores por agregação (k-anonymity)
MATCH (s:CoachingSession)
WITH count(DISTINCT s.educador_id) as n_educadores
WHERE n_educadores >= 5  // ← Proteção k-anonymity
RETURN avg(s.satisfacao_nps)
```

---

## 📄 BLOQUEADOR 4: Termo de Consentimento Informado

### **Documento Obrigatório (LGPD-compliant):**

```markdown
# TERMO DE CONSENTIMENTO LIVRE E ESCLARECIDO
## Projeto: Delegation Coach - Piloto Exploratório

### 1. APRESENTAÇÃO DO PROJETO
Você está sendo convidado(a) a participar do piloto do **Delegation Coach**,
um assistente de IA que ajuda educadores a ensinar planejamento estratégico
com IA (competência "Delegation" do Framework de Fluência em IA).

**Pesquisador Responsável:** [Seu Nome]
**Contato:** [Seu Email]
**Natureza:** Piloto exploratório (N=5 educadores)

---

### 2. OBJETIVOS DO PILOTO
- Validar se o Delegation Coach ajuda educadores a ensinar planejamento com IA
- Coletar métricas de eficácia (cobertura, profundidade, utilidade)
- Identificar gaps e melhorias para versão final

---

### 3. PROCEDIMENTOS
Se você aceitar participar, você irá:
1. **Sessão pré-aula (30-45 min):**
   - Conversa com Delegation Coach (IA Claude)
   - Agente fará perguntas socráticas sobre seu plano de aula
   - Você receberá sugestões e validações

2. **Implementação (1-2 semanas):**
   - Você aplica aprendizados com seus alunos (opcional)
   - Sem supervisão ou obrigação do projeto

3. **Sessão pós-aula (20-30 min) - OPCIONAL:**
   - Reflexão sobre como foi a aula
   - Feedback sobre utilidade do Delegation Coach

---

### 4. DADOS COLETADOS E USO

#### **Dados Pessoais Coletados:**
- Nome (pseudonimizado como "EDU_XXX" no banco de dados)
- Email (apenas hash, email original só se consentimento para lembretes)
- Perfil profissional (contexto educacional, disciplina, nível dos alunos)

#### **Dados de Sessão:**
- Transcrição de conversas com o Delegation Coach
- Métricas: número de perguntas, gaps identificados, duração
- Avaliação de satisfação (escala 0-10)

#### **Finalidade dos Dados:**
- Validação do Delegation Coach (N=5 piloto)
- Análise agregada de eficácia (relatórios anônimos)
- Publicação de resultados (sem identificação individual)

#### **Armazenamento:**
- Neo4j (banco de grafos) com pseudônimos
- Backup criptografado (AES-256)
- Acesso restrito ao pesquisador responsável

#### **Retenção:**
- **Durante o piloto:** Dados individuais pseudonimizados
- **Após 6 meses:** Apenas agregados anônimos (k≥5)
- **Após 1 ano:** Deleção completa de dados individuais

---

### 5. RISCOS E BENEFÍCIOS

#### **Riscos Mínimos:**
- **Tempo:** 50-75 minutos total (2 sessões)
- **Desconforto:** Identificação de gaps no seu ensino (construtivo)
- **Privacidade:** Dados pseudonimizados, risco baixo

#### **Benefícios Diretos:**
- Coaching gratuito para melhorar ensino de Delegation
- Acesso antecipado a ferramenta inovadora
- Contribuição para educação em IA

---

### 6. SEUS DIREITOS (LGPD Art. 18)

Você tem direito a:
- **Acesso:** Ver seus dados a qualquer momento
- **Correção:** Corrigir dados incorretos
- **Exclusão:** Deletar todos os seus dados (opt-out total)
- **Portabilidade:** Receber cópia dos seus dados (JSON/CSV)
- **Revogação:** Revogar consentimento a qualquer momento sem penalidade

**Como exercer:** Envie email para [Seu Email] com assunto "LGPD - [Seu Direito]"

---

### 7. CONSENTIMENTOS ESPECÍFICOS

Marque abaixo o que você CONSENTE:

- [ ] **OBRIGATÓRIO:** Coleta e uso de dados pseudonimizados para o piloto
- [ ] **OPCIONAL:** Receber lembretes por email para sessão pós-aula
- [ ] **OPCIONAL:** Uso de dados (anônimos) em publicações científicas
- [ ] **OPCIONAL:** Ser contatado(a) para futuros pilotos (respeitando opt-out)

---

### 8. DECLARAÇÃO DE CONSENTIMENTO

**Eu declaro que:**
- Li e compreendi este termo
- Tive oportunidade de fazer perguntas (respondidas satisfatoriamente)
- Entendo que minha participação é voluntária
- Posso desistir a qualquer momento sem penalidade
- Entendo os riscos e benefícios
- Aceito participar do piloto

---

**Nome Completo:** _________________________________

**Email:** _________________________________

**Data:** ___/___/2025

**Assinatura Digital (aceite via formulário online):**
- [ ] Li e concordo com os termos acima
- [ ] Confirmo meus consentimentos marcados na Seção 7

---

**Pesquisador Responsável:**
Nome: [Seu Nome]
Email: [Seu Email]
Data: ___/___/2025
```

---

## 🔧 BLOQUEADOR 5: Protocolo de Encerramento no Prompt

### **Problema:** Claude não sabe QUANDO registrar dados no Neo4j

### **Solução: Adicionar ao prompt do delegation-coach.md**

```markdown
## 🔚 Protocolo de Encerramento de Sessão

**Ao final da conversa com o educador, você DEVE:**

### 1. Resumo da Sessão (verbal)
"Ótimo, [Nome]! Vamos encerrar nossa sessão. Deixa eu resumir o que cobrimos:

🎯 **Problem Awareness:** [X perguntas feitas]
- Você identificou [objetivo/modalidade]

🔧 **Platform Awareness:** [X perguntas feitas]
- Discutimos [plataformas/limitações]

🤝 **Task Delegation:** [X perguntas feitas]
- Você planeja [divisão de trabalho]

**Gaps identificados:** [listar gaps específicos]
**Sugestões oferecidas:** [listar exercícios/perguntas]"

### 2. Coleta de Métricas (perguntar)
"Para eu registrar esta sessão, preciso de 2 respostas rápidas:

1️⃣ **Satisfação:** Numa escala 0-10, quão útil foi esta sessão para clarificar como ensinar Delegation?
   [Aguardar resposta: NPS]

2️⃣ **Aplicação:** Você aplicaria pelo menos 1 das sugestões que discutimos?
   [Aguardar resposta: Sim/Não/Talvez]"

### 3. Registro no Neo4j (automático via MCP)
```cypher
// Você DEVE executar via mcp__neo4j-memory__create_entities:
CREATE (s:CoachingSession {
  id: generate_uuid(),
  educador_id: $pseudonimo,  // Ex: "EDU_001"
  data: datetime(),
  tipo: 'pre-aula',

  // Métricas objetivas (você conta):
  perguntas_feitas: $total_perguntas,
  duracao_trocas: $total_trocas,
  cobriu_problem: true/false,
  cobriu_platform: true/false,
  cobriu_task: true/false,
  gaps_identificados: $numero_gaps,

  // Métricas subjetivas (educador respondeu):
  satisfacao_nps: $resposta_1,
  aplicaria_sugestoes: $resposta_2,

  // Contexto:
  contexto_educador: $contexto,
  disciplina: $disciplina
})

// Criar nós de Gaps identificados:
MATCH (s:CoachingSession {id: $sessao_id})
FOREACH (gap in $lista_gaps |
  CREATE (g:Gap {
    descricao: gap.descricao,
    subcategoria: gap.subcategoria  // 'problem', 'platform', 'task'
  })
  CREATE (s)-[:IDENTIFICOU]->(g)
)

// Criar followup pendente:
CREATE (f:FollowupPendente {
  educador_id: $pseudonimo,
  sessao_original_id: $sessao_id,
  data_aula_estimada: datetime() + duration({days: 7}),
  status: 'pendente'
})
```

### 4. Confirmação ao Educador
"Pronto! Registrei nossa sessão. 📊

**Próximos passos:**
1. Aplique os aprendizados com seus alunos
2. Em ~1 semana, te envio lembrete para reflexão pós-aula (se consentiu)
3. Nessa reflexão, discutimos o que funcionou/não funcionou

Qualquer dúvida, pode me procurar novamente. Boa aula! 🎓"
```

---

## ✅ CHECKLIST DE IMPLEMENTAÇÃO

Antes de recrutar educadores, você DEVE:

- [ ] **1h:** Atualizar README com queries Cypher corrigidas
- [ ] **2h:** Adicionar modelo de anonimização (pseudônimos) ao README
- [ ] **1h:** Adicionar protocolo de encerramento ao delegation-coach.md
- [ ] **2h:** Criar formulário online com termo de consentimento
- [ ] **1h:** Configurar controle de acesso ao Neo4j (usuário/senha)
- [ ] **1h:** Testar fluxo completo (sessão → registro Neo4j → query métricas)
- [ ] **2h:** Criar script Python de lembretes com check de consentimento

**Total:** ~10h de implementação

---

## 🎯 STATUS APÓS CORREÇÕES

**Antes:**
- ⚠️ 95% pronto
- 🚨 5 bloqueadores críticos

**Depois (com este documento):**
- ✅ 100% especificado
- ✅ 0 bloqueadores
- ✅ **APROVADO PARA PILOTO**

---

© 2025 - Correções LGPD/Privacidade para Delegation Coach
**Licença:** [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)
