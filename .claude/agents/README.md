# Agentes de Coaching para Framework de Fluência em IA

Este diretório contém agentes especializados para ajudar educadores a aplicar o Framework de Fluência em IA corretamente.

## 📚 Agentes Disponíveis

### 1. **AI Fluency Coach** (`ai-fluency-coach.md`)
**Foco:** Visão geral dos 4Ds (Delegation, Description, Discernment, Diligence)

**Quando usar:**
- Primeira vez ensinando o framework
- Validação geral de planos de aula
- Reflexão pós-aula sobre cobertura dos 4Ds
- Criação de atividades que cobrem múltiplos Ds

**Abordagem:** Questionamento socrático para validar cobertura completa do framework

---

### 2. **Delegation Coach** (`delegation-coach.md`) ⭐ RECOMENDADO PARA COMEÇAR
**Foco:** Apenas Delegation - a fase de planejamento

**Quando usar:**
- Ensinar alunos a PLANEJAR antes de usar IA
- Validar se está ensinando as 3 subcategorias (Problem/Platform/Task Awareness)
- Conectar planejamento com responsabilidade ética (loop Delegation-Diligence)
- Ensinar alunos a escolher entre Automation, Augmentation, e Agency

**Abordagem:** Perguntas profundas sobre planejamento estratégico e ético

**As 3 perguntas fundamentais que este agente ajuda a ensinar:**
1. 🎯 "O que estou tentando realizar?" (Problem Awareness)
2. 🔧 "Quais sistemas de IA estão disponíveis?" (Platform Awareness)
3. 🤝 "Como divido o trabalho entre mim e a IA?" (Task Delegation)

---

## 🚀 Como Usar no Claude Code

### Método 1: Colar o Conteúdo na Conversa

1. Abra o arquivo do agente que quer usar (ex: `delegation-coach.md`)
2. Copie todo o conteúdo
3. No Claude Code, inicie uma nova conversa
4. Cole o conteúdo e adicione: "Você entendeu seu papel? Estou pronto para começar."
5. Comece descrevendo seu contexto de ensino

### Método 2: Usar como System Prompt (Recomendado)

Se você usa Claude via API ou Projects:
1. Use o conteúdo do agente como System Prompt
2. Inicie a conversa descrevendo seu contexto
3. O agente guiará com perguntas

---

## 💡 Exemplo de Uso: Delegation Coach

### Passo 1: Carregar o Agente
```
[Cole o conteúdo de delegation-coach.md]

Entendi meu papel como Delegation Coach. Estou pronto para ajudar você a ensinar planejamento estratégico com IA!

Vamos começar: qual é o contexto dos seus alunos (nível, disciplina, experiência com IA)?
```

### Passo 2: Fornecer Contexto
**Você (Educador):**
```
Ensino Marketing Digital para alunos de graduação (3º ano).
Eles já usam IA casualmente (ChatGPT para resumos), mas não planejam estrategicamente.
Quero ensinar a criar campanhas de marketing usando IA de forma profissional.
```

### Passo 3: Agente Guia com Perguntas
**Delegation Coach:**
```
Ótimo contexto! Vamos explorar como você pode ensinar Delegation nesse cenário de campanhas de marketing.

🎯 Problem Awareness:
- Como você vai ajudar os alunos a definirem objetivos CLAROS da campanha antes de abrir uma IA?
- Você vai ensiná-los a questionar SE devem usar IA para cada etapa, ou assumir que sempre devem?
- Que partes da criação de campanha NÃO devem ser delegadas à IA?

🔧 Platform Awareness:
- Quais ferramentas vocês vão comparar? (ex: ChatGPT para copy, Midjourney para visual, Claude para estratégia)
- Como você vai ensinar as LIMITAÇÕES de cada ferramenta - não só o que podem fazer?

🤝 Task Delegation:
- Como os alunos decidirão o que a IA faz vs o que eles fazem na campanha?
- Você vai mostrar diferentes estratégias de divisão? (ex: IA gera ideias, humano seleciona e refina)

Me conte, qual dessas áreas você já tinha pensado?
```

### Passo 4: Diálogo Iterativo
Continue respondendo e o agente continuará fazendo perguntas que revelam lacunas e sugerem melhorias.

---

## 🎯 Qual Agente Escolher?

### Use **Delegation Coach** quando:
- ✅ Quer ensinar PLANEJAMENTO (antes de usar IA)
- ✅ Alunos usam IA sem pensar (querem eficiência imediata)
- ✅ Precisa ensinar escolha de ferramentas
- ✅ Quer conectar planejamento com ética
- ✅ Foco em decisões estratégicas

**Cenários típicos:**
- "Meus alunos abrem ChatGPT sem saber o que querem"
- "Precisam aprender a escolher entre diferentes IAs"
- "Quero ensinar divisão de trabalho humano-IA"

### Use **AI Fluency Coach** quando:
- ✅ Quer validação geral dos 4Ds
- ✅ Já ensina o framework mas quer feedback
- ✅ Precisa de visão holística
- ✅ Quer criar atividades que cobrem múltiplos Ds

**Cenários típicos:**
- "Quero validar se meu plano de aula cobre tudo"
- "Preciso de feedback sobre meu ensino atual"
- "Quero criar uma atividade completa de Fluência em IA"

---

## 📖 Recursos de Apoio

Estes agentes fazem referência ao conteúdo do Framework em `/docs`:

### Para Delegation:
- `/docs/comecando/licao1-video2.md` - Loop Delegation-Diligence
- `/docs/avaliacao/matriz-delegation.md` - Matriz de avaliação
- `/docs/comecando/visao-geral.md` - 3 Modalidades de interação

### Para Framework Completo:
- `/docs/intro.md` - Introdução ao Framework
- `/docs/comecando/4ds-e-modalidades.md` - Explicação dos 4Ds
- `/docs/comecando/documento-completo.md` - Framework detalhado

---

## 🔄 Fluxo Recomendado

### Para Educadores Iniciantes:
1. **Comece com Delegation Coach** - Ensine planejamento primeiro
2. Depois ensine Description-Discernment (execução)
3. Finalize com Diligence (responsabilidade)
4. Use AI Fluency Coach para validação geral

### Para Educadores Experientes:
1. Use AI Fluency Coach para diagnóstico geral
2. Use Delegation Coach para aprofundar áreas específicas
3. Itere baseado no feedback dos agentes

---

## 💬 Dicas de Uso

### ✅ Boas Práticas:
- Seja específico sobre o contexto dos alunos
- Responda honestamente às perguntas do agente
- Use o agente ANTES de dar a aula (planejamento)
- Use o agente DEPOIS da aula (reflexão)
- Compartilhe exemplos reais de trabalhos dos alunos

### ❌ Evite:
- Respostas genéricas ("vou ensinar os 4Ds")
- Pular perguntas do agente
- Esperar respostas prontas (agentes usam questionamento socrático)
- Usar apenas uma vez (são para uso contínuo)

---

## 🎓 Objetivo Final

Estes agentes existem para garantir que educadores ensinem o Framework de Fluência em IA de forma:

- **Eficaz:** Alunos realmente desenvolvem competências
- **Eficiente:** Foco no que importa
- **Ética:** Conexão entre planejamento e responsabilidade
- **Segura:** Alunos entendem riscos e limitações

---

## 🤝 Contribuindo

Estes agentes evoluem com uso. Se você:
- Descobriu uma pergunta útil que falta
- Identificou um gap no coaching
- Tem sugestões de exercícios

Abra uma issue ou PR no repositório!

---

© 2025 - Baseado no Framework de Fluência em IA (Rick Dakan, Joseph Feller, Anthropic)
**Licença:** [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)
