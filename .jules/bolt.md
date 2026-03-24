## 2024-03-23 - N+1 Query in Household Users
**Learning:** The `GoogleSyncService`'s `_household_users` method previously fetched a list of user IDs for a calendar, then queried `UserRepository.get_user_by_id` individually in a loop, creating an N+1 query issue.
**Action:** Created `UserRepository.get_users_by_calendar_id` to fetch all users in a single query. Future queries fetching lists of entities by relation ID should be audited for this pattern.
## 2024-05-24 - Pre-compile regex for performance
**Learning:** Instantiating and compiling regular expressions inside tight loops or frequently called functions adds significant, unnecessary CPU overhead.
**Action:** When a static set of string patterns is used repeatedly (like locale keywords in NLP), compile them to `re.Pattern` objects during class initialization or at the module level.

## 2024-05-23 - [Precompute Monthly Overview Variables]
**Learning:** In hot loops such as calculating monthly budget overviews, fetching repeated values from a dictionary using `get()` and constantly evaluating defaults within the loop creates measurable processing overhead (especially when multiplied by many users or years).
**Action:** When a loop iterates over fixed bounds (e.g., months 1-12), use a pre-allocated array of corresponding size and pre-compute repetitive math operations. In Python, list indexing combined with ahead-of-time calculations is substantially faster than inline dictionary lookups and conditional default evaluations.
