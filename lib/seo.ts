import { Metadata } from "next"

export function generateSovereignMetadata({ 
  title, 
  description, 
  path,
  image = "/og-industrial.png"
}: { 
  title: string, 
  description: string, 
  path: string,
  image?: string
}): Metadata {
  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || "https://aiwf.sovereign"
  
  return {
    title: `${title} | AIWF Sovereign Shard`,
    description,
    openGraph: {
      title,
      description,
      url: `${siteUrl}${path}`,
      siteName: "AI Workspace Factory",
      images: [{ url: `${siteUrl}${image}` }],
      locale: "en_US",
      type: "website",
    },
    twitter: {
      card: "summary_large_image",
      title,
      description,
      images: [image],
    },
    alternates: {
      canonical: `${siteUrl}${path}`,
      languages: {
        "ar-EG": `${siteUrl}/ar${path}`,
      },
    },
    robots: {
      index: true,
      follow: true,
    }
  }
}
