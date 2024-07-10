import { generateObject } from "ai"
import { openai } from "@ai-sdk/openai"
import { z } from 'zod';
import dotenv from 'dotenv';

dotenv.config();

async function main() {
  const { object } = await generateObject({
    model: openai("gpt-4o"),
    maxTokens: 4096,
    schema: z.object({
      users: z.array(
        z.object({
          firstname: z.string(),
          lastname: z.string(),
          age: z.string(),
        })
      ),
    }),
    prompt: 'Generate 10 mocking data',
  });
  console.log(object)
  console.log(object.users[0].firstname)
}

main().catch(console.error)