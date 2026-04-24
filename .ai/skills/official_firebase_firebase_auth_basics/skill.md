---
name: firebase-auth-basics
description: Guide for setting up and using Firebase Authentication. Use this skill when the user's app requires user sign-in, user management, or secure data access using auth rules.
compatibility: This skill is best used with the Firebase CLI, but does not require it. Firebase CLI can be accessed through `npx -y firebase-tools@latest`.
---

## Prerequisites

- **Firebase Project**: Created via `npx -y firebase-tools@latest projects:create`
- **Firebase CLI**: Installed and logged in

## Core Concepts

Firebase Authentication provides backend services, easy-to-use SDKs, and ready-made UI libraries to authenticate users to your app.

### Identity Providers

Firebase Auth supports multiple ways to sign in:
- **Email/Password**: Basic email and password authentication
- **Federated Identity Providers**: Google, Facebook, Twitter, GitHub, Microsoft, Apple, etc.
- **Phone Number**: SMS-based authentication
- **Anonymous**: Temporary guest accounts that can be linked to permanent accounts later

Google Sign In is recommended as a good and secure default provider.

## Workflow

### 1. Provisioning

Configure Firebase Authentication in `firebase.json`:

```json
{
  "auth": {
    "providers": {
      "anonymous": true,
      "emailPassword": true,
      "googleSignIn": {
        "oAuthBrandDisplayName": "Your Brand Name",
        "supportEmail": "support@example.com",
        "authorizedRedirectUris": ["https://example.com"]
      }
    }
  }
}
```

### 2. Security Rules

Secure your data using `request.auth` in Firestore/Storage rules.

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
  }
}
```
