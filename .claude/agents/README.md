# Delegation Coach - Agente de Coaching para Educadores

Coach especializado em ensinar **Delegation** - a fase de planejamento do Framework de Fluência em IA.

---

## 🎯 O que é o Delegation Coach?

Um assistente que usa **questionamento socrático** para ajudar educadores a garantir que seus alunos estão aprendendo a **planejar antes de usar IA**.

### As 3 Perguntas Fundamentais que Este Agente Ensina:

1. 🎯 **"O que estou tentando realizar?"** (Problem Awareness)
2. 🔧 **"Quais sistemas de IA estão disponíveis?"** (Platform Awareness)
3. 🤝 **"Como divido o trabalho entre mim e a IA?"** (Task Delegation)

---

## 📊 Decisões de Delegation na Criação do Agente

### 🔧 Por que Claude Code?
- **Decisão:** Sempre usaremos Claude SDK (não comparamos outras plataformas)
- **Justificativa:**
  - ✅ Já temos plano pago do Claude SDK
  - ✅ Contexto longo (200k tokens) essencial para coaching profundo
  - ✅ Melhor em raciocínio socrático e nuanceado
  - ✅ Alinhamento ético da Anthropic com ensino de Diligence

### 🔒 Privacidade e Divulgação
- **Política:** Todas as conversas são públicas e podem ser divulgadas
- **Transparência:** Educadores são informados que o agente é para fins educacionais
- **Dados sensíveis:** Educadores devem evitar compartilhar informações identificáveis de alunos

### 💰 Sustentabilidade
- **Custo:** Incluído no plano pago do Claude SDK
- **Manutenção:** Responsabilidade do criador do projeto
- **Escalabilidade:** Suportada pela infraestrutura existente

---

## 🔍 Alternativas Consideradas

### **Plataformas Avaliadas:**

#### **GPT-4 / ChatGPT**
- **Prós:**
  - Mais acessível (educadores podem ter conta própria)
  - Interface web familiar
  - GPTs customizados facilitam compartilhamento
- **Contras:**
  - Contexto menor (128k vs 200k tokens)
  - Menos forte em raciocínio socrático profundo
  - Alinhamento ético menos evidente
- **Decisão:** ❌ Descartado - contexto longo é crítico para coaching profundo com múltiplas trocas

#### **Google Gemini**
- **Prós:**
  - Contexto ainda maior (1M+ tokens)
  - Multimodal nativo (educador poderia anexar planos de aula)
  - Integração com Google Workspace
- **Contras:**
  - Menos testado para coaching socrático
  - API menos madura que Anthropic
  - Histórico de alucinações em respostas longas
- **Decisão:** ❌ Descartado - maturidade do Claude em conversas longas é superior

#### **Modelos Locais (Ollama/LM Studio)**
- **Prós:**
  - Privacidade total (dados não saem do dispositivo)
  - Custo zero após setup
  - Controle completo sobre modelo
- **Contras:**
  - Requer setup técnico complexo
  - Modelos menores (<70B params) não têm qualidade suficiente
  - Inacessível para educadores sem background técnico
- **Decisão:** ❌ Descartado - barreira técnica muito alta para público-alvo

### **Modalidades Avaliadas:**

#### **Guia Estático (Checklist/PDF)**
- **Prós:**
  - Custo zero
  - Sempre disponível offline
  - Sem dependência de API
- **Contras:**
  - Sem adaptação ao contexto específico do educador
  - Não provoca reflexão através de perguntas
  - Educador pode pular seções sem validação
- **Decisão:** ❌ Descartado - interação socrática é núcleo da proposta de valor

#### **Fórum de Discussão / Comunidade**
- **Prós:**
  - Educadores aprendem uns com os outros
  - Casos reais compartilhados
  - Networking entre educadores
- **Contras:**
  - Não escala (depende de moderadores)
  - Feedback não é imediato
  - Qualidade varia muito
- **Decisão:** ❌ Descartado - pode complementar no futuro, mas não substitui coaching individual

#### **Agente Conversacional (Claude)**
- **Prós:**
  - Adaptação ao contexto específico do educador
  - Questionamento socrático profundo
  - Disponibilidade 24/7
  - Escalável sem perda de qualidade
- **Contras:**
  - Requer acesso ao Claude SDK
  - Custo por sessão (coberto pelo plano)
  - Não substitui comunidade de prática
- **Decisão:** ✅ **ESCOLHIDO** - melhor equilíbrio entre qualidade, escalabilidade e adaptação

### **Estratégias Híbridas Consideradas:**

#### **Modelo Menor + Claude (fallback)**
- **Avaliado:** Usar Haiku para perguntas simples, Sonnet para análise profunda
- **Decisão:** ⚠️ **FUTURO** - válido para otimizar custos após validação inicial

---

## 📊 Métodos de Coleta de Métricas

| Métrica | Método de Coleta | Responsável | Ferramenta | Quando |
|---------|------------------|-------------|------------|--------|
| **90% cobrem 3 subcategorias** | Checklist automático ao fim da sessão | Agente | Template no prompt final | Ao fim de cada sessão |
| **80% questionamento profundo** | Contador de perguntas + análise de padrão | Sistema | Log de mensagens | Pós-sessão (automático) |
| **70% revelam gaps** | Registro de gaps identificados durante conversa | Agente | Seção específica no output final | Ao fim de cada sessão |
| **80% aplicariam sugestões** | Pergunta direta escala 1-5 + justificativa | Educador | Formulário pós-sessão | Após sessão (manual) |
| **75% duração 5-10 trocas** | Contador de mensagens (educador + agente) | Sistema | Log de mensagens | Pós-sessão (automático) |

### **Templates de Coleta:**

#### **Checklist Pós-Sessão (Agente preenche automaticamente):**
```markdown
## Resumo da Sessão

### Cobertura das 3 Subcategorias:
- [ ] Problem Awareness: X perguntas feitas
- [ ] Platform Awareness: X perguntas feitas
- [ ] Task Delegation: X perguntas feitas
- [ ] Conexão com Diligence: Sim/Não

### Gaps Identificados:
1. [Gap específico revelado]
2. [Outro gap se houver]

### Sugestões Práticas Oferecidas:
1. [Exercício ou pergunta sugerida]
2. [Outra sugestão]

Total de trocas: X mensagens
```

#### **Formulário Pós-Sessão (Educador preenche):**
```markdown
1. Você aplicaria pelo menos 1 sugestão do agente em sua aula?
   - [ ] Sim, com certeza
   - [ ] Provavelmente sim
   - [ ] Talvez
   - [ ] Provavelmente não
   - [ ] Não

2. Esta sessão ajudou a clarificar como ensinar Delegation?
   - Escala: 1 (nada) a 5 (muito)
   - [1] [2] [3] [4] [5]

3. Você usaria o Delegation Coach novamente?
   - [ ] Sim
   - [ ] Não
   - Por quê? _______________

4. Feedback aberto: _______________
```

---

## 🎭 Mitigação de Viés de Contexto

### **Viés Identificado:**
Agente pressupõe contexto educacional formal (universidades, escolas)

### **Impacto:**
Educadores de contextos não-formais (ONGs, autodidatas, treinamento corporativo) podem receber sugestões menos adequadas

### **Plano de Mitigação:**

#### **Fase 1: Teste Piloto**
- ✅ Incluir pelo menos **1 educador de contexto não-formal** nos 5 pilotos
- ✅ Incluir pelo menos **1 educador de país não-anglófono** (contexto cultural)
- ✅ Documentar adaptações necessárias

#### **Fase 2: Ajuste do Agente**
Se viés for confirmado, adicionar ao prompt do agente:
```markdown
**Antes de iniciar, pergunte ao educador:**
- "Qual o contexto do seu ensino?"
  (formal/não-formal, corporativo, autodidata, etc.)
- "Qual a faixa etária dos alunos?"
- "Há restrições de infraestrutura?"
  (acesso limitado a internet, dispositivos, etc.)
```

#### **Fase 3: Documentação**
Adicionar seção no README:
```markdown
## Adaptações por Contexto

### Educação Formal:
- [Exemplos específicos]

### Educação Não-Formal (ONGs):
- [Exemplos adaptados]

### Treinamento Corporativo:
- [Exemplos adaptados]

### Autodidatas:
- [Exemplos adaptados]
```

#### **Compromisso:**
- 🔄 Revisar viés a cada 10 sessões
- 📝 Documentar casos de inadequação
- 🔧 Ajustar prompt quando padrão emergir

---

## ✅ Critérios de Sucesso (Como Medir Eficácia)

### **Métrica 1: Cobertura Completa das 3 Subcategorias**
**Objetivo:** 100% das sessões devem cobrir Problem, Platform e Task Awareness

**Como medir:**
- [ ] Agente fez pelo menos 2 perguntas sobre Problem Awareness?
- [ ] Agente fez pelo menos 2 perguntas sobre Platform Awareness?
- [ ] Agente fez pelo menos 2 perguntas sobre Task Delegation?
- [ ] Agente conectou com Diligence (responsabilidade ética)?

**Meta:** 4/4 checkboxes em 100% das sessões

---

### **Métrica 2: Profundidade do Questionamento Socrático**
**Objetivo:** Provocar reflexão real, não apenas informação superficial

**Como medir:**
- Agente fez entre 8-15 perguntas por sessão? (não muito pouco, não excessivo)
- Perguntas seguem padrão "Como você...", "Por que...", "O que acontece se..."?
- Agente evitou dar respostas prontas?

**Meta:** 80% das sessões atingem esse padrão

---

### **Métrica 3: Identificação de Gaps**
**Objetivo:** Revelar lacunas que o educador não tinha considerado

**Como medir:**
- Agente identificou pelo menos 1 aspecto que educador não tinha planejado?
- Educador expressou insight tipo "Não tinha pensado nisso" ou similar?
- Agente ofereceu pelo menos 2 sugestões práticas (exercícios, perguntas para alunos)?

**Meta:** 70% das sessões revelam algum gap

---

### **Métrica 4: Utilidade Percebida pelo Educador**
**Objetivo:** Educador sente que a sessão foi valiosa

**Como medir (feedback pós-sessão):**
- Educador aplicaria pelo menos 1 sugestão do agente? (Sim/Não)
- Sessão ajudou a clarificar ensino de Delegation? (Escala 1-5)
- Educador usaria o agente novamente? (Sim/Não)

**Meta:**
- 80% aplicariam sugestões
- Média ≥ 4.0 na escala de clarificação
- 85% usariam novamente

---

### **Métrica 5: Tempo e Eficiência**
**Objetivo:** Sessão produtiva sem ser excessivamente longa

**Como medir:**
- Sessão teve entre 5-10 trocas de mensagens?
- Educador conseguiu responder perguntas sem frustração?
- Agente convergiu para sugestões práticas em tempo razoável?

**Meta:** 75% das sessões dentro desse range

---

### **Como Validar na Prática:**

#### **Fase 1: Teste Piloto (primeiras 5 sessões)**
- Executar com 5 educadores diferentes
- Coletar dados de todas as 5 métricas
- Identificar padrões de falha

#### **Fase 2: Iteração (se < 70% das metas atingidas)**
- Ajustar prompt do agente baseado em falhas
- Re-testar com 3 novos educadores
- Comparar melhorias

#### **Fase 3: Validação Final**
- 10 sessões adicionais
- Meta: ≥ 70% das métricas atingidas
- Documentar casos de sucesso e fracasso

---

## 🎯 Objetivo Final Mensurável

**O Delegation Coach é considerado bem-sucedido quando:**

✅ **90%** das sessões cobrem as 3 subcategorias completamente
✅ **80%** das sessões usam questionamento socrático profundo
✅ **70%** das sessões revelam pelo menos 1 gap
✅ **80%** dos educadores aplicariam sugestões
✅ **75%** das sessões têm duração eficiente

**Status Atual:** Não testado (aguardando Fase 1: Teste Piloto)

---

## 🚀 Como Usar

Copie todo o conteúdo de `delegation-coach.md` e cole no início de uma nova conversa do Claude Code, depois forneça seu contexto como educador.

---

© 2025 - Baseado no Framework de Fluência em IA (Rick Dakan, Joseph Feller, Anthropic)
**Licença:** [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)
