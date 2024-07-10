import { streamText } from "ai"
import { openai } from "@ai-sdk/openai"
import dotenv from 'dotenv';

dotenv.config();

async function main() {
  const result = await streamText({
    model: openai("gpt-4o"),
    prompt: "Once upon a time",
  })

  for await (const textPart of result.textStream) {
    console.log(textPart);
  }
}

main().catch(console.error)