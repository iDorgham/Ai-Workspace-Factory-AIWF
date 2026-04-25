---
name: firebase-app-hosting-basics
description: Deploy and manage web apps with Firebase App Hosting. Use this skill when deploying Next.js/Angular apps with backends.
---

# App Hosting Basics

## Description
This skill enables the agent to deploy and manage modern, full-stack web applications (Next.js, Angular, etc.) using Firebase App Hosting.

**Important**: Firebase App Hosting requires the Blaze pricing plan.

## Hosting vs App Hosting

**Choose Firebase Hosting if:**
- You are deploying a static site (HTML/CSS/JS)
- You are deploying a simple SPA (React, Vue, etc. without SSR)

**Choose Firebase App Hosting if:**
- You are using a supported full-stack framework like Next.js or Angular
- You need Server-Side Rendering (SSR) or ISR
- You want an automated "git push to deploy" workflow

## Deploying to App Hosting

1. Configure `firebase.json` with an `apphosting` block:
    ```json
    {
      "apphosting": {
        "backendId": "my-app-id",
        "rootDir": "/"
      }
    }
    ```
2. Create or edit `apphosting.yaml` for configuration
3. If the app needs sensitive keys, use `npx -y firebase-tools@latest apphosting:secrets` commands
4. Run `npx -y firebase-tools@latest deploy` when ready to deploy
