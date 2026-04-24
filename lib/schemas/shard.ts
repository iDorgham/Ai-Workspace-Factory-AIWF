import { z } from "zod"

export const createShardSchema = z.object({
  name: z.string().min(3).max(50),
  slug: z.string().min(3).max(20).regex(/^[a-z0-9-]+$/),
  vertical: z.enum(["LEGAL", "MEDICAL", "FINANCE", "HOSPITALITY", "INDUSTRIAL"]),
})

export type CreateShardInput = z.infer<typeof createShardSchema>
