BHARATH LIVE - Discord Nickname Bot (Python)

Commands:
- /nick member:<member> nickname:<new nickname>
  Changes a member's server nickname.
- /resetnick member:<member>
  Resets a member's server nickname to their account name.

Render Background Worker:
Build Command:
  pip install -r requirements.txt

Start Command:
  python main.py

Environment Variable:
  Key: DISCORD_TOKEN
  Value: Your Discord bot token

Discord setup:
1. In Discord Developer Portal, create/open your application and add a Bot if needed.
2. Copy the bot token and add it to Render as DISCORD_TOKEN.
3. Invite the bot with the applications.commands scope and the bot scope.
4. Give the bot the Manage Nicknames permission.
5. In your server, move the bot's role ABOVE the roles of members it needs to manage.
6. Use /nick and /resetnick. The person using these commands must have Manage Nicknames.

Security:
- Never share your bot token.
- Never paste the token into main.py or upload it to GitHub.
- Keep DISCORD_TOKEN only in Render Environment Variables.
