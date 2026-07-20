# kidobum - 24x7 Video Upload Automation

Automated video uploading pipeline for the `kidobum` channel.

## 🚀 Setup & Secrets Configuration

To make this GitHub Action work, you need to configure several Repository Secrets in GitHub. The most common error is configuring the Google/YouTube credentials incorrectly.

### 1. Generating Google Drive & YouTube Tokens

The scripts `agent1_fetcher.py` and `agent2_youtube.py` do NOT take the `client_secret.json` downloaded from Google Cloud directly. They require an **Authorized User Token** (a `token.json` file containing a `refresh_token`), because a GitHub Action runs on a server without a browser.

**To generate the correct secrets, run these helper scripts on your local computer:**

1. Download your OAuth 2.0 Client ID JSON from Google Cloud Console and save it as `client_secret.json` in this repository's folder on your PC.
2. Install the required Python packages locally:
   ```bash
   pip install google-auth-oauthlib google-api-python-client
   ```
3. Run the Drive token generator:
   ```bash
   python generate_drive_token.py
   ```
   A browser window will open. Log in and grant permissions. A `drive_token.json` file will be created.
   Copy the **entire contents** of `drive_token.json` and paste it into the GitHub Secret `GOOGLE_DRIVE_CREDENTIALS`.

4. Run the YouTube token generator:
   ```bash
   python generate_youtube_token.py
   ```
   A browser window will open. Log in and grant permissions. A `youtube_token.json` file will be created.
   Copy the **entire contents** of `youtube_token.json` and paste it into the GitHub Secret `YOUTUBE_CLIENT_SECRETS`.

### 2. Required GitHub Secrets List

| Secret Name | Description |
|---|---|
| `GOOGLE_DRIVE_CREDENTIALS` | The **Authorized User Token JSON** for Google Drive (contains `refresh_token`). |
| `YOUTUBE_CLIENT_SECRETS` | The **Authorized User Token JSON** for YouTube (contains `refresh_token`). |
| `LLM_API_KEY` | API Key for LLM to generate SEO metadata (e.g. OpenAI or Nvidia API key). |
| `FACEBOOK_ACCESS_TOKEN` | Long-lived Facebook Page Access Token for Reels publishing. |
| `FACEBOOK_PAGE_ID` | Facebook Page ID. |
| `DISCORD_WEBHOOK_URL` | Discord webhook URL for success/failure notifications. |

## 🐛 Common Errors

- **`Authorized user info was not in the expected format, missing fields refresh_token, client_secret.`**
  You pasted your Google Cloud `client_secret.json` into the `YOUTUBE_CLIENT_SECRETS` GitHub secret. You must run `generate_youtube_token.py` locally and paste the resulting token instead.
- **`Extra data: line X column Y` or JSON Parsing Errors from Facebook/YouTube Agents**
  These were caused by the LLM generating extra text or markdown alongside the JSON. The parsing regex has been updated to fix this.
