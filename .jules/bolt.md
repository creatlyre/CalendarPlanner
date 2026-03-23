## 2024-03-23 - N+1 Query in Household Users
**Learning:** The `GoogleSyncService`'s `_household_users` method previously fetched a list of user IDs for a calendar, then queried `UserRepository.get_user_by_id` individually in a loop, creating an N+1 query issue.
**Action:** Created `UserRepository.get_users_by_calendar_id` to fetch all users in a single query. Future queries fetching lists of entities by relation ID should be audited for this pattern.
