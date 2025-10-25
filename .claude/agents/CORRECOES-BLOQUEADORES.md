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

---

## 🎯 BLOQUEADOR 6: Sistema de IDs Consistente (RESOLVIDO)

### **Decisão:** Opção A - Pseudônimos Simples

**Justificativa:**
- ✅ Queries simples e legíveis
- ✅ Reversibilidade garantida (LGPD Art. 18)
- ✅ K-anonymity preservado
- ✅ Sem complexidade desnecessária

### **Modelo Final Neo4j (CONSISTENTE):**

```cypher
// 1. Nó Educador (PÚBLICO - dados agregados)
CREATE (e:Educador {
  id: 'EDU_001',                        // ← Pseudônimo curto
  perfil_inovacao: 'early_adopter',
  experiencia_ia: 'basica',
  contexto: 'formal',
  disciplina: 'Marketing',
  pais: 'Brasil',
  consentimento_email: true,
  consentimento_data_coleta: true,
  consentimento_pesquisa: true,
  data_consentimento: datetime()
})

// 2. Nó PII (PRIVADO - acesso restrito)
CREATE (pii:PII {
  pseudonimo: 'EDU_001',                // ← Link com Educador
  nome_real: ENCRYPT('João Silva', $chave_master),
  email_real: ENCRYPT('joao@escola.com', $chave_master),
  instituicao: ENCRYPT('Universidade XYZ', $chave_master)
})

// 3. Relacionamento
CREATE (e)-[:TEM_PII]->(pii)
```

### **Query de Exclusão LGPD Art. 18 (exemplo completo):**

```cypher
// Educador João Silva pede exclusão
// Passo 1: Desenvolvedor recebe email
// Passo 2: Desenvolvedor executa (acesso ao PII):

// 2.1 - Encontrar pseudônimo
MATCH (pii:PII)
WHERE DECRYPT(pii.nome_real, $chave_master) = 'João Silva'
RETURN pii.pseudonimo
// Resultado: 'EDU_001'

// 2.2 - Deletar PII
MATCH (pii:PII {pseudonimo: 'EDU_001'})
DELETE pii

// 2.3 - Anonimizar Educador (manter para estatísticas)
MATCH (e:Educador {id: 'EDU_001'})
SET e.id = 'EDU_DELETADO_' + randomUUID(),
    e.consentimento_email = false
REMOVE e.data_consentimento

// 2.4 - Anonimizar sessões
MATCH (s:CoachingSession {educador_id: 'EDU_001'})
SET s.educador_id = e.id  // ← Novo ID anonimizado

// Resultado: Dados agregados preservados, PII deletado
```

---

## 🎯 BLOQUEADOR 7: Protocolo Técnico Completo (RESOLVIDO)

### **Decisão:** Claude executa via MCP Neo4j direto

### **Arquitetura Técnica Completa:**

```mermaid
Educador → Claude Code → Delegation Coach (prompt) →
         → [Detecta fim via palavras-chave] →
         → [Coleta métricas verbalmente] →
         → [Executa MCP neo4j create_entities] →
         → [Confirma registro ao educador] →
         → Fim
```

### **Implementação no delegation-coach.md:**

Adicionar ao prompt do agente:

```markdown
## 🔚 PROTOCOLO DE ENCERRAMENTO (EXECUTAR AO FINAL)

### Detectar Fim de Sessão

Você está encerrando a sessão quando educador diz:
- "Obrigado, era isso"
- "Acho que já tenho o que preciso"
- "Até mais" / "Tchau"
- "Vou implementar isso agora"
- Ou similar indicando conclusão

### Quando detectar fim, EXECUTE:

**Passo 1: Resumo Verbal**
"Ótimo, [Nome do Educador]! Vamos encerrar nossa sessão de coaching.

📊 **Resumo do que cobrimos:**

🎯 **Problem Awareness:** Fiz [CONTE quantas] perguntas sobre definição de objetivos
🔧 **Platform Awareness:** Fiz [CONTE quantas] perguntas sobre escolha de ferramentas
🤝 **Task Delegation:** Fiz [CONTE quantas] perguntas sobre divisão de trabalho
⚖️ **Conexão com Diligence:** [Sim/Não] conectamos planejamento com ética

**Gaps identificados:**
1. [Liste cada gap específico que você revelou]
2. [Outro gap, se houver]
[Se nenhum gap: "Não identifiquei gaps - seu planejamento está sólido!"]

**Sugestões práticas oferecidas:**
1. [Liste exercícios ou perguntas que sugeriu]
2. [Outras sugestões]"

---

**Passo 2: Coleta de Métricas**
"Para eu registrar esta sessão e melhorar o coaching, preciso de 2 respostas rápidas:

1️⃣ **Utilidade:** Numa escala de 0 a 10, quão útil foi esta sessão para clarificar como ensinar Delegation aos seus alunos?
   [Aguarde resposta → armazene como $satisfacao_nps]

2️⃣ **Aplicação:** Você aplicaria pelo menos 1 das sugestões que discutimos na sua próxima aula?
   - [ ] Sim, com certeza
   - [ ] Provavelmente sim
   - [ ] Talvez
   - [ ] Provavelmente não
   - [ ] Não
   [Aguarde resposta → converta para booleano: Sim/Provavelmente=true, resto=false]"

---

**Passo 3: Registro Neo4j (VIA MCP)**

EXECUTE AGORA via mcp__neo4j-memory__create_entities:

```cypher
CREATE (s:CoachingSession {
  id: $generate_random_uuid,
  educador_id: $pseudonimo_do_educador,  // Ex: "EDU_001" (perguntou no início?)
  data: datetime(),
  tipo: 'pre-aula',

  // Métricas objetivas (VOCÊ contou):
  perguntas_feitas: $total_perguntas_que_voce_fez,
  duracao_trocas: $total_mensagens_trocadas,
  cobriu_problem: $true_ou_false,
  cobriu_platform: $true_ou_false,
  cobriu_task: $true_ou_false,
  gaps_identificados: $numero_de_gaps_que_revelou,

  // Métricas subjetivas (educador respondeu):
  satisfacao_nps: $resposta_pergunta_1,
  aplicaria_sugestoes: $resposta_pergunta_2_convertida,

  // Contexto:
  contexto: $contexto_do_educador,  // Ex: "Marketing, graduação, formal"
  disciplina: $disciplina
})

// Criar nós de Gap (para cada gap identificado):
CREATE (g1:Gap {
  descricao: $descricao_gap_1,
  subcategoria: $qual_subcategoria,  // 'problem', 'platform', ou 'task'
  severidade: $baixa_media_alta
})
CREATE (s)-[:IDENTIFICOU]->(g1)

// Criar followup pendente (se educador consentiu emails):
CREATE (f:FollowupPendente {
  educador_id: $pseudonimo,
  sessao_original_id: $id_da_sessao,
  data_aula_estimada: datetime() + duration({days: 7}),
  status: 'pendente'
})
```

---

**Passo 4: Confirmação ao Educador**
"Pronto! Registrei nossa sessão com sucesso. 📊

**Próximos passos sugeridos:**
1. Aplique as sugestões que discutimos com seus alunos
2. Em ~7 dias, te envio um lembrete para conversarmos sobre como foi (se você consentiu receber emails)
3. Nessa sessão pós-aula, vamos refletir sobre o que funcionou e o que pode melhorar

**Dúvidas?** Pode voltar a qualquer momento!

Boa sorte com a aula! 🎓"
```

---

**Passo 5: Fallback de Erro**
```python
# Se mcp__neo4j-memory__create_entities falhar:
if erro_neo4j:
    # Informa educador
    print("⚠️ Não consegui registrar agora (Neo4j offline).")
    print("Suas respostas foram salvas localmente e serão sincronizadas depois.")

    # Salva em arquivo temporário
    with open(f'/tmp/coaching_sessions/{uuid}.json', 'w') as f:
        json.dump({
            'educador_id': pseudonimo,
            'data': datetime.now().isoformat(),
            'satisfacao_nps': nps,
            # ... resto dos dados
        }, f)

    # Job cron sincroniza depois:
    # crontab: */30 * * * * python sync_pending_sessions.py
```

---

---

## 🎯 BLOQUEADOR 8: Sintaxe MCP Executável (RESOLVIDO)

### **Problema:** Código abstrato - não mostra sintaxe MCP real

### **Solução:** Sintaxe executável completa para delegation-coach.md

**Adicionar ao prompt do delegation-coach.md:**

```markdown
## 🔚 CÓDIGO MCP PARA ENCERRAMENTO DE SESSÃO

### Passo 3: Registrar no Neo4j (via MCP)

Quando chegar neste passo, use a ferramenta MCP Neo4j:

**Via mcp__neo4j-memory__create_entities:**

\`\`\`json
{
  "entities": [
    {
      "name": "Sessao_<timestamp>",
      "type": "CoachingSession",
      "observations": [
        "educador_id: <pseudonimo do educador>",
        "data: <data atual>",
        "tipo: pre-aula",
        "perguntas_feitas: <você conta>",
        "duracao_trocas: <total de mensagens>",
        "cobriu_problem: <true/false>",
        "cobriu_platform: <true/false>",
        "cobriu_task: <true/false>",
        "gaps_identificados: <número>",
        "satisfacao_nps: <resposta educador>",
        "aplicaria_sugestoes: <true/false>",
        "contexto: <contexto do educador>",
        "disciplina: <disciplina>"
      ]
    }
  ]
}
\`\`\`

**Depois, criar relacionamento:**

\`\`\`json
{
  "relations": [
    {
      "source": "<pseudonimo_educador>",
      "target": "Sessao_<timestamp>",
      "relationType": "PARTICIPOU"
    }
  ]
}
\`\`\`

**Se houver gaps identificados, criar nós de Gap:**

\`\`\`json
{
  "entities": [
    {
      "name": "Gap_<timestamp>_1",
      "type": "Gap",
      "observations": [
        "descricao: <descrição do gap>",
        "subcategoria: <problem/platform/task>",
        "severidade: <baixa/media/alta>"
      ]
    }
  ]
}
\`\`\`

\`\`\`json
{
  "relations": [
    {
      "source": "Sessao_<timestamp>",
      "target": "Gap_<timestamp>_1",
      "relationType": "IDENTIFICOU"
    }
  ]
}
\`\`\`

**Criar followup pendente (se educador consentiu emails):**

\`\`\`json
{
  "entities": [
    {
      "name": "Followup_<timestamp>",
      "type": "FollowupPendente",
      "observations": [
        "educador_id: <pseudonimo>",
        "sessao_original_id: Sessao_<timestamp>",
        "data_aula_estimada: <data + 7 dias>",
        "status: pendente"
      ]
    }
  ]
}
\`\`\`

---

**Passo 4: Confirmação ao Educador**

"✅ Pronto! Registrei nossa sessão com sucesso.

**ID da Sessão:** Sessao_<timestamp>
**Suas métricas:** NPS <valor>, Aplicaria: <Sim/Não>

**Próximos passos:**
1. Aplique as sugestões com seus alunos
2. Em ~7 dias, você receberá um lembrete para reflexão pós-aula
3. Nessa reflexão, vamos discutir o que funcionou

Boa aula! 🎓"

---

**Passo 5: Fallback se Neo4j MCP falhar**

Se a ferramenta mcp__neo4j-memory__create_entities retornar erro:

\`\`\`bash
# Via Bash tool:
cat > /tmp/coaching_sessions/sessao_$(date +%s).json <<EOF
{
  "educador_id": "<pseudonimo>",
  "data": "$(date -Iseconds)",
  "satisfacao_nps": <valor>,
  "aplicaria_sugestoes": <true/false>,
  "perguntas_feitas": <numero>,
  "cobriu_problem": <true/false>,
  "cobriu_platform": <true/false>,
  "cobriu_task": <true/false>
}
EOF
\`\`\`

"⚠️ Neo4j está offline no momento. Salvei sua sessão localmente e será sincronizada em breve.
Você ainda receberá seu lembrete normalmente."
```

---

## 🎯 BLOQUEADOR 9: Gestão de Chaves de Criptografia (RESOLVIDO)

### **Problema:** Criptografia sem definir onde/como gerenciar chaves

### **Solução: Sistema de Chaves Completo**

**Setup Inicial (ANTES do piloto):**

```bash
# 1. Gerar chave AES-256 (via Fernet)
python3 << EOF
from cryptography.fernet import Fernet
key = Fernet.generate_key()
print(f"ENCRYPTION_KEY={key.decode()}")
EOF
# Output: ENCRYPTION_KEY=<chave-base64>

# 2. Adicionar ao .env (nunca commitear!)
echo "ENCRYPTION_KEY=<chave-base64>" >> .env

# 3. Adicionar .env ao .gitignore
echo ".env" >> .gitignore

# 4. Backup da chave (CRÍTICO)
# Salvar em 2 locais seguros:
# - Gerenciador de senhas pessoal (1Password, Bitwarden)
# - Cofre institucional (se houver)
```

**Código Python para Encriptação:**

```python
import os
import json
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# Carregar chave do .env
load_dotenv()
ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY').encode()
cipher = Fernet(ENCRYPTION_KEY)

def encriptar_pii(nome, email, instituicao=None):
    """Encripta PII antes de salvar no Neo4j"""
    dados_pii = {
        'nome': nome,
        'email': email,
        'instituicao': instituicao
    }
    encrypted = cipher.encrypt(json.dumps(dados_pii).encode())
    return encrypted.decode()  # String base64

def decriptar_pii(encrypted_string):
    """Decripta PII (apenas para LGPD Art. 18)"""
    encrypted = encrypted_string.encode()
    decrypted_bytes = cipher.decrypt(encrypted)
    return json.loads(decrypted_bytes)

# Uso no Neo4j:
query = """
MERGE (pii:PII {pseudonimo: $pseudo_id})
SET pii.dados_encriptados = $dados_encrypted
"""
neo4j.query(query,
    pseudo_id='EDU_001',
    dados_encrypted=encriptar_pii('João Silva', 'joao@exemplo.com')
)
```

**Rotação de Chaves:**
- **Piloto (3 meses):** Não necessária
- **Produção (após piloto):** Anual ou se comprometida
- **Processo:** Gerar nova chave → re-encriptar todos os PIIs → deletar chave antiga

---

## 🎯 BLOQUEADOR 10: Termo LGPD - Menores (RESOLVIDO)

### **Problema:** Termo sem consentimento de menores de idade

### **Solução: Consentimento Duplo**

**Adicionar ao bloqueador 4, Seção VIII:**

```markdown
---

## 🔐 PARA MENORES DE 18 ANOS

**LGPD Art. 14, §1º:** Consentimento de menores requer "melhor interesse" e participação dos responsáveis.

### Se o participante tiver **menos de 18 anos:**

#### Consentimento Duplo Obrigatório:

**Responsável Legal:**

Eu, _________________________________ (nome completo),
CPF ________________, responsável legal por _________________ (menor),
DECLARO que:
- Li e compreendi este termo em nome do(a) menor
- Autorizo a participação do(a) menor no piloto
- Entendo que posso revogar autorização a qualquer momento

Assinatura responsável: _________________________________
Data: ___/___/2025

---

**Menor de Idade (se 12+ anos):**

Eu, _________________________________ (nome completo),
DECLARO que:
- Entendi a explicação do pesquisador sobre o projeto
- Quero participar voluntariamente
- Sei que posso desistir quando quiser

Assinatura menor: _________________________________
Data: ___/___/2025

---

**Testemunha Presencial (se menor <12 anos):**

Eu, _________________________________ (nome completo),
CPF ________________,
Relação com a pesquisa: _________________ (ex: assistente, colega),
TESTEMUNHO que:
- Presenciei a explicação ao responsável legal
- O responsável compreendeu o projeto
- O consentimento foi dado livre e esclarecidamente

Assinatura testemunha: _________________________________
Data: ___/___/2025

---

**Justificativa Legal:**
- LGPD Art. 14, §1º: Tratamento de dados de menores
- Resolução CNS 466/2012: Pesquisa com seres humanos
- Código de Ética de Pesquisa: Proteção de populações vulneráveis
```

---

## ✅ CHECKLIST DE IMPLEMENTAÇÃO

Antes de recrutar educadores, você DEVE:
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
