import { PrismaClient } from "@prisma/client"

const prisma = new PrismaClient()

async function main() {
  console.log("🌱 Initiating Industrial Seeding Protocol...")

  // Materialize Core Shards
  const legalShard = await prisma.shard.upsert({
    where: { slug: "legal-shard-01" },
    update: {},
    create: {
      name: "Sovereign Legal Shard",
      slug: "legal-shard-01",
      vertical: "LEGAL",
      status: "ACTIVE",
    },
  })

  const medicalShard = await prisma.shard.upsert({
    where: { slug: "medical-shard-01" },
    update: {},
    create: {
      name: "Sovereign Medical Shard",
      slug: "medical-shard-01",
      vertical: "MEDICAL",
      status: "ACTIVE",
    },
  })

  console.log("✅ Shards Materialized:", { legalShard: legalShard.slug, medicalShard: medicalShard.slug })
}

main()
  .catch((e) => {
    console.error("❌ Seeding Failure:", e)
    process.exit(1)
  })
  .finally(async () => {
    await prisma.$disconnect()
  })
