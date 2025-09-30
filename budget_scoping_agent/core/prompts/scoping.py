"""Prompts for the budget search scoping workflow."""

clarify_with_user_instructions = """
These are the messages that have been exchanged so far from the user asking for budget information:

<Messages>
{messages}
</Messages>

Today's date is {date}. 
You should only speak portuguese.

Your task is to assess whether the user has provided both:
1. A clear TOPIC OF INTEREST (e.g., hospitals, education, infrastructure, health, security, etc.)
2. A specific REFERENCE YEAR (e.g., 2024, 2025, etc.)

IMPORTANT: If you can see in the messages history that you have already asked a clarifying question, you almost always do not need to ask another one. Only ask another question if ABSOLUTELY NECESSARY.

Examples of complete requests:
- "Me fale sobre o orçamento de hospitais em 2025" → hospitais + 2025 ✓
- "Quero saber sobre educação em 2024" → educação + 2024 ✓
- "Orçamento para segurança pública 2023" → segurança pública + 2023 ✓

Examples that need clarification:
- "Eu tenho interesse em saber sobre hospitais" → missing year ✗
- "Quero dados de 2024" → missing topic ✗
- "Me fale sobre o orçamento" → missing both ✗

If you need to ask a question:
- Be concise and direct
- Ask specifically for the missing information (topic, year, or both)
- Provide examples to help the user understand what you need
- Use markdown formatting for clarity
- Don't ask for unnecessary information that the user has already provided

Respond in valid JSON format with these exact keys:
- "need_clarification": boolean
- "question": "<question to ask the user>"
- "verification": "<verification message>"

If you need to ask a clarifying question, return:
- "need_clarification": true
- "question": "<your clarifying question asking for missing topic/year>"
- "verification": ""

If you do not need to ask a clarifying question, return:
- "need_clarification": false
- "question": ""
- "verification": "<acknowledgement that you have both topic and year and will proceed>"

For the verification message when no clarification is needed:
- Confirm that you identified both the topic of interest and reference year
- Briefly restate what you understood
- Confirm you will proceed with the budget search
- Keep it concise and professional
"""

transform_messages_into_research_topic_prompt = """
Based on the conversation history below, extract the topic of interest and reference year for the budget search.

<Conversation History>
{messages}
</Conversation History>

Today's date is {date}.
You should always speak portuguese.

CRITICAL: The topic should ALWAYS be just one word. So for example, if the user asks for
'Educação pública', use the most important, the most all-encompassing. In this case, for example,
you should use just 'educação'. That's critical for the system.

From the conversation, identify:
1. TOPIC OF INTEREST: The specific budget area/theme the user wants to know about (e.g., hospitais, educação, segurança, infraestrutura, saúde, etc.)
2. REFERENCE YEAR: The specific year for the budget data (e.g., 2024, 2025, etc.)

The search query should be in the format: "[topic] [year]"

Examples:
- User: "Me fale sobre o orçamento de hospitais em 2025" → Query: "hospitais 2025"
- User: "Quero saber sobre educação em 2024" → Query: "educação 2024"
- User: "Dados de segurança pública para 2023" → Query: "segurança 2023"
- User: "Eu quero mais informações sobre o que foi gasto com manutenção predial em 2024" → Query: "manutenção 2024"

Extract the most relevant and specific terms for the topic, keeping it concise but descriptive enough for an effective budget search.
"""