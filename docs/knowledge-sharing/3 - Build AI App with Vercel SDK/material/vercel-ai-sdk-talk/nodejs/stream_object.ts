import { streamObject } from "ai"
import { openai } from "@ai-sdk/openai"
import { z } from 'zod';
import dotenv from 'dotenv';

dotenv.config();

async function main() {
  const { partialObjectStream } = await streamObject({
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
  for await (const partialObject of partialObjectStream) {
    console.log(partialObject);
    // sleep for 1 seconds
    await new Promise(r => setTimeout(r, 1000));
  }
}

main().catch(console.error)