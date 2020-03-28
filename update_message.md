##### Updated to version 0.5!
> In this version, I removed the need for database migrations by making the database 100% dynamic. Meaning when you run dashmachine your old site.db file will be deleted and a new one will be created using the data from config.ini. This will make adding features in the future easier and updates will break things less. To accomplish this you will notice that user management has been moved to config.ini. If you are upgrading from a previous version, your user table was deleted. Please login with default user/pass (which is now 'admin' and 'admin') and take a look at the users section in the readme to add users.

**Changelog**
- ui fixes
- users are now managed through config.ini
- no more alembic, completely dynamic database, created on startup
- users can now override global settings
- added update message
- performance fixes
- added setting for hiding sidebar by default
- broke up config readme into 3 tabs, and 3 .md files
- changed 'app templates' to 'card templates'
- added 'collection' cards
- added 'custom' cards
- added options for setting tag icons and sort position
- removed list view to focus on different card types on /home
- added ability to collapse/expand tags on /home
- added setting for having tags default to collapsed state
- created a public user view with no sidebar
- added sidebar default overrides for users
- fixes #57, #55, #45, #41, #40 