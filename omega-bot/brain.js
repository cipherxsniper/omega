import axios from "axios";
import dotenv from "dotenv";
import { saveMessage, getRecentMessages } from "./memory.js";

dotenv.config();

export async function askOmega(userId, message) {

  // Save user message
  saveMessage(userId, "user", message);

  // Load memory
  const history = await getRecentMessages(userId, 15);

  const systemPrompt = `
You are Omega Mind, a persistent AI system.

You:
- remember past conversations
- build context over time
- think deeply and logically
- ask follow-up questions
- adapt personality per user

You are not generic — you evolve based on memory.
`;

  const response = await axios.post(
    "https://api.groq.com/openai/v1/chat/completions",
    {
      model: process.env.MODEL,
      messages: [
        { role: "system", content: systemPrompt },

        ...history.map(h => ({
          role: h.role,
          content: h.message
        })),

        { role: "user", content: message }
      ]
    },
    {
      headers: {
        Authorization: `Bearer ${process.env.GROQ_API_KEY}`,
        "Content-Type": "application/json"
      }
    }
  );

  const reply = response.data.choices[0].message.content;

  // Save AI response
  saveMessage(userId, "assistant", reply);

  return reply;
}
