# Meta (Facebook/Instagram) App Configuration Guide

This guide will walk you through the complete process of creating and configuring a Meta (Facebook) app for use with TheCrowdVoice social analytics platform.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Creating a Meta App](#creating-a-meta-app)
3. [Configuring Facebook Login](#configuring-facebook-login)
4. [Setting Up Required Permissions](#setting-up-required-permissions)
5. [Configuring OAuth Redirect URIs](#configuring-oauth-redirect-uris)
6. [Getting Your App Credentials](#getting-your-app-credentials)
7. [App Review Process](#app-review-process)
8. [Testing Your Integration](#testing-your-integration)
9. [Production Deployment](#production-deployment)
10. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before you begin, make sure you have:

- A Facebook account (business account recommended for production apps)
- Access to [Meta for Developers](https://developers.facebook.com/)
- Your application's domain and redirect URIs ready
- Basic understanding of OAuth 2.0 flow

---

## Creating a Meta App

### Step 1: Access Meta for Developers

1. Go to [https://developers.facebook.com/](https://developers.facebook.com/)
2. Log in with your Facebook account
3. Click on **"My Apps"** in the top right corner
4. Click **"Create App"** button

### Step 2: Select App Type

**For the new Meta Developer Console (2024-2025):**

1. Choose **"Authenticate and request data from users with Facebook Login"** from the suggested use cases
2. Select app type: **"Business"** (recommended for production applications)
3. When asked "Are you building a game?", select **"No, I'm not building a game"**
4. Click **"Next"**

### Step 3: Configure Basic App Information

Fill in the following details:

- **App Name**: Choose a descriptive name (e.g., "TheCrowdVoice Analytics" or your brand name)
- **App Contact Email**: Your business/support email address
- **Business Account**: (Optional) Link to your Meta Business Account if you have one
- Click **"Create App"**

### Step 4: Complete Security Check

Complete the security verification (CAPTCHA) to confirm you're not a robot.

---

## Configuring Facebook Login

### Step 1: Add Facebook Login Product

1. From your App Dashboard, locate **"Add Products"** section
2. Find **"Facebook Login for Business"** and click **"Set Up"**
   - Note: "Facebook Login for Business" enables access for most app modules and provides the necessary authentication capabilities

### Step 2: Select Platform

1. Choose **"Web"** as your platform
2. You may be asked to provide your site URL - enter your application's base URL
   - Development: `http://localhost:3000`
   - Production: `https://yourdomain.com`

---

## Setting Up Required Permissions

TheCrowdVoice requires the following permissions to function properly:

### Required Facebook Permissions

| Permission | Purpose | Access Level |
|------------|---------|--------------|
| `pages_show_list` | List all Facebook Pages the user manages | Standard Access |
| `pages_read_engagement` | Read engagement data (comments, reactions, messages) from Pages | Advanced Access |
| `pages_manage_metadata` | Read and update Page metadata | Advanced Access |
| `pages_messaging` | Send and receive messages on behalf of Pages | Advanced Access |

### Required Instagram Permissions (if using Instagram)

| Permission | Purpose | Access Level |
|------------|---------|--------------|
| `instagram_basic` | Access basic Instagram account information | Standard Access |
| `instagram_manage_messages` | Read and respond to Instagram Direct messages | Advanced Access |
| `instagram_manage_comments` | Read, create, and delete comments | Advanced Access |

### How to Request Permissions

#### For Development/Testing (Standard Access):

During development, you automatically have access to:
- `public_profile`
- `email`
- `pages_show_list`
- `instagram_basic`

#### For Production (Advanced Access):

1. Go to your App Dashboard
2. Navigate to **"App Review"** > **"Permissions and Features"**
3. Find each required permission (e.g., `pages_read_engagement`, `pages_messaging`)
4. Click **"Request Advanced Access"**
5. For each permission:
   - Read and agree to the terms and conditions
   - Click **"Confirm"**
   - You'll need to complete the App Review process (see [App Review Process](#app-review-process))

---

## Configuring OAuth Redirect URIs

OAuth redirect URIs are critical for the OAuth 2.0 authentication flow. You must register all URIs where Meta will redirect users after authentication.

### Step 1: Navigate to Facebook Login Settings

1. From your App Dashboard, go to **"Products"** > **"Facebook Login"** > **"Settings"**
2. Scroll down to **"Client OAuth Settings"**

### Step 2: Add Valid OAuth Redirect URIs

Add the following URIs based on your environment:

#### Development Environment:
```
http://localhost:8000/api/channels/facebook/callback
http://localhost:8000/api/channels/instagram/callback
http://127.0.0.1:8000/api/channels/facebook/callback
http://127.0.0.1:8000/api/channels/instagram/callback
```

#### Production Environment:
```
https://yourdomain.com/api/channels/facebook/callback
https://yourdomain.com/api/channels/instagram/callback
```

### Step 3: Configure Additional OAuth Settings

In the same **"Client OAuth Settings"** section:

- **Valid OAuth Redirect URIs**: (added above)
- **Login from Devices**: OFF (unless you're building a device flow)
- **Use Strict Mode for Redirect URIs**: ON (recommended for security)
- **Enforce HTTPS**: ON (for production)

### Step 4: Save Changes

Click **"Save Changes"** at the bottom of the page.

---

## Getting Your App Credentials

### Step 1: Navigate to Basic Settings

1. From your App Dashboard, go to **"Settings"** > **"Basic"**

### Step 2: Retrieve Your Credentials

You'll find:

- **App ID**: This is your `FACEBOOK_APP_ID` / `INSTAGRAM_APP_ID`
- **App Secret**: Click **"Show"** to reveal it. This is your `FACEBOOK_APP_SECRET` / `INSTAGRAM_APP_SECRET`

### Step 3: Update Your Environment Configuration

Update your `.env` file with these credentials:

```env
# Facebook App credentials
FACEBOOK_APP_ID=your_app_id_here
FACEBOOK_APP_SECRET=your_app_secret_here
FACEBOOK_REDIRECT_URI=http://localhost:8000/api/channels/facebook/callback

# Instagram (uses Facebook credentials)
INSTAGRAM_APP_ID=your_app_id_here
INSTAGRAM_APP_SECRET=your_app_secret_here
```

**Security Note**: Never commit your `.env` file to version control. Keep your App Secret confidential.

---

## App Review Process

To use advanced permissions in production, you must submit your app for Meta's App Review.

### When Do You Need App Review?

- **Development/Testing**: Standard Access permissions work without review
- **Production**: Advanced Access permissions require App Review
- **Public Apps**: Any app accessible to users outside your business requires review

### Preparing for App Review

#### 1. Build Your App First

Your app must be functional and demonstrate the use of each requested permission.

#### 2. Prepare Documentation

For each permission, you need to provide:

- **Use Case Description**: Clear explanation of why you need the permission
- **Step-by-Step Instructions**: How users will trigger the permission
- **Screencast/Video**: Video demonstration showing:
  - User logging in
  - Granting the permission
  - The feature that uses the permission
  - End-to-end user flow

#### 3. Submit for Review

1. Go to **"App Review"** > **"Permissions and Features"**
2. For each permission needing Advanced Access:
   - Click **"Request Advanced Access"**
   - Fill out the submission form
   - Upload your screencast
   - Provide detailed instructions
3. Submit and wait for review (typically 3-7 business days)

### Review Tips

- Make the review process as easy as possible:
  - Provide test credentials if needed
  - Include clear, narrated videos
  - Write detailed step-by-step instructions
  - Ensure your app is publicly accessible or provide staging access
- Be specific about the business use case
- Show respect for user privacy and data handling

---

## Testing Your Integration

### Step 1: Add Test Users

During development, you can create test users:

1. Go to **"Roles"** > **"Test Users"**
2. Click **"Add Test Users"**
3. Create test accounts for testing the OAuth flow

### Step 2: Add Your Facebook Account

Add your own Facebook account as an app admin:

1. Go to **"Roles"** > **"Roles"**
2. Under **"Administrators"**, click **"Add Administrators"**
3. Add your Facebook account

### Step 3: Test the OAuth Flow

1. Start your application:
   ```bash
   docker-compose up
   ```

2. Navigate to `http://localhost:3000`

3. Log in to your app

4. Go to **"Channels"** page

5. Click **"Connect Facebook"** or **"Connect Instagram"**

6. You should be redirected to Facebook's OAuth dialog

7. Grant the requested permissions

8. You should be redirected back to your app with a success message

### Step 4: Verify in Meta Dashboard

1. Go to **"App Review"** > **"Permission and Features"**
2. Click on a permission to see its usage
3. Verify that tokens are being generated correctly

### Step 5: Test API Calls

Use the [Graph API Explorer](https://developers.facebook.com/tools/explorer/):

1. Select your app from the dropdown
2. Get a User Access Token
3. Add the permissions you want to test
4. Make test API calls to verify functionality

---

## Production Deployment

### Step 1: Update Environment Variables

For production, update your `.env` file:

```env
# Django settings
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# CORS
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Facebook App credentials (Production)
FACEBOOK_APP_ID=your_production_app_id
FACEBOOK_APP_SECRET=your_production_app_secret
FACEBOOK_REDIRECT_URI=https://yourdomain.com/api/channels/facebook/callback

# Instagram
INSTAGRAM_APP_ID=your_production_app_id
INSTAGRAM_APP_SECRET=your_production_app_secret
```

### Step 2: Update App Settings in Meta

1. Go to **"Settings"** > **"Basic"**
2. Update **"App Domains"**: Add your production domain (e.g., `yourdomain.com`)
3. Update **"Privacy Policy URL"**: Add your privacy policy URL
4. Update **"Terms of Service URL"**: Add your terms of service URL

### Step 3: Update OAuth Redirect URIs

Add production URIs to **"Facebook Login"** > **"Settings"** > **"Valid OAuth Redirect URIs"**:

```
https://yourdomain.com/api/channels/facebook/callback
https://yourdomain.com/api/channels/instagram/callback
```

### Step 4: Switch App to Live Mode

1. Go to **"Settings"** > **"Basic"**
2. At the top of the page, toggle the app mode from **"Development"** to **"Live"**
3. Confirm the switch

**Important**: Only switch to Live mode after:
- Completing App Review for all required permissions
- Testing thoroughly in development mode
- Updating all production settings

### Step 5: Monitor Your App

- Set up **"Webhooks"** for real-time updates (optional but recommended)
- Monitor usage in **"Analytics"** dashboard
- Check **"Alerts"** regularly for any issues

---

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: "Invalid OAuth Redirect URI"

**Symptoms**: After clicking "Connect Facebook", you get an error about invalid redirect URI.

**Solutions**:
- Verify the redirect URI in your `.env` matches exactly what's in Meta dashboard
- Check for typos, including `http` vs `https`
- Ensure no trailing slashes where they shouldn't be
- Make sure you saved changes in Meta dashboard after adding URIs

#### Issue 2: "This endpoint requires the 'pages_read_engagement' permission"

**Symptoms**: API calls fail with permission errors.

**Solutions**:
- Verify you've requested Advanced Access for the permission
- Check if App Review has been approved
- Ensure the permission is included in the OAuth scope in `backend/social_analytics/channels/views.py:29`
- Regenerate the access token with the correct scopes

#### Issue 3: "Error validating access token"

**Symptoms**: API calls fail with token validation errors.

**Solutions**:
- Check if the access token has expired
- Verify `FACEBOOK_APP_ID` and `FACEBOOK_APP_SECRET` in `.env` are correct
- Ensure the app is not in Development mode with restricted access
- Try disconnecting and reconnecting the channel

#### Issue 4: App Review Rejected

**Symptoms**: Your app review submission was rejected.

**Solutions**:
- Read the rejection reason carefully
- Common reasons:
  - Unclear use case explanation
  - Poor quality screencast
  - Missing privacy policy
  - Not demonstrating the actual use of the permission
- Address the specific feedback and resubmit
- Make sure your screencast is clear and shows the complete user flow

#### Issue 5: "App Not Set Up: This app is still in development mode"

**Symptoms**: Users can't connect their accounts.

**Solutions**:
- Add users as App Admins/Developers/Testers under **"Roles"**
- Or complete App Review and switch to Live mode
- For testing, use Test Users feature

### Getting Help

- **Meta for Developers Documentation**: [https://developers.facebook.com/docs](https://developers.facebook.com/docs)
- **Graph API Explorer**: [https://developers.facebook.com/tools/explorer/](https://developers.facebook.com/tools/explorer/)
- **Meta Developer Community**: [https://developers.facebook.com/community/](https://developers.facebook.com/community/)
- **Stack Overflow**: Tag your questions with `facebook-graph-api`

---

## Additional Resources

### Official Documentation

- [Facebook Login Manual Flow](https://developers.facebook.com/docs/facebook-login/guides/advanced/manual-flow)
- [Facebook Permissions Reference](https://developers.facebook.com/docs/permissions/reference)
- [Graph API Reference](https://developers.facebook.com/docs/graph-api)
- [App Review Documentation](https://developers.facebook.com/docs/app-review)
- [Instagram Graph API](https://developers.facebook.com/docs/instagram-api)

### Platform-Specific URLs

| Environment | Facebook Auth URL | Instagram Auth URL |
|-------------|-------------------|-------------------|
| Development | `http://localhost:3000/channels` | `http://localhost:3000/channels` |
| Production | `https://yourdomain.com/channels` | `https://yourdomain.com/channels` |

### API Versions

The platform currently uses **Facebook Graph API v18.0**. Check the code in:
- `backend/social_analytics/channels/views.py:32` - OAuth URL
- `backend/social_analytics/channels/views.py:53` - Token exchange URL

To update to a newer version, update the version string in these locations.

---

## Security Best Practices

1. **Never commit secrets**: Keep `.env` file out of version control
2. **Use HTTPS in production**: Always use HTTPS for production OAuth redirects
3. **Rotate secrets regularly**: Change your App Secret periodically
4. **Implement rate limiting**: Protect your API endpoints from abuse
5. **Validate state parameter**: The platform passes user ID in state - verify it matches the logged-in user
6. **Store tokens securely**: Tokens are stored in the database - ensure database security
7. **Monitor for suspicious activity**: Use Meta's Analytics dashboard to monitor usage
8. **Follow data minimization**: Only request permissions you actually need
9. **Respect token expiration**: Implement proper token refresh logic
10. **Comply with Meta policies**: Stay updated with Meta's Platform Terms and Developer Policies

---

## Quick Reference

### Environment Variables Required

```env
FACEBOOK_APP_ID=your_facebook_app_id
FACEBOOK_APP_SECRET=your_facebook_app_secret
FACEBOOK_REDIRECT_URI=http://localhost:8000/api/channels/facebook/callback
INSTAGRAM_APP_ID=your_facebook_app_id
INSTAGRAM_APP_SECRET=your_facebook_app_secret
```

### OAuth Scopes Used

**Facebook**: `pages_show_list,pages_read_engagement,pages_manage_metadata,pages_messaging`

**Instagram**: `instagram_basic,instagram_manage_messages,instagram_manage_comments`

### Key Files in Codebase

- `backend/social_analytics/channels/views.py` - OAuth flow implementation
- `backend/social_analytics/channels/models.py` - SocialAccount model
- `.env` - Environment configuration
- `.env.example` - Environment template

---

## Changelog

- **2025**: Updated for new Meta Developer Console interface
- **2024**: Added Instagram integration support
- **2024**: Updated permissions requirements for latest Graph API

---

## Support

If you encounter issues not covered in this guide:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review Meta's official documentation
3. Search for similar issues on Stack Overflow
4. Open an issue on the project's GitHub repository

---

**Last Updated**: January 2025
**Platform Version**: TheCrowdVoice MVP
**Graph API Version**: v18.0
