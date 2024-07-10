import { generateText } from "ai"
import { openai } from "@ai-sdk/openai"
import dotenv from 'dotenv';

dotenv.config();

async function main() {
  const result = await generateText({
    model: openai("gpt-4o"),
    prompt: "Once upon a time",
  })

  console.log(result.text)
}

main().catch(console.error)