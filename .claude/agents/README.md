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
